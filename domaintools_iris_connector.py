# --
# File: domaintools_iris_connector.py
#
# Copyright (c) 2019-2023 DomainTools, LLC
#
# --

import codecs
import json
import phantom.app as phantom
import re
import requests
import sys
import tldextract

from datetime import datetime, timedelta

from domaintools import API
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector


# Define the App Class
class DomainToolsConnector(BaseConnector):
    ACTION_ID_DOMAIN_REPUTATION = "domain_reputation"
    ACTION_ID_DOMAIN_ENRICH = "domain_enrich"
    ACTION_ID_DOMAIN_INVESTIGATE = "domain_investigate"
    ACTION_ID_PIVOT = "pivot_action"
    ACTION_ID_REVERSE_IP = "reverse_lookup_ip"
    ACTION_ID_REVERSE_EMAIL = "reverse_whois_email"
    ACTION_ID_REVERSE_DOMAIN = "reverse_lookup_domain"
    ACTION_ID_LOAD_HASH = "load_hash"

    def __init__(self):
        # Call the BaseConnectors init first
        super(DomainToolsConnector, self).__init__()

        self._ssl = None
        self._username = None
        self._key = None
        self._domains = None
        self._proxy_url = None

    def initialize(self):
        # get the app configuation - super class pulls domaintools_iris.json
        app_json_configuration = self.get_app_json()

        self.app_version_number = app_json_configuration.get("app_version", "")
        self.app_name = app_json_configuration.get("name", "")
        self.app_partner = "splunk_soar"

        # Fetching the Python major version
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(
                phantom.APP_ERROR,
                "Error occurred while getting the Splunk SOAR server's Python major version",
            )

        return phantom.APP_SUCCESS

    def _handle_py_ver_for_byte(self, input_str):
        """
        This method returns the binary|original string based on the Python version.
        :param input_str: Input string to be processed
        :return: input_str (Processed input string based on following logic 'input_str - Python 2; binary data input_str - Python 3')
        """
        if self._python_version < 3:
            return input_str
        else:
            return codecs.latin_1_encode(input_str)[0]

    def _get_error_message_from_exception(self, e):
        """This function is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """
        error_code = "Error code unavailable"
        error_msg = "Unknown error occurred. Please check the asset configuration and|or the action parameters."

        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except:
            pass

        return error_code, error_msg

    def _clean_empty_response(self, response):
        # PAPP-2087 DomainTools - Reverse Email table widget shows contextual action for no domain
        if response.get("domains") == []:
            del response["domains"]

    def _parse_response(self, action_result, response_json):
        """
        No need to do exception handling, since this function call has a try...except around it.
        If you do want to catch a specific exception to generate proper error strings, go ahead
        """

        response = response_json.get("response")
        error = response_json.get("error", {})
        status = int(error.get("code", 200))

        if status == 400:
            error_message = (
                "You must include at least one search parameter from the list: domain, ip, email, "
                "email_domain, nameserver_host, nameserver_domain, nameserver_ip, registrar, registrant, "
                "registrant_org, mailserver_host, mailserver_domain, mailserver_ip, redirect_domain, "
                "ssl_hash, ssl_subject, ssl_email, ssl_org, google_analytics, adsense, asn, isp_name, "
                "search_hash"
            )
            action_result.add_data({})
            return action_result.set_status(phantom.APP_ERROR, error_message)

        if status == 403:
            error_message = "The credentials you entered do not match an active account"
            action_result.add_data({})
            return action_result.set_status(phantom.APP_ERROR, error_message)

        if status == 404:
            action_result.add_data({})
            return action_result.set_status(
                phantom.APP_ERROR,
                error.get("message", "Domain Tools failed to find IP/Domain"),
            )

        if status == 503:
            error_message = error.get(
                "message",
                (
                    "There was an error processing your request. "
                    "Please try again or contact support (http://www.domaintools.com/support) with questions."
                ),
            )
            action_result.add_data({})
            return action_result.set_status(phantom.APP_ERROR, error_message)

        if (status == 200) and (response):
            self._clean_empty_response(response)

            if "results" in response:
                action_result.update_summary(
                    {"Connected Domains Count": len(response["results"])}
                )
                action_result.update_data(response["results"])
            else:
                action_result.add_data(response)

            if response.get("limit_exceeded"):
                msg = response.get(
                    "message", "Response limit exceeded, please narrow your search"
                )
                action_result.update_summary({"Error": msg})
                return action_result.set_status(phantom.APP_ERROR, msg)

            return action_result.set_status(phantom.APP_SUCCESS)

        return action_result.set_status(
            phantom.APP_ERROR,
            error.get(
                "message", "An unknown error occurred while querying domaintools"
            ),
        )

    def _do_query(self, service, action_result, query_args=None):
        """
        Call DT API and send the response to be parsed
        This function uses the DomainTools Python API to get the requested data from an action.
        Documentation: https://github.com/DomainTools/python_api
        :param: service (str): Currently only using iris_investigate, this the function call for dt api
        :param: action_result (obj): Splunk SOAR object
        :param: query_args (str): Parameters to send the service
        :return: APP_SUCCESS or APP_ERROR
        """

        self.save_progress("Connecting to domaintools")

        try:
            dt_api = API(
                self._username,
                self._key,
                app_partner=self.app_partner,
                app_name=self.app_name,
                app_version=self.app_version_number,
                proxy_url=self._proxy_url,
                verify_ssl=self._ssl,
                https=self._ssl,
                always_sign_api_key=True,
            )
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Unable connect to DomainTools API", e
            )

        try:
            domains = query_args.get("domains")
            service_api = getattr(dt_api, service)
            # Not optimal, there is probably a better way

            # Pagination parameters
            has_more_results = True
            position = None
            results_data = []

            while has_more_results:
                if isinstance(query_args, str):
                    response = service_api(query_args, position=position)
                elif domains:
                    query_args.pop("domains", None)
                    response = service_api(domains, **query_args, position=position)
                else:
                    response = service_api(**query_args, position=position)

                try:
                    response_json = response.data()
                except Exception as e:
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        "Unable to get data() from the DomainTools API response",
                        e,
                    )

                if response_json:
                    response = response_json.get("response", {})
                    has_more_results = response.get("has_more_results")
                    position = response.get("position")
                    results_data += response.get("results")

        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR,
                "Unable connect to DomainTools {} API".format(service),
                e,
            )

        self.save_progress(f"Parsing {len(results_data)} results...")
        response_json["response"]["results"] = self._convert_risk_scores_to_string(results_data)

        try:
            return self._parse_response(action_result, response_json)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR,
                "An error occurred while parsing DomainTools response",
                e,
            )

    def _convert_risk_scores_to_string(self, results_data):
        # We need this to make the table view sortable.
        # For some unknown reason, numeric values are not sortable using
        # the default table view from Splunk SOAR template.
        final_result = []
        for result in results_data:
            result.get("domain_risk").update(
                {
                    "risk_score_string": self._convert_null_value_to_empty_string(
                        result.get("domain_risk", {}).get("risk_score")
                    )
                }
            )
            final_result.append(result)

        # Make the final result sorted in descending order by default
        return sorted(
            final_result,
            key=lambda d: 0 if d.get("domain_risk", {}).get("risk_score_string") == "" else d.get("domain_risk", {}).get("risk_score"),
            reverse=True
        )

    def _test_connectivity(self):
        params = {"domains": "domaintools.net"}
        self.save_progress("Performing test query")

        # Progress
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, "domaintools.com")

        action_result = self.add_action_result(ActionResult(dict(params)))

        try:
            self._do_query("iris_investigate", action_result, query_args=params)
            if action_result.get_status() != phantom.APP_SUCCESS:
                raise Exception(action_result.get_message())
        except Exception as e:
            message = "Failed to connect to domaintools.com"
            action_result.set_status(phantom.APP_ERROR, message, e)
            return action_result.get_status()

        return self.set_status_save_progress(
            phantom.APP_SUCCESS,
            "Successfully connected to domaintools.com.\nTest Connectivity passed",
        )

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id: {}".format(self.get_action_identifier()))

        # Get the config
        config = self.get_config()

        self._username = config["username"]
        self._key = config["key"]
        self._ssl = self._get_ssl(config)
        self._proxy_url = self._get_proxy_url(config)

        # If there is a domains attribute, do tldextract
        # Note: Parameter remained to be named `domain` to avoid
        # modifying the Playbooks currently being used by customers
        domains = param.get("domain")
        if domains:
            hostnames = domains.replace(" ", "").strip(",").split(",")
            self._domains = self._get_domains(hostnames)
        # If pivoting  and the type is domain, set the query_vca
        if param.get("pivot_type") == "domain":
            hostnames = param.get("query_value").replace(" ", "").strip(",").split(",")
            self._domains = self._get_domains(hostnames)

        # Handle the actions
        if action_id == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
            ret_val = self._test_connectivity()
        elif action_id == self.ACTION_ID_DOMAIN_ENRICH:
            ret_val = self._domain_enrich(param)
        elif action_id == self.ACTION_ID_DOMAIN_INVESTIGATE:
            ret_val = self._domain_investigate(param)
        elif action_id == self.ACTION_ID_DOMAIN_REPUTATION:
            ret_val = self._domain_reputation(param)
        elif action_id == self.ACTION_ID_PIVOT:
            ret_val = self._pivot_action(param)
        elif action_id == self.ACTION_ID_REVERSE_IP:
            ret_val = self._reverse_lookup_ip(param)
        elif action_id == self.ACTION_ID_REVERSE_EMAIL:
            ret_val = self._reverse_whois_email(param)
        elif action_id == self.ACTION_ID_REVERSE_DOMAIN:
            ret_val = self._reverse_lookup_domain(param)
        elif action_id == self.ACTION_ID_LOAD_HASH:
            ret_val = self._load_hash(param)

        return ret_val

    def _get_proxy_url(self, config):
        proxy_url = None
        if config.get("proxy"):
            proxy_server = config.get("proxy_server")
            proxy_port = config.get("proxy_port")
            proxy_url = f"{proxy_server}:{proxy_port}"
            server_address = proxy_url

            if not (proxy_server and proxy_port):
                raise Exception("Must provide both a Proxy Server and Proxy Port.")

            protocol = "http"
            split_url = proxy_url.split("://")
            if len(split_url) == 2:
                protocol = split_url[0]
                server_address = split_url[1]
            else:
                proxy_url = f"{protocol}://{server_address}"

            if config.get("proxy_auth"):
                proxy_username = config.get("proxy_username")
                proxy_password = config.get("proxy_password")

                if not (proxy_username and proxy_password):
                    raise Exception("Must provide both a Proxy Username and Proxy Password.")

                proxy_url = f"{protocol}://{proxy_username}:{proxy_password}@{server_address}"

        return proxy_url

    def _get_ssl(self, config):
        custom_ssl_cert_path = config.get("custom_ssl_certificate_path")
        if config.get("custom_ssl_certificate"):
            if not custom_ssl_cert_path:
             raise Exception("Must provide the custom ssl certificate path.")
            return custom_ssl_cert_path

        return config.get("ssl", False)

    def _refang(self, line):
        """Refangs a line of text. See: https://bitbucket.org/johannestaas/defang
        :param str line: the line of text to reverse the defanging of.
        :return: the "dirty" line with actual URIs
        """
        dirty_line = re.sub(r"\((\.|dot)\)", ".", line, flags=re.IGNORECASE)
        dirty_line = re.sub(r"\[(\.|dot)]", ".", dirty_line, flags=re.IGNORECASE)
        dirty_line = re.sub(
            r"(\s*)h([x]{1,2})p([s]?)\[?:]?//",
            r"\1http\3://",
            dirty_line,
            flags=re.IGNORECASE,
        )
        dirty_line = re.sub(
            r"(\s*)(s?)fxp(s?)\[?:]?//",
            r"\1\2ftp\3://",
            dirty_line,
            flags=re.IGNORECASE,
        )
        dirty_line = re.sub(
            r"(\s*)\(([-.+a-zA-Z0-9]{1,12})\)\[?:]?//",
            r"\1\2://",
            dirty_line,
            flags=re.IGNORECASE,
        )
        return dirty_line

    # Borrowed from https://github.com/phantomcyber/phantom-apps/blob/master/Apps/phurlvoid/urlvoid_connector.py
    def _get_domains(self, hostnames):
        extract = None
        domains = []
        try:
            extract = tldextract.TLDExtract(suffix_list_urls=None)
        except Exception as e:
            raise Exception("tldextract result failed", e)

        for hostname in hostnames:
            cleaned = self._refang(hostname)
            result = extract(cleaned)
            domains.append("{0}.{1}".format(result.domain, result.suffix))

        return domains

    def _reverse_lookup_domain(self, param):
        action_result = self.add_action_result(ActionResult(param))
        params = {"domains": self._domains}
        ret_val = self._do_query("iris_investigate", action_result, query_args=params)

        if not ret_val:
            return action_result.get_data()

        data = action_result.get_data()

        if not data:
            return action_result.get_status()

        ips = []

        for a in data[0]["ip"]:
            if "address" in a:
                ips.append(
                    {
                        "ip": a["address"]["value"],
                        "type": "Host IP",
                        "count": a["address"]["count"],
                        "count_string": self._convert_null_value_to_empty_string(a["address"]["count"])
                    }
                )

        for a in data[0]["mx"]:
            if "ip" in a:
                for b in a["ip"]:
                    ips.append({"ip": b["value"], "type": "MX IP", "count": b["count"], "count_string": self._convert_null_value_to_empty_string(b["count"])}) # noqa

        for a in data[0]["name_server"]:
            if "ip" in a:
                for b in a["ip"]:
                    ips.append({"ip": b["value"], "type": "NS IP", "count": b["count"], "count_string": self._convert_null_value_to_empty_string(b["count"])}) # noqa

        sorted_ips = sorted(
            ips,
            key=lambda d: 0 if d.get("count_string") == "" else(d.get("count")),
            reverse=True)
        action_result.update_summary({"ip_list": sorted_ips})

        return action_result.get_status()

    def _convert_null_value_to_empty_string(self, value):
        return "" if value is None else f"{value:,}"

    def _domain_enrich(self, param):
        self.save_progress("Starting domain_enrich action.")
        action_result = self.add_action_result(ActionResult(param))

        params = {"domains": ",".join(self._domains)}
        self._do_query("iris_enrich", action_result, query_args=params)
        self.save_progress("Completed domain_enrich action.")

        return action_result.get_status()

    def _domain_investigate(self, param):
        self.save_progress("Starting domain_investigate action.")
        action_result = self.add_action_result(ActionResult(param))

        params = {"domains": self._domains}
        self._do_query("iris_investigate", action_result, query_args=params)
        self.save_progress("Completed domain_investigate action.")

        return action_result.get_status()

    def _domain_reputation(self, param):
        action_result = self.add_action_result(ActionResult(param))
        domain_to_query = self._domains
        params = {"domains": domain_to_query}

        ret_val = self._do_query("iris_investigate", action_result, query_args=params)

        if not ret_val:
            return action_result.get_data()

        data = action_result.get_data()

        if not data:
            return action_result.get_status()

        action_result.update_summary(
            {"domain_risk": data[0]["domain_risk"]["risk_score"]}
        )

        for a in data[0]["domain_risk"]["components"]:
            if a["name"] == "zerolist":
                action_result.update_summary({"zerolisted": True})
            else:
                action_result.update_summary({a["name"]: a["risk_score"]})

        return action_result.get_status()

    def _reverse_lookup_ip(self, param):
        updates = {"pivot_type": "ip", "query_value": param["ip"], "ip": param["ip"]}
        param.update(updates)
        return self._pivot_action(param)

    def _reverse_whois_email(self, param):
        updates = {
            "pivot_type": "email",
            "query_value": param["email"],
            "email": param["email"],
        }
        param.update(updates)
        return self._pivot_action(param)

    def _load_hash(self, param):
        param_hash = param.get("search_hash") or ""
        data = {
            "pivot_type": "search_hash",
            "query_value": param_hash,
            "hash": param_hash,
        }
        param.update(data)
        return self._pivot_action(param)

    def _pivot_action(self, param):
        action_result = self.add_action_result(ActionResult(param))
        query_field = param["pivot_type"] if param["pivot_type"] != "domain" else "domains"
        if query_field == "domains":
            query_value = self._domains
        else:
            query_value = param["query_value"]

        params = {query_field: query_value}

        if "tld" in param:
            params["tld"] = param["tld"]

        if "data_updated_after" in param:
            params["data_updated_after"] = param["data_updated_after"]
            if params["data_updated_after"].lower() == "today":
                params["data_updated_after"] = datetime.today().strftime("%Y-%m-%d")
            if params["data_updated_after"].lower() == "yesterday":
                params["data_updated_after"] = (
                    datetime.now() - timedelta(days=1)
                ).strftime("%Y-%m-%d")

        if "create_date" in param:
            params["create_date"] = param["create_date"]
            if params["create_date"].lower() == "today":
                params["create_date"] = datetime.today().strftime("%Y-%m-%d")
            if params["create_date"].lower() == "yesterday":
                params["create_date"] = (datetime.now() - timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )

        if "expiration_date" in param:
            params["expiration_date"] = param["expiration_date"]
            if params["expiration_date"].lower() == "today":
                params["expiration_date"] = datetime.today().strftime("%Y-%m-%d")
            if params["expiration_date"].lower() == "yesterday":
                params["expiration_date"] = (
                    datetime.now() - timedelta(days=1)
                ).strftime("%Y-%m-%d")

        if "status" in param and param["status"].lower() != "any":
            params["active"] = param["status"].lower() == "active"

        if "create_date_within" in param:
            params["create_date_within"] = param["create_date_within"]

        if "first_seen_within" in param:
            params["first_seen_within"] = param["first_seen_within"]

        if "first_seen_since" in param:
            params["first_seen_since"] = param["first_seen_since"]

        ret_val = self._do_query("iris_investigate", action_result, query_args=params)

        if not ret_val:
            return action_result.get_data()

        return action_result.get_status()


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = DomainToolsConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, timeout=60)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, data=data, headers=headers, timeout=60)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = DomainToolsConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
