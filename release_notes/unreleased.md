**Unreleased**
* All Iris Investigate and Iris Enrich queries now support batch lookups of up to 100 comma-separated domain inputs
* Added support for additional Iris fields: “first seen”, “server type”, and “website title”
* Pivot action adds support for additional operators: “create date within”, “first seen within”, and “first seen since”
* Added pagination on pivot responses (returns up to 5000 domains, sorted by highest risk)
* “Lookup Domain” action displays and adds outbound links to pivot in Iris Investigate when a domain has up to 500 connected domains on a data point
* Added support for proxies
* Minor UI improvements
* Updated python libraries