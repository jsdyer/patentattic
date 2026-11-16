# Patent Attic

Search a small collection of Canadian patent publications in computing, photography, networks, electronics and photonics. Search by title, publication number, topic or original applicant. Filter by topic, decade, and publication kind. Each result links to the publication copy, its drawings where available, and the CIPO record or search.

The 22 titles, publication numbers and dates are verified against individual Canadian public patent publications indexed by Google Patents. The original CIPO lookup is available separately. The publication kind distinguishes an application publication (A1) from a grant publication (C), while both can have subsequent changes in official status. Topic labels are assigned for discovery.

CIPO's IP Horizons listing and its licensing notice were available at validation. The tested official bulk archive ZIP downloads returned HTTP 503, so this edition intentionally uses a curated research subset. No bulk download, outside service, or account is required in the publication workflow.

## Build

Run `python3 scripts/build.py` and serve `dist/`. The build validates publication identifiers and dates. Search, filters, record details and CSV exports work locally after loading the catalogue. Add individually verified publications to `data/curated.json` and update its check date. There is no scheduled refresh.

## Data

- [CIPO Canadian Patents Database](https://cipo-opic.ic.gc.ca/opic-cipo/cpd/eng/introduction.html)
- [CIPO IP Horizons bulk data](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/canadian-intellectual-property-statistics/ip-horizons-download-intellectual-property-data)
- [Canadian Intellectual Property Data terms](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/terms-and-conditions-use-canadian-intellectual-property-data)

Contains data licensed by Her Majesty the Queen in right of Canada, as represented by the Minister of Industry, the minister responsible for the administration of the Canadian Intellectual Property Office.
