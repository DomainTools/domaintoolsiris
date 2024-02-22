[comment]: # "Auto-generated SOAR connector documentation"
# DomainTools Iris Investigate

Publisher: DomainTools  
Connector Version: 1.5.1  
Product Vendor: DomainTools  
Product Name: DomainTools Iris Investigate  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.1.1  

This app supports investigative actions to profile domain names, get risk scores, and find connected domains that share the same Whois details, web hosting profiles, SSL certificates, and more on DomainTools Iris Investigate

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2024 DomainTools, LLC"
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""

[comment]: # "Monitoring/Scheduling Playbook(s) feature"
## DomainTools Iris Investigate Monitoring Playbook Feature
This feature allows the user to schedule playbooks to run on an specified interval and run it on a specific container/event ID you provided on each row. Coupled with our reference playbooks, linked below, this can be a powerful tool to notify you of domain infrastructure changes, or when newly created domains match specific infrastructure you're monitoring. See the individual playbooks for more information. This readme covers how to set up Iris Monitoring for those playbooks.

### Configuration
This feature depends on the 1 asset configuration fields that are **required** when using this feature.
| **Name** | **Description** | **Default Value** | **Required** |
| --- | --- | --- | --- |
| Splunk SOAR HTTPS port (default: 8443) | Splunk SOAR HTTP port if your instance uses one other than the default, 8443 | 8443 | Yes |

To configure this, you need to:
1. Go to **Apps**
2. Select **DomainTools Iris Investigate**
3. Select a configured asset or create one if you don't have any.
4. Go to **Asset Settings**
5. Look for `Splunk SOAR HTTPS port (default: 8443)` field. By default it contains `8443` value.


### Prerequisites
This feature uses a custom list named `domaintools_scheduled_playbooks`. <br>
To generate the custom list, you need to:
1. Go to **Apps**
2. Select **DomainTools Iris Investigate**
3, Select a configured asset or create one if you don't have any.
4. Go to **Actions** dropdown then;
5. Select '`configure scheduled playbooks`' action, then;
6. Hit `Test Action`.

If you go back to custom list page. you should have the `domaintools_scheduled_playbooks` generated for you.

**Note:** The values of this list has 6 columns and the header should not be altered. The last 3 columns are intentionally left blank and used by the playbook scheduler.<br>
**Sample domaintools_scheduled_playbooks table:**
| **repo/playbook_name** | **event_id** | **interval (mins)** | **last_run (server time)** | **last_run_status** | **remarks** |
| --- | --- | --- | --- | --- | --- |
| `local/DomainTools Monitor Domain Risk Score`| `<your_event_id>` | 1440 | | | |
| `local/DomainTools Monitor Domain Infrastructure`| `<your_event_id>` | 1440 | | | |
| `local/DomainTools Monitor Search Hash`| `<your_event_id>` | 1440 | | | |
In this example, we've specified to run three separate monitoring playbooks on daily schedules. Note that each scheduled lookup will consume Iris Investigate queries, depending how many domains or Iris search hashes are being monitored.<br>

### How to use monitoring/scheduling feature in DomainTools Iris Investigate App
1. Under **Apps** > **DomainTools Iris Investigate** > **Asset Settings** > **Ingest Settings** > **Label**, specify or select a label to apply to objects from this source. <br>
**Recommended:** Use a custom label rather using a predefined label like `events`.
2. Specify a polling interval to check if playbooks need to be run. Note that this is separate from the playbook run interval specified in step 4. We **recommend** running **every minute** for the most accurate scheduling.
3. Under Custom Lists > `domaintools_scheduled_playbooks` input your desired playbook schedule following the example in the Configuration Section<br>
**Note:** Make sure the label of the **playbook** and **event_id** you inputted shares the label that you selected in *Step 1*. The `domaintools_scheduled_playbooks` custom list should have been created when you updated our installed the DomainTools app, but if you don't see it, you can generate it by following the **Prerequisites** section of this page.

**Note:** For the DomainTools reference playbooks, see
[this](https://github.com/DomainTools/playbooks/tree/main/Splunk%20SOAR) Github repository.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a DomainTools Iris Investigate asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** |  required  | string | User Name
**key** |  required  | password | API Key
**proxy** |  optional  | boolean | Use Proxy
**proxy_auth** |  optional  | boolean | Use Proxy Authentication
**proxy_server** |  optional  | string | Proxy Server
**proxy_username** |  optional  | string | Proxy Username
**proxy_port** |  optional  | numeric | Proxy Port
**proxy_password** |  optional  | password | Proxy Password
**custom_ssl_certificate** |  optional  | boolean | Use Custom SSL Certificate
**ssl** |  optional  | boolean | Use SSL
**custom_ssl_certificate_path** |  optional  | string | Custom SSL Certificate Path
**http_port** |  optional  | string | Splunk SOAR HTTPS port (default: 8443)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity  
[domain reputation](#action-domain-reputation) - Evaluates the risk of a given domain  
[pivot action](#action-pivot-action) - Find domains connected by any supported Iris Investigate search parameter  
[reverse domain](#action-reverse-domain) - Extract IPs from a single domain response for further pivoting  
[reverse ip](#action-reverse-ip) - Find domains with web hosting IP, NS IP or MX IP  
[load hash](#action-load-hash) - Load or monitor Iris Investigate search results by Iris Investigate export hash  
[reverse email](#action-reverse-email) - Find domains with email in Whois, DNS SOA or SSL certificate  
[lookup domain](#action-lookup-domain) - Get all Iris Investigate data for a domain using the Iris Investigate API endpoint (required)  
[enrich domain](#action-enrich-domain) - Get all Iris Investigate data for a domain except counts using the high volume Iris Enrich API endpoint (if provisioned)  
[whois history](#action-whois-history) - Obtain historic whois records for a domain name  
[reverse whois](#action-reverse-whois) - Find domains based on terms in their Whois record  
[whois domain](#action-whois-domain) - Execute whois lookup on the given domain or IP  
[whois ip](#action-whois-ip) - Execute whois lookup on the given IP address  
[recent domains](#action-recent-domains) - Search for new domains containing a word  
[hosting history](#action-hosting-history) - Obtain changes to registrar, IP, etc  
[configure scheduled playbooks](#action-configure-scheduled-playbooks) - Run on initial setup to configure the optional monitoring playbooks. This action creates a custom list to manage the playbook scheduling and run status  
[on poll](#action-on-poll) - Execute scheduled playbooks based on the set interval(mins) in 'domaintools_scheduled_playbooks' custom list. Smaller intervals will result in more accurate schedules  

## action: 'test connectivity'
Validate the asset configuration for connectivity

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'domain reputation'
Evaluates the risk of a given domain

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain or comma-separated list of domains to query | string |  `url`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.domain | string |  `url`  `domain`  |  
action_result.data | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary.domain_risk | numeric |  |  
action_result.summary.zerolisted | boolean |  |   True  False 
action_result.summary.proximity | numeric |  |  
action_result.summary.threat_profile | numeric |  |  
action_result.summary.threat_profile_malware | numeric |  |  
action_result.summary.threat_profile_phishing | numeric |  |  
action_result.summary.threat_profile_spam | numeric |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'pivot action'
Find domains connected by any supported Iris Investigate search parameter

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query_value** |  required  | Value to query | string |  `url`  `domain`  `ip`  `email` 
**pivot_type** |  required  | Field to pivot on | string | 
**status** |  optional  | Return domains of this registration type | string | 
**data_updated_after** |  optional  | Iris Investigate records that were updated on or after midnight on this date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**tld** |  optional  | Limit results to only include domains in a specific top-level domain (i.e. “tld=com” or “tld=ru”) | string | 
**create_date** |  optional  | Only include domains created on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**create_date_within** |  optional  | Only include domains with a whois create date within the specified number of days (e.g. specifying '1' would indicate within the past day) | string | 
**first_seen_within** |  optional  | Only include domains with a current lifecycle first observed within the specified number of seconds (e.g. specifying '86400' would indicate within the past day) | string | 
**first_seen_since** |  optional  | Only include domains with a current lifecycle first observed since a specified datetime. (Example: 2023-04-10T00:00:00+00:00) | string | 
**expiration_date** |  optional  | Only include domains expiring on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.create_date | string |  |  
action_result.parameter.create_date_within | string |  |  
action_result.parameter.data_updated_after | string |  |  
action_result.parameter.first_seen_within | string |  |  
action_result.parameter.first_seen_since | string |  |  
action_result.parameter.expiration_date | string |  |  
action_result.data.\*.first_seen.count | numeric |  |  
action_result.data.\*.first_seen.value | string |  |  
action_result.data.\*.server_type.count | numeric |  |  
action_result.data.\*.server_type.value | string |  |  
action_result.data.\*.website_title.count | numeric |  |  
action_result.data.\*.website_title.value | string |  |  
action_result.parameter.pivot_type | string |  |  
action_result.parameter.query_value | string |  `url`  `domain`  `ip`  `email`  |  
action_result.parameter.status | string |  |  
action_result.parameter.tld | string |  |  
action_result.data.\*.domain | string |  `domain`  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.domain_risk.risk_score_string | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reverse domain'
Extract IPs from a single domain response for further pivoting

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain or comma-separated list of domains to query | string |  `url`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.domain | string |  `url`  `domain`  |  
action_result.data | string |  |  
action_result.data.\*.first_seen.count | numeric |  |  
action_result.data.\*.first_seen.value | string |  |  
action_result.data.\*.server_type.count | numeric |  |  
action_result.data.\*.server_type.value | string |  |  
action_result.data.\*.website_title.count | numeric |  |  
action_result.data.\*.website_title.value | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary.ip_list.\*.count | numeric |  |  
action_result.summary.ip_list.\*.count_string | string |  |  
action_result.summary.ip_list.\*.ip | string |  `ip`  |  
action_result.summary.ip_list.\*.type | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reverse ip'
Find domains with web hosting IP, NS IP or MX IP

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP address to query | string |  `ip` 
**status** |  optional  | Return domains of this registration type | string | 
**data_updated_after** |  optional  | Iris Investigate records that were updated on or after midnight on this date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**tld** |  optional  | Limit results to only include domains in a specific top-level domain (i.e. “tld=com” or “tld=ru”) | string | 
**create_date** |  optional  | Only include domains created on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**create_date_within** |  optional  | Only include domains with a whois create date within the specified number of days (e.g. specifying '1' would indicate within the past day) | string | 
**first_seen_within** |  optional  | Only include domains with a current lifecycle first observed within the specified number of seconds (e.g. specifying '86400' would indicate within the past day) | string | 
**first_seen_since** |  optional  | Only include domains with a current lifecycle first observed since a specified datetime. (Example: 2023-04-10T00:00:00+00:00) | string | 
**expiration_date** |  optional  | Only include domains expiring on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.create_date | string |  |  
action_result.parameter.create_date_within | string |  |  
action_result.parameter.data_updated_after | string |  |  
action_result.parameter.expiration_date | string |  |  
action_result.parameter.first_seen_within | string |  |  
action_result.parameter.first_seen_since | string |  |  
action_result.parameter.ip | string |  `ip`  |  
action_result.parameter.status | string |  |  
action_result.parameter.tld | string |  |  
action_result.data.\*.domain | string |  `domain`  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.domain_risk.risk_score_string | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'load hash'
Load or monitor Iris Investigate search results by Iris Investigate export hash

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**search_hash** |  required  | Paste the "Current Search Export" string (Advanced -> Import/Export Search) from Iris Investigate in this field to import up to 5000 domains | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.search_hash | string |  |  
action_result.data.\*.domain | string |  `domain`  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.domain_risk.risk_score_string | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reverse email'
Find domains with email in Whois, DNS SOA or SSL certificate

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**email** |  required  | Email query | string |  `email` 
**status** |  optional  | Return domains of this registration type | string | 
**data_updated_after** |  optional  | Iris Investigate records that were updated on or after midnight on this date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**tld** |  optional  | Limit results to only include domains in a specific top-level domain (i.e. “tld=com” or “tld=ru”) | string | 
**create_date** |  optional  | Only include domains created on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 
**create_date_within** |  optional  | Only include domains with a whois create date within the specified number of days (e.g. specifying '1' would indicate within the past day) | string | 
**first_seen_within** |  optional  | Only include domains with a current lifecycle first observed within the specified number of seconds (e.g. specifying '86400' would indicate within the past day) | string | 
**first_seen_since** |  optional  | Only include domains with a current lifecycle first observed since a specified datetime. (Example: 2023-04-10T00:00:00+00:00) | string | 
**expiration_date** |  optional  | Only include domains expiring on a specific date, in YYYY-MM-DD format or relative options ( 'today', 'yesterday' ) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.create_date | string |  |  
action_result.parameter.create_date_within | string |  |  
action_result.parameter.data_updated_after | string |  |  
action_result.parameter.email | string |  `email`  |  
action_result.parameter.expiration_date | string |  |  
action_result.parameter.first_seen_within | string |  |  
action_result.parameter.first_seen_since | string |  |  
action_result.parameter.status | string |  |  
action_result.parameter.tld | string |  |  
action_result.data.\*.domain | string |  `domain`  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.domain_risk.risk_score_string | string |  |  
action_result.data.\*.first_seen.count | numeric |  |  
action_result.data.\*.first_seen.value | string |  |  
action_result.data.\*.server_type.count | numeric |  |  
action_result.data.\*.server_type.value | string |  |  
action_result.data.\*.website_title.count | numeric |  |  
action_result.data.\*.website_title.value | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
action_result.summary | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'lookup domain'
Get all Iris Investigate data for a domain using the Iris Investigate API endpoint (required)

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain or comma-separated list of domains to query using the Iris Investigate API | string |  `url`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   failed  success 
action_result.parameter.domain | string |  `url`  `domain`  |  
action_result.data.\*.additional_whois_email.\*.count | numeric |  |  
action_result.data.\*.additional_whois_email.\*.value | string |  |  
action_result.data.\*.admin_contact.city.count | numeric |  |  
action_result.data.\*.admin_contact.city.value | string |  |  
action_result.data.\*.admin_contact.country.count | numeric |  |  
action_result.data.\*.admin_contact.country.value | string |  |  
action_result.data.\*.admin_contact.fax.count | numeric |  |  
action_result.data.\*.admin_contact.fax.value | string |  |  
action_result.data.\*.admin_contact.name.count | numeric |  |  
action_result.data.\*.admin_contact.name.value | string |  |  
action_result.data.\*.admin_contact.org.count | numeric |  |  
action_result.data.\*.admin_contact.org.value | string |  |  
action_result.data.\*.admin_contact.phone.count | numeric |  |  
action_result.data.\*.admin_contact.phone.value | string |  |  
action_result.data.\*.admin_contact.postal.count | numeric |  |  
action_result.data.\*.admin_contact.postal.value | string |  |  
action_result.data.\*.admin_contact.state.count | numeric |  |  
action_result.data.\*.admin_contact.state.value | string |  |  
action_result.data.\*.admin_contact.street.count | numeric |  |  
action_result.data.\*.admin_contact.street.value | string |  |  
action_result.data.\*.adsense.count | numeric |  |  
action_result.data.\*.adsense.value | string |  |  
action_result.data.\*.alexa | numeric |  |  
action_result.data.\*.billing_contact.city.count | numeric |  |  
action_result.data.\*.billing_contact.city.value | string |  |  
action_result.data.\*.billing_contact.country.count | numeric |  |  
action_result.data.\*.billing_contact.country.value | string |  |  
action_result.data.\*.billing_contact.fax.count | numeric |  |  
action_result.data.\*.billing_contact.fax.value | string |  |  
action_result.data.\*.billing_contact.name.count | numeric |  |  
action_result.data.\*.billing_contact.name.value | string |  |  
action_result.data.\*.billing_contact.org.count | numeric |  |  
action_result.data.\*.billing_contact.org.value | string |  |  
action_result.data.\*.billing_contact.phone.count | numeric |  |  
action_result.data.\*.billing_contact.phone.value | string |  |  
action_result.data.\*.billing_contact.postal.count | numeric |  |  
action_result.data.\*.billing_contact.postal.value | string |  |  
action_result.data.\*.billing_contact.state.count | numeric |  |  
action_result.data.\*.billing_contact.state.value | string |  |  
action_result.data.\*.billing_contact.street.count | numeric |  |  
action_result.data.\*.billing_contact.street.value | string |  |  
action_result.data.\*.create_date.count | numeric |  |  
action_result.data.\*.create_date.value | string |  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.email_domain.\*.count | numeric |  |  
action_result.data.\*.email_domain.\*.value | string |  |  
action_result.data.\*.expiration_date.count | numeric |  |  
action_result.data.\*.expiration_date.value | string |  |  
action_result.data.\*.first_seen.count | numeric |  |  
action_result.data.\*.first_seen.value | string |  |  
action_result.data.\*.google_analytics.count | numeric |  |  
action_result.data.\*.google_analytics.value | string |  |  
action_result.data.\*.ip.\*.address.count | numeric |  |  
action_result.data.\*.ip.\*.address.value | string |  |  
action_result.data.\*.ip.\*.asn.\*.count | numeric |  |  
action_result.data.\*.ip.\*.asn.\*.value | string |  |  
action_result.data.\*.ip.\*.country_code.count | numeric |  |  
action_result.data.\*.ip.\*.country_code.value | string |  |  
action_result.data.\*.ip.\*.isp.count | numeric |  |  
action_result.data.\*.ip.\*.isp.value | string |  |  
action_result.data.\*.mx.\*.domain.count | numeric |  |  
action_result.data.\*.mx.\*.domain.value | string |  |  
action_result.data.\*.mx.\*.host.count | numeric |  |  
action_result.data.\*.mx.\*.host.value | string |  |  
action_result.data.\*.mx.\*.ip.\*.count | numeric |  |  
action_result.data.\*.mx.\*.ip.\*.value | string |  |  
action_result.data.\*.name_server.\*.domain.count | numeric |  |  
action_result.data.\*.name_server.\*.domain.value | string |  |  
action_result.data.\*.name_server.\*.host.count | numeric |  |  
action_result.data.\*.name_server.\*.host.value | string |  |  
action_result.data.\*.name_server.\*.ip.\*.count | numeric |  |  
action_result.data.\*.name_server.\*.ip.\*.value | string |  |  
action_result.data.\*.redirect.count | numeric |  |  
action_result.data.\*.redirect.value | string |  |  
action_result.data.\*.redirect_domain.count | numeric |  |  
action_result.data.\*.redirect_domain.value | string |  |  
action_result.data.\*.registrant_contact.city.count | numeric |  |  
action_result.data.\*.registrant_contact.city.value | string |  |  
action_result.data.\*.registrant_contact.country.count | numeric |  |  
action_result.data.\*.registrant_contact.country.value | string |  |  
action_result.data.\*.registrant_contact.email.\*.value | string |  |  
action_result.data.\*.registrant_contact.email.\*.count | numeric |  |  
action_result.data.\*.registrant_contact.fax.count | numeric |  |  
action_result.data.\*.registrant_contact.fax.value | string |  |  
action_result.data.\*.registrant_contact.name.count | numeric |  |  
action_result.data.\*.registrant_contact.name.value | string |  |  
action_result.data.\*.registrant_contact.org.count | numeric |  |  
action_result.data.\*.registrant_contact.org.value | string |  |  
action_result.data.\*.registrant_contact.phone.count | numeric |  |  
action_result.data.\*.registrant_contact.phone.value | string |  |  
action_result.data.\*.registrant_contact.postal.count | numeric |  |  
action_result.data.\*.registrant_contact.postal.value | string |  |  
action_result.data.\*.registrant_contact.state.count | numeric |  |  
action_result.data.\*.registrant_contact.state.value | string |  |  
action_result.data.\*.registrant_contact.street.count | numeric |  |  
action_result.data.\*.registrant_contact.street.value | string |  |  
action_result.data.\*.registrant_name.count | numeric |  |  
action_result.data.\*.registrant_name.value | string |  |  
action_result.data.\*.registrant_org.count | numeric |  |  
action_result.data.\*.registrant_org.value | string |  |  
action_result.data.\*.registrar.count | numeric |  |  
action_result.data.\*.registrar.value | string |  |  
action_result.data.\*.server_type.count | numeric |  |  
action_result.data.\*.server_type.value | string |  |  
action_result.data.\*.soa_email.\*.count | numeric |  |  
action_result.data.\*.soa_email.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.alt_names.\*.count | numeric |  |  
action_result.data.\*.ssl_info.\*.alt_names.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.common_name.count | numeric |  |  
action_result.data.\*.ssl_info.\*.common_name.value | string |  |  
action_result.data.\*.ssl_info.\*.duration.count | numeric |  |  
action_result.data.\*.ssl_info.\*.duration.value | string |  |  
action_result.data.\*.ssl_info.\*.email.\*.count | numeric |  |  
action_result.data.\*.ssl_info.\*.email.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.hash.count | numeric |  |  
action_result.data.\*.ssl_info.\*.hash.value | string |  |  
action_result.data.\*.ssl_info.\*.issuer_common_name.count | numeric |  |  
action_result.data.\*.ssl_info.\*.issuer_common_name.value | string |  |  
action_result.data.\*.ssl_info.\*.not_after.count | numeric |  |  
action_result.data.\*.ssl_info.\*.not_after.value | string |  |  
action_result.data.\*.ssl_info.\*.not_before.count | numeric |  |  
action_result.data.\*.ssl_info.\*.not_before.value | string |  |  
action_result.data.\*.ssl_info.\*.organization.count | numeric |  |  
action_result.data.\*.ssl_info.\*.organization.value | string |  |  
action_result.data.\*.ssl_info.\*.subject.count | numeric |  |  
action_result.data.\*.ssl_info.\*.subject.value | string |  |  
action_result.data.\*.tags.\*.label | string |  |  
action_result.data.\*.tags.\*.scope | string |  |  
action_result.data.\*.tags.\*.tagged_at | string |  |  
action_result.data.\*.technical_contact.city.count | numeric |  |  
action_result.data.\*.technical_contact.city.value | string |  |  
action_result.data.\*.technical_contact.country.count | numeric |  |  
action_result.data.\*.technical_contact.country.value | string |  |  
action_result.data.\*.technical_contact.fax.count | numeric |  |  
action_result.data.\*.technical_contact.fax.value | string |  |  
action_result.data.\*.technical_contact.name.count | numeric |  |  
action_result.data.\*.technical_contact.name.value | string |  |  
action_result.data.\*.technical_contact.org.count | numeric |  |  
action_result.data.\*.technical_contact.org.value | string |  |  
action_result.data.\*.technical_contact.phone.count | numeric |  |  
action_result.data.\*.technical_contact.phone.value | string |  |  
action_result.data.\*.technical_contact.postal.count | numeric |  |  
action_result.data.\*.technical_contact.postal.value | string |  |  
action_result.data.\*.technical_contact.state.count | numeric |  |  
action_result.data.\*.technical_contact.state.value | string |  |  
action_result.data.\*.technical_contact.street.count | numeric |  |  
action_result.data.\*.technical_contact.street.value | string |  |  
action_result.data.\*.tld | string |  |  
action_result.summary | string |  |  
action_result.data.\*.website_title.count | numeric |  |  
action_result.data.\*.website_title.value | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'enrich domain'
Get all Iris Investigate data for a domain except counts using the high volume Iris Enrich API endpoint (if provisioned)

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain or comma-separated list of domains to query using the Iris Enrich API (if provisioned) | string |  `url`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   failed  success 
action_result.parameter.domain | string |  `url`  `domain`  |  
action_result.data.\*.additional_whois_email.\*.value | string |  |  
action_result.data.\*.admin_contact.city.value | string |  |  
action_result.data.\*.admin_contact.country.value | string |  |  
action_result.data.\*.admin_contact.fax.value | string |  |  
action_result.data.\*.admin_contact.name.value | string |  |  
action_result.data.\*.admin_contact.org.value | string |  |  
action_result.data.\*.admin_contact.phone.value | string |  |  
action_result.data.\*.admin_contact.postal.value | string |  |  
action_result.data.\*.admin_contact.state.value | string |  |  
action_result.data.\*.admin_contact.street.value | string |  |  
action_result.data.\*.adsense.value | string |  |  
action_result.data.\*.alexa | numeric |  |  
action_result.data.\*.billing_contact.city.value | string |  |  
action_result.data.\*.billing_contact.country.value | string |  |  
action_result.data.\*.billing_contact.fax.value | string |  |  
action_result.data.\*.billing_contact.name.value | string |  |  
action_result.data.\*.billing_contact.org.value | string |  |  
action_result.data.\*.billing_contact.phone.value | string |  |  
action_result.data.\*.billing_contact.postal.value | string |  |  
action_result.data.\*.billing_contact.state.value | string |  |  
action_result.data.\*.billing_contact.street.value | string |  |  
action_result.data.\*.create_date.value | string |  |  
action_result.data.\*.domain_risk.risk_score | numeric |  |  
action_result.data.\*.email_domain.\*.value | string |  |  
action_result.data.\*.expiration_date.value | string |  |  
action_result.data.\*.first_seen.value | string |  |  
action_result.data.\*.google_analytics.value | string |  |  
action_result.data.\*.ip.\*.address.value | string |  |  
action_result.data.\*.ip.\*.asn.\*.value | string |  |  
action_result.data.\*.ip.\*.country_code.value | string |  |  
action_result.data.\*.ip.\*.isp.value | string |  |  
action_result.data.\*.mx.\*.domain.value | string |  |  
action_result.data.\*.mx.\*.host.value | string |  |  
action_result.data.\*.mx.\*.ip.\*.value | string |  |  
action_result.data.\*.name_server.\*.domain.value | string |  |  
action_result.data.\*.name_server.\*.host.value | string |  |  
action_result.data.\*.name_server.\*.ip.\*.value | string |  |  
action_result.data.\*.redirect.value | string |  |  
action_result.data.\*.redirect_domain.value | string |  |  
action_result.data.\*.registrant_contact.city.value | string |  |  
action_result.data.\*.registrant_contact.country.value | string |  |  
action_result.data.\*.registrant_contact.email.\*.value | string |  |  
action_result.data.\*.registrant_contact.fax.value | string |  |  
action_result.data.\*.registrant_contact.name.value | string |  |  
action_result.data.\*.registrant_contact.org.value | string |  |  
action_result.data.\*.registrant_contact.phone.value | string |  |  
action_result.data.\*.registrant_contact.postal.value | string |  |  
action_result.data.\*.registrant_contact.state.value | string |  |  
action_result.data.\*.registrant_contact.street.value | string |  |  
action_result.data.\*.registrant_name.value | string |  |  
action_result.data.\*.registrant_org.value | string |  |  
action_result.data.\*.registrar.value | string |  |  
action_result.data.\*.server_type.value | string |  |  
action_result.data.\*.soa_email.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.alt_names.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.common_name.value | string |  |  
action_result.data.\*.ssl_info.\*.duration.value | string |  |  
action_result.data.\*.ssl_info.\*.email.\*.value | string |  |  
action_result.data.\*.ssl_info.\*.hash.value | string |  |  
action_result.data.\*.ssl_info.\*.issuer_common_name.value | string |  |  
action_result.data.\*.ssl_info.\*.not_after.value | string |  |  
action_result.data.\*.ssl_info.\*.not_before.value | string |  |  
action_result.data.\*.ssl_info.\*.organization.value | string |  |  
action_result.data.\*.ssl_info.\*.subject.value | string |  |  
action_result.data.\*.tags.\*.label | string |  |  
action_result.data.\*.tags.\*.scope | string |  |  
action_result.data.\*.tags.\*.tagged_at | string |  |  
action_result.data.\*.technical_contact.city.value | string |  |  
action_result.data.\*.technical_contact.country.value | string |  |  
action_result.data.\*.technical_contact.fax.value | string |  |  
action_result.data.\*.technical_contact.name.value | string |  |  
action_result.data.\*.technical_contact.org.value | string |  |  
action_result.data.\*.technical_contact.phone.value | string |  |  
action_result.data.\*.technical_contact.postal.value | string |  |  
action_result.data.\*.technical_contact.state.value | string |  |  
action_result.data.\*.technical_contact.street.value | string |  |  
action_result.data.\*.tld | string |  |  
action_result.data.\*.website_title.value | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'whois history'
Obtain historic whois records for a domain name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to query | string |  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.domain | string |  `domain`  |   splunk.com 
action_result.data.\*.history.\*.date | string |  |   2013-07-05 
action_result.data.\*.history.\*.is_private | numeric |  |   1 
action_result.data.\*.history.\*.whois.name_servers | string |  |   NS7.TEST.COM 
action_result.data.\*.history.\*.whois.record | string |  |   Registered through: Test.com, LLC (http://www.test.com)
   Domain Name: PHANTOMCYBER.COM
      Created on: 04-Jul-13
      Expires on: 04-Jul-14
      Last Updated on: 04-Jul-13

   Registrant:
   Domains By Proxy, LLC
   DomainsByProxy.com
   14747 N Northsight Blvd Suite 111, PMB 309
   Scottsdale, Arizona 85260
   United States

   Administrative Contact:
      Private, Registration  PHANTOMCYBER.COM@domainsbyproxy.com
      Domains By Proxy, LLC
      DomainsByProxy.com
      14747 N Northsight Blvd Suite 111, PMB 309
      Scottsdale, Arizona 85260
      United States
      (480) 624-2599      Fax -- (480) 624-2598

   Technical Contact:
      Private, Registration  PHANTOMCYBER.COM@domainsbyproxy.com
      Domains By Proxy, LLC
      DomainsByProxy.com
      14747 N Northsight Blvd Suite 111, PMB 309
      Scottsdale, Arizona 85260
      United States
      (480) 624-2599      Fax -- (480) 624-2598

   Domain servers in listed order:
      NS67.DOMAINCONTROL.COM
      NS68.DOMAINCONTROL.COM
 
action_result.data.\*.history.\*.whois.registrant | string |  |   Domains By Proxy, LLC 
action_result.data.\*.history.\*.whois.registration.created | string |  |   2013-07-04 
action_result.data.\*.history.\*.whois.registration.expires | string |  |   2014-07-04 
action_result.data.\*.history.\*.whois.registration.registrar | string |  |   TEST.COM, LLC 
action_result.data.\*.history.\*.whois.registration.statuses | string |  |   clientUpdateProhibited 
action_result.data.\*.history.\*.whois.registration.updated | string |  |   2013-07-04 
action_result.data.\*.history.\*.whois.server | string |  |   whois.test.com 
action_result.data.\*.record_count | numeric |  |   24 
action_result.summary | string |  |  
action_result.summary.record_count | numeric |  |   24 
action_result.message | string |  |   Record count: 24 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reverse whois'
Find domains based on terms in their Whois record

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**terms** |  required  | terms to query | string | 
**include_history** |  optional  | Include historical whois matches | boolean | 
**count_only** |  optional  | Only return count of matched records | boolean | 
**exclude_domains** |  optional  | Domain names with these words will be excluded from the result set. For exclusions of multiple terms, use the ( | ) character as a logical AND. | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   failed  success 
action_result.parameter.count_only | boolean |  |   False  True 
action_result.parameter.terms | string |  |   network.splunk.comm.$#@$@$  splunk.com  splunk.com.  splunk.com?  splunk.comm.$#@$@$  test.com 
action_result.parameter.include_history | boolean |  |   False  True 
action_result.parameter.exclude_domains | string |  |   splunk.com  test-domain.com 
action_result.data.\*.domain_count.current | numeric |  |   0 
action_result.data.\*.domain_count.historic | numeric |  |   0 
action_result.data.\*.domains | string |  `domain`  |  
action_result.data.\*.report_cost.current | numeric |  |   0 
action_result.data.\*.report_cost.historic | numeric |  |   0 
action_result.data.\*.report_price.current | numeric |  |   0 
action_result.data.\*.report_price.historic | numeric |  |   0 
action_result.summary | string |  |  
action_result.summary.total_domains | numeric |  `domain`  |   0 
action_result.message | string |  |   Parameter 'email' failed validation  Total domains: 0 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   0  1   

## action: 'whois domain'
Execute whois lookup on the given domain or IP

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to query | string |  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.domain | string |  `domain`  |   SPLUNK.COM 
action_result.data.\*.name_servers | string |  |   NS4.SPLUNK.US 
action_result.data.\*.parsed_whois.contacts.admin.city | string |  |   San Jose 
action_result.data.\*.parsed_whois.contacts.admin.country | string |  |   US 
action_result.data.\*.parsed_whois.contacts.admin.email | string |  `email`  |   idc@splunk.com 
action_result.data.\*.parsed_whois.contacts.admin.fax | string |  |    
action_result.data.\*.parsed_whois.contacts.admin.name | string |  |   Jhon Smith 
action_result.data.\*.parsed_whois.contacts.admin.org | string |  |   Splunk Inc. 
action_result.data.\*.parsed_whois.contacts.admin.phone | string |  |   866-434-1111 
action_result.data.\*.parsed_whois.contacts.admin.postal | string |  |   94086 
action_result.data.\*.parsed_whois.contacts.admin.state | string |  |   CA 
action_result.data.\*.parsed_whois.contacts.admin.street | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.city | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.country | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.email | string |  `email`  |    
action_result.data.\*.parsed_whois.contacts.billing.fax | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.name | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.org | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.phone | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.postal | string |  |    
action_result.data.\*.parsed_whois.contacts.billing.state | string |  |    
action_result.data.\*.parsed_whois.contacts.registrant.city | string |  |   San Jose 
action_result.data.\*.parsed_whois.contacts.registrant.country | string |  |   US 
action_result.data.\*.parsed_whois.contacts.registrant.email | string |  `email`  |   idc@splunk.com 
action_result.data.\*.parsed_whois.contacts.registrant.fax | string |  |    
action_result.data.\*.parsed_whois.contacts.registrant.name | string |  |   Jhon Smith 
action_result.data.\*.parsed_whois.contacts.registrant.org | string |  |   Splunk Inc 
action_result.data.\*.parsed_whois.contacts.registrant.phone | string |  |   866-434-9121 
action_result.data.\*.parsed_whois.contacts.registrant.postal | string |  |   94088 
action_result.data.\*.parsed_whois.contacts.registrant.state | string |  |   CA 
action_result.data.\*.parsed_whois.contacts.registrant.street | string |  |    
action_result.data.\*.parsed_whois.contacts.tech.city | string |  |   San Jose 
action_result.data.\*.parsed_whois.contacts.tech.country | string |  |   US 
action_result.data.\*.parsed_whois.contacts.tech.email | string |  `email`  |   idc@splunk.com 
action_result.data.\*.parsed_whois.contacts.tech.fax | string |  |    
action_result.data.\*.parsed_whois.contacts.tech.name | string |  |   Jhon smith 
action_result.data.\*.parsed_whois.contacts.tech.org | string |  |   Splunk Inc 
action_result.data.\*.parsed_whois.contacts.tech.phone | string |  |   861-111-1211 
action_result.data.\*.parsed_whois.contacts.tech.postal | string |  |   94088 
action_result.data.\*.parsed_whois.contacts.tech.state | string |  |   CA 
action_result.data.\*.parsed_whois.contacts.tech.street | string |  |    
action_result.data.\*.parsed_whois.created_date | string |  |   2006-06-20T12:49:22+00:00 
action_result.data.\*.parsed_whois.domain | string |  `domain`  |   SPLUNK.COM 
action_result.data.\*.parsed_whois.expired_date | string |  |   2019-06-20T12:49:22+00:00 
action_result.data.\*.parsed_whois.name_servers | string |  |   ns4.splunk.com 
action_result.data.\*.parsed_whois.other_properties.dnssec | string |  |   unsignedDelegation 
action_result.data.\*.parsed_whois.other_properties.domain_domain_status | string |  `domain`  |   ok https://icann.org/epp#ok 
action_result.data.\*.parsed_whois.other_properties.registry_domain_id | string |  `domain`  |   491960245_DOMAIN_COM-VRSN 
action_result.data.\*.parsed_whois.registrar.abuse_contact_email | string |  `email`  |   abuse@net4.com 
action_result.data.\*.parsed_whois.registrar.abuse_contact_phone | string |  |   911204323500 
action_result.data.\*.parsed_whois.registrar.iana_id | string |  |   1007 
action_result.data.\*.parsed_whois.registrar.name | string |  |   Net 4 Test Limited 
action_result.data.\*.parsed_whois.registrar.url | string |  `url`  |   http://www.net4.us/ 
action_result.data.\*.parsed_whois.registrar.whois_server | string |  `host name`  |   whois.net4domains.com 
action_result.data.\*.parsed_whois.statuses | string |  |  
action_result.data.\*.parsed_whois.updated_date | string |  |   2018-06-21T08:29:46+00:00 
action_result.data.\*.record_source | string |  |   SPLUNK.COM 
action_result.data.\*.registrant | string |  |   Splunk Inc 
action_result.data.\*.registration.created | string |  |   2006-06-20 
action_result.data.\*.registration.expires | string |  |   2019-06-20 
action_result.data.\*.registration.registrar | string |  |   Net 4 Test Limited 
action_result.data.\*.registration.statuses | string |  |   ok 
action_result.data.\*.registration.updated | string |  |   2018-06-21 
action_result.data.\*.whois.date | string |  |   2018-10-03 
action_result.data.\*.whois.record | string |  |   Domain Name: SPLUNK.COM
Registry Domain ID: 491960245_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.net4domains.com
Registrar URL: http://www.net4.in/
Updated Date: 2018-06-21T08:29:46Z
Creation Date: 2006-06-20T12:49:22Z
Registrar Registration Expiration Date: 2019-06-20T12:49:22Z
Registrar: Net 4 India Limited
Registrar IANA ID: 1007
Registrar Abuse Contact Email: abuse@net4.com
Registrar Abuse Contact Phone: +1.9661231111
Domain Domain Status: ok https://icann.org/epp#ok
Registry Registrant ID: 
Registrant Name: Jhon Smith
Registrant Organization: Splunk Inc
Registrant Street: ,
Registrant City: San Jose
Registrant State/Province: CA
Registrant Postal Code: 94088
Registrant Country: US
Registrant Phone: +91.2612789500
Registrant Phone Ext:
Registrant Fax: 
Registrant Fax Ext:
Registrant Email: idc@splunk.com
Registry Admin ID: 
Admin Name: Jhon Smith
Admin Organization: Splunk Inc
Admin Street: ,
Admin City: San Jose
Admin State/Province: CA
Admin Postal Code: 94088
Admin Country: US
Admin Phone: +1.9661231111
Admin Phone Ext:
Admin Fax: 
Admin Fax Ext:
Admin Email: idc@splunk.com
Registry Tech ID: 
Tech Name: Jhon Smith
Tech Organization: Splunk Inc
Tech Street: ,
Tech City: San Jose
Tech State/Province: CA
Tech Postal Code: 94088
Tech Country: IN
Tech Phone: +1.9661231111
Tech Phone Ext:
Tech Fax: 
Tech Fax Ext:
Tech Email: idc@splunk.com
Name Server: NS1.SPLUNK.COM
Name Server: NS2.SPLUNK.COM
Name Server: NS3.SPLUNK.COM
Name Server: NS4.SPLUNK.COM
DNSSEC: unsignedDelegation
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
 
action_result.summary | string |  |  
action_result.summary.city | string |  |   San Jose 
action_result.summary.country | string |  |   US 
action_result.summary.organization | string |  |   Splunk Inc 
action_result.message | string |  |   Organization: Splunk Inc. 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'whois ip'
Execute whois lookup on the given IP address

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP to query | string |  `ip`  `ipv6` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.ip | string |  `ip`  `ipv6`  |   1.1.1.1  203.88.139.34  10.0.1.20 
action_result.data.\*.parsed_whois.contacts.\*.abuse_mailbox | string |  `email`  |   test@test.net 
action_result.data.\*.parsed_whois.contacts.\*.address | string |  |   Australia  India  90292 
action_result.data.\*.parsed_whois.contacts.\*.address.0 | string |  |  
action_result.data.\*.parsed_whois.contacts.\*.address.1 | string |  |  
action_result.data.\*.parsed_whois.contacts.\*.address.2 | string |  |  
action_result.data.\*.parsed_whois.contacts.\*.address.3 | string |  |  
action_result.data.\*.parsed_whois.contacts.\*.contact_keys.abuse | string |  |   IANA-IP-ARIN 
action_result.data.\*.parsed_whois.contacts.\*.contact_keys.admin | string |  |   AH256-AP 
action_result.data.\*.parsed_whois.contacts.\*.contact_keys.noc | string |  |  
action_result.data.\*.parsed_whois.contacts.\*.contact_keys.tech | string |  |   AH256-AP  IANA-IP-ARIN 
action_result.data.\*.parsed_whois.contacts.\*.country | string |  |     in  us 
action_result.data.\*.parsed_whois.contacts.\*.created_date | string |  |    
action_result.data.\*.parsed_whois.contacts.\*.email | string |  `email`  |   research@test.net  test@splunk.com 
action_result.data.\*.parsed_whois.contacts.\*.fax | string |  |   61738583199  912612789501 
action_result.data.\*.parsed_whois.contacts.\*.id | string |  |   IRT-APNICRANDNET-AU  NI23-AP  IANA 
action_result.data.\*.parsed_whois.contacts.\*.mnt_keys.by | string |  |   MAINT-APNIC-AP  MAINT-IN-YOU 
action_result.data.\*.parsed_whois.contacts.\*.mnt_keys.ref | string |  |   APNIC-HM 
action_result.data.\*.parsed_whois.contacts.\*.name | string |  |     NOC IQARA  Internet Assigned Numbers Authority 
action_result.data.\*.parsed_whois.contacts.\*.other.auth | string |  |   # Filtered 
action_result.data.\*.parsed_whois.contacts.\*.phone | string |  |   61738583188  912612789500  13103015820 
action_result.data.\*.parsed_whois.contacts.\*.ref | string |  `url`  |     https://rdap.arin.net/registry/entity/IANA 
action_result.data.\*.parsed_whois.contacts.\*.remarks | string |  |   ----------------------------------------- 
action_result.data.\*.parsed_whois.contacts.\*.source | string |  |   APNIC   
action_result.data.\*.parsed_whois.contacts.\*.type | string |  |   irt  person  organization 
action_result.data.\*.parsed_whois.contacts.\*.updated_date | string |  |   2011-09-22T03:53:02+00:00  2010-04-07T10:10:28+00:00  2012-08-31T00:00:00 
action_result.data.\*.parsed_whois.networks.\*.asn | string |  |    
action_result.data.\*.parsed_whois.networks.\*.contact_keys.abuse | string |  |  
action_result.data.\*.parsed_whois.networks.\*.contact_keys.admin | string |  |   AR302-AP  SG135-AP 
action_result.data.\*.parsed_whois.networks.\*.contact_keys.noc | string |  |  
action_result.data.\*.parsed_whois.networks.\*.contact_keys.org | string |  |   IANA 
action_result.data.\*.parsed_whois.networks.\*.contact_keys.tech | string |  |   AR302-AP  NI23-AP 
action_result.data.\*.parsed_whois.networks.\*.country | string |  |   au  in   
action_result.data.\*.parsed_whois.networks.\*.created_date | string |  |    
action_result.data.\*.parsed_whois.networks.\*.customer | string |  |    
action_result.data.\*.parsed_whois.networks.\*.descr | string |  `url`  |   Research prefix for APNIC Labs  YOU Telecom India Pvt Ltd  http://datatracker.ietf.org/doc/rfc1918 
action_result.data.\*.parsed_whois.networks.\*.id | string |  |     NET-10-0-0-0-1 
action_result.data.\*.parsed_whois.networks.\*.mnt_keys.by | string |  |   APNIC-HM  MAINT-IN-YOU 
action_result.data.\*.parsed_whois.networks.\*.mnt_keys.irt | string |  |   IRT-APNICRANDNET-AU 
action_result.data.\*.parsed_whois.networks.\*.mnt_keys.routes | string |  |   MAINT-AU-APNIC-GM85-AP 
action_result.data.\*.parsed_whois.networks.\*.name | string |  |   APNIC-LABS  YOUTELE  PRIVATE-ADDRESS-ABLK-RFC1918-IANA-RESERVED 
action_result.data.\*.parsed_whois.networks.\*.org | string |  |   ORG-ARAD1-AP    Internet Assigned Numbers Authority (IANA) 
action_result.data.\*.parsed_whois.networks.\*.parent | string |  |     () 
action_result.data.\*.parsed_whois.networks.\*.parent_id | string |  |    
action_result.data.\*.parsed_whois.networks.\*.range.cidr | string |  |   1.1.1.0/24  203.88.128.0/20  10.0.0.0/8 
action_result.data.\*.parsed_whois.networks.\*.range.count | numeric |  |   256  4096  16777216 
action_result.data.\*.parsed_whois.networks.\*.range.from | string |  `ip`  `ipv6`  |   1.1.1.0  203.88.128.0  10.0.0.0 
action_result.data.\*.parsed_whois.networks.\*.range.to | string |  `ip`  `ipv6`  |   1.1.1.255  203.88.143.255  10.255.255.255 
action_result.data.\*.parsed_whois.networks.\*.ref | string |  `url`  |     https://rdap.arin.net/registry/ip/10.0.0.0 
action_result.data.\*.parsed_whois.networks.\*.remarks | string |  |   --------------- 
action_result.data.\*.parsed_whois.networks.\*.source | string |  |   APNIC   
action_result.data.\*.parsed_whois.networks.\*.status | string |  |   ASSIGNED PORTABLE  ASSIGNED NON-PORTABLE  IANA Special Use 
action_result.data.\*.parsed_whois.networks.\*.updated_date | string |  |   2018-03-30T01:51:28+00:00  2009-12-10T05:27:14+00:00  2013-08-30T00:00:00 
action_result.data.\*.parsed_whois.routes.\*.asn | string |  |   AS13335  AS18207 
action_result.data.\*.parsed_whois.routes.\*.country | string |  |    
action_result.data.\*.parsed_whois.routes.\*.created_date | string |  |    
action_result.data.\*.parsed_whois.routes.\*.descr | string |  |   6 Cordelia St  Splunk Inc. 
action_result.data.\*.parsed_whois.routes.\*.id | string |  |   1.1.1.0/24  203.88.128.0/24 
action_result.data.\*.parsed_whois.routes.\*.mnt_keys.by | string |  |   MAINT-AU-APNIC-GM85-AP  MAINT-IN-YOU 
action_result.data.\*.parsed_whois.routes.\*.mnt_keys.lower | string |  |   MAINT-IN-YOU 
action_result.data.\*.parsed_whois.routes.\*.mnt_keys.routes | string |  |   MAINT-IN-YOU 
action_result.data.\*.parsed_whois.routes.\*.name | string |  |    
action_result.data.\*.parsed_whois.routes.\*.org | string |  |    
action_result.data.\*.parsed_whois.routes.\*.ref | string |  |    
action_result.data.\*.parsed_whois.routes.\*.source | string |  |   APNIC 
action_result.data.\*.parsed_whois.routes.\*.status | string |  |    
action_result.data.\*.parsed_whois.routes.\*.updated_date | string |  |   2018-03-16T16:58:06+00:00  2011-12-03T11:08:14+00:00 
action_result.data.\*.record_source | string |  `ip`  `ipv6`  |   1.1.1.1  203.88.128.214  10.3.88.37 
action_result.data.\*.registrant | string |  |   ORG-ARAD1-AP  YOUTELE  Internet Assigned Numbers Authority (IANA) 
action_result.data.\*.source | string |  |   APNIC  ARIN 
action_result.data.\*.whois.date | string |  |   2018-10-23  2018-10-07 
action_result.data.\*.whois.record | string |  |   inetnum:        1.1.1.0 - 1.1.1.255
netname:        APNIC-LABS
descr:          APNIC and Cloudflare DNS Resolver project
descr:          Routed globally by AS13335/Cloudflare
descr:          Research prefix for APNIC Labs
country:        AU
org:            ORG-ARAD1-AP
admin-c:        AR302-AP
tech-c:         AR302-AP
mnt-by:         APNIC-HM
mnt-routes:     MAINT-AU-APNIC-GM85-AP
mnt-irt:        IRT-APNICRANDNET-AU
status:         ASSIGNED PORTABLE
remarks:        ---------------
remarks:        All Cloudflare abuse reporting can be done via
remarks:        resolver-abuse@cloudflare.com
remarks:        ---------------
last-modified:  2018-03-30T01:51:28Z
source:         APNIC

irt:            IRT-APNICRANDNET-AU
address:        PO Box 3646
address:        South Brisbane, QLD 4101
address:        Australia
e-mail:         abuse@apnic.net
abuse-mailbox:  abuse@apnic.net
admin-c:        AR302-AP
tech-c:         AR302-AP
auth:           # Filtered
mnt-by:         MAINT-AU-APNIC-GM85-AP
last-modified:  2011-09-22T03:53:02Z
source:         APNIC

organisation:   ORG-ARAD1-AP
org-name:       APNIC Research and Development
country:        AU
address:        6 Cordelia St
phone:          +61-7-38583100
fax-no:         +61-7-38583199
e-mail:         helpdesk@apnic.net
mnt-ref:        APNIC-HM
mnt-by:         APNIC-HM
last-modified:  2017-10-11T01:28:39Z
source:         APNIC

role:           APNIC RESEARCH
address:        PO Box 3646
address:        South Brisbane, QLD 4101
address:        Australia
country:        AU
phone:          +61-7-3858-3188
fax-no:         +61-7-3858-3199
e-mail:         research@apnic.net
nic-hdl:        AR302-AP
tech-c:         AH256-AP
admin-c:        AH256-AP
mnt-by:         MAINT-APNIC-AP
last-modified:  2018-04-04T04:26:04Z
source:         APNIC

route:          1.1.1.0/24
origin:         AS13335
descr:          APNIC Research and Development
                6 Cordelia St
mnt-by:         MAINT-AU-APNIC-GM85-AP
last-modified:  2018-03-16T16:58:06Z
source:         APNIC
  inetnum:        203.88.128.0 - 203.88.143.255
netname:        YOUTELE
descr:          Splunk Inc
country:        US
admin-c:        SG135-AP
tech-c:         NI23-AP
status:         ASSIGNED NON-PORTABLE
mnt-by:         MAINT-IN-YOU
last-modified:  2009-12-10T05:27:14Z
source:         APNIC

person:         NOC IQARA
nic-hdl:        NI23-AP
e-mail:         network@SPLUNK.COM
address:        Splunk Inc.
address:        Iqara Center
address:        San-Jose
address:        San jose
phone:          +1-261-2789500
fax-no:         +1-261-2789501
country:        US
mnt-by:         MAINT-US-YOU
last-modified:  2010-04-07T10:10:28Z
source:         APNIC

person:         SRIDHAR G
nic-hdl:        SG135-AP
e-mail:         test@splunk.com
remarks:        -----------------------------------------
remarks:        send abuse and spam report to
remarks:        test@splunk.com or test@splunk.com
remarks:        -----------------------------------------
address:        Splunk Inc.
address:        Millenium Arcade, 2nd floor
address:        San Jose
address:        CA
address:        US
phone:          +91-261-2789500
fax-no:         +91-261-2789501
country:        IN
mnt-by:         MAINT-IN-YOU
last-modified:  2010-05-13T04:40:07Z
source:         APNIC

route:          203.88.128.0/24
descr:          Splunk Inc.
origin:         AS18207
mnt-lower:      MAINT-IN-YOU
mnt-routes:     MAINT-IN-YOU
mnt-by:         MAINT-IN-YOU
last-modified:  2011-12-03T11:08:14Z
source:         APNIC
  NetRange:       10.0.0.0 - 10.255.255.255
CIDR:           10.0.0.0/8
NetName:        PRIVATE-ADDRESS-ABLK-RFC1918-IANA-RESERVED
NetHandle:      NET-10-0-0-0-1
Parent:          ()
NetType:        IANA Special Use
OriginAS:       
Organization:   Internet Assigned Numbers Authority (IANA)
RegDate:        
Updated:        2013-08-30
Comment:        These addresses are in use by many millions of independently operated networks, which might be as small as a single computer connected to a home gateway, and are automatically configured in hundreds of millions of devices.  They are only intended for use within a private context  and traffic that needs to cross the Internet will need to use a different, unique address.
Comment:        
Comment:        These addresses can be used by anyone without any need to coordinate with IANA or an Internet registry.  The traffic from these addresses does not come from ICANN or IANA.  We are not the source of activity you may see on logs or in e-mail records.  Please refer to http://www.iana.org/abuse/answers
Comment:        
Comment:        These addresses were assigned by the IETF, the organization that develops Internet protocols, in the Best Current Practice document, RFC 1918 which can be found at:
Comment:        http://datatracker.ietf.org/doc/rfc1918
Ref:            https://rdap.arin.net/registry/ip/10.0.0.0

OrgName:        Internet Assigned Numbers Authority
OrgId:          IANA
Address:        12025 Waterfront Drive
Address:        Suite 300
City:           Los Angeles
StateProv:      CA
PostalCode:     90292
Country:        US
RegDate:        
Updated:        2012-08-31
Ref:            https://rdap.arin.net/registry/entity/IANA

OrgAbuseHandle: IANA-IP-ARIN
OrgAbuseName:   ICANN
OrgAbusePhone:  +1-310-301-5820 
OrgAbuseEmail:  abuse@iana.org
OrgAbuseRef:    https://rdap.arin.net/registry/entity/IANA-IP-ARIN

OrgTechHandle: IANA-IP-ARIN
OrgTechName:   ICANN
OrgTechPhone:  +1-310-301-5820 
OrgTechEmail:  abuse@iana.org
OrgTechRef:    https://rdap.arin.net/registry/entity/IANA-IP-ARIN
 
action_result.summary.city | string |  |  
action_result.summary.country | string |  |     in  us 
action_result.summary.organization | string |  |   ORG-ARAD1-AP  YOUTELE  Internet Assigned Numbers Authority (IANA) 
action_result.message | string |  |   Organization: ORG-ARAD1-AP, City: None, Country:   Organization: YOUTELE, City: None, Country: in  Organization: Internet Assigned Numbers Authority (IANA), City: None, Country: us 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'recent domains'
Search for new domains containing a word

Type: **investigate**  
Read only: **True**

If the <b>days_back</b> parameter is not set, the data for the current day is returned, else data of the particular day in the past is retrieved.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  required  | Word to look for in a domain name | string | 
**days_back** |  optional  | Number of days back to search for (1-6) | string | 
**status** |  optional  | Status of the domain | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.days_back | string |  |  
action_result.parameter.query | string |  |   domain  test4.test@splunk.com  splunk.com  splunk.com.test 
action_result.parameter.status | string |  |  
action_result.data.\*.alerts.\*.domain | string |  `domain`  |   0000.domains 
action_result.data.\*.alerts.\*.status | string |  |   new 
action_result.data.\*.date | string |  |   2018-10-25  2018-10-24 
action_result.data.\*.limit | numeric |  |   3000 
action_result.data.\*.new | boolean |  |   False  True 
action_result.data.\*.on-hold | boolean |  |   False  True 
action_result.data.\*.query | string |  `email`  |   domain  test1@splunk.com  splunk.com  splunk.com.test 
action_result.data.\*.total | numeric |  |   306  0 
action_result.data.\*.utf8 | boolean |  |   False  True 
action_result.summary | string |  |  
action_result.summary.total_domains | numeric |  `domain`  |   306  0 
action_result.message | string |  |   Total domains: 306  Total domains: 0 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'hosting history'
Obtain changes to registrar, IP, etc

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to query | string |  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success 
action_result.parameter.domain | string |  `domain`  |   splunk.com 
action_result.data.\*.domain_name | string |  `domain`  |   splunk.com 
action_result.data.\*.ip_history.\*.action | string |  |   N 
action_result.data.\*.ip_history.\*.action_in_words | string |  |   New 
action_result.data.\*.ip_history.\*.actiondate | string |  |   2004-06-12  2013-07-19  2006-06-22 
action_result.data.\*.ip_history.\*.domain | string |  `domain`  |   SPLUNK.COM 
action_result.data.\*.ip_history.\*.post_ip | string |  `ip`  `ipv6`  |   216.239.51.107  184.168.221.62  202.71.128.225 
action_result.data.\*.ip_history.\*.pre_ip | string |  `ip`  `ipv6`  |  
action_result.data.\*.nameserver_history.\*.action | string |  |   T  N 
action_result.data.\*.nameserver_history.\*.action_in_words | string |  |   Transfer  New 
action_result.data.\*.nameserver_history.\*.actiondate | string |  |   2004-03-27  2013-07-05  2006-04-25 
action_result.data.\*.nameserver_history.\*.domain | string |  `domain`  |   SPLUNK.COM 
action_result.data.\*.nameserver_history.\*.post_mns | string |  |   Splunk.com 
action_result.data.\*.nameserver_history.\*.pre_mns | string |  |   Splunk.com   
action_result.data.\*.registrar_history.\*.date_created | string |  |   1995-08-13  2013-07-04  2006-06-20 
action_result.data.\*.registrar_history.\*.date_expires | string |  |   2003-08-12  2014-07-04  2007-06-20 
action_result.data.\*.registrar_history.\*.date_lastchecked | string |  |   2003-06-28  2013-07-16  2006-06-22 
action_result.data.\*.registrar_history.\*.date_updated | string |  |   2002-06-26  2013-07-04  2006-06-20 
action_result.data.\*.registrar_history.\*.domain | string |  `domain`  |   SPLUNK.COM 
action_result.data.\*.registrar_history.\*.registrar | string |  |   Test.com 
action_result.data.\*.registrar_history.\*.registrartag | string |  |   Test.COM  Test Software Inc 
action_result.summary | string |  |  
action_result.summary.ip_history_count | numeric |  |   280  5  3 
action_result.summary.nameserver_history_count | numeric |  |   2  10 
action_result.summary.registrar_history_count | numeric |  |   3  1  2 
action_result.message | string |  |   Ip history count: 280, Registrar history count: 3, Nameserver history count: 2  Ip history count: 5, Registrar history count: 1, Nameserver history count: 2  Ip history count: 3, Registrar history count: 2, Nameserver history count: 10 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'configure scheduled playbooks'
Run on initial setup to configure the optional monitoring playbooks. This action creates a custom list to manage the playbook scheduling and run status

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   failed  success 
action_result.data.\* | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'on poll'
Execute scheduled playbooks based on the set interval(mins) in 'domaintools_scheduled_playbooks' custom list. Smaller intervals will result in more accurate schedules

Type: **ingest**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output