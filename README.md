# Patent Attic

[Search Patent Attic](https://coolcode.ca/patentattic/) by application number, applicant, title or IPC classification. The default collection is CIPO’s weekly pre-grant queue. A separate collection preserves 22 selected Canadian technology publications and their drawings.

<!-- coolcode:guide -->
Search 3016489 to inspect the Gearing System application in the November 17, 2026 pre-grant edition, or G01S to find applications in its IPC subclass. Each queue entry identifies the final fee date, applicant, classification and queue position. For the historical collection choose Selected technology publications and search Autofocus.
<!-- /coolcode:guide -->

The November 17 workbook contained 14,556 distinct applications. CIPO updates the queue as applications are processed, so a later edition may drop a number. Check the linked Canadian Patents Database record for later grants and status. A queue position is specific to that edition. The date displayed on a queue card is the final fee receipt date. Dates in the separate curated collection are publication dates.

## Build and reproduce

Install `requirements.txt` and run `python3 scripts/build.py`. The build downloads the spreadsheet linked from [CIPO’s weekly pre-grant page](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/pre-grant-patent-applications-xlsx), validates application identifiers and relevant fields, and preserves the internal edition date, exact workbook URL and SHA-256 in `dist/manifest.json`. English titles fall back to the French title when necessary. Applicant names and classifications follow the workbook. The published interface searches locally after loading. The weekly Pages workflow keeps the previous deployment if the source cannot be read or validated.

The historical collection is independently maintained in `data/curated.json`. Its titles, dates and publication numbers were checked against the individual published documents. Its topic labels are editorial.

## Data

- [CIPO Canadian Patents Database](https://cipo-opic.ic.gc.ca/opic-cipo/cpd/eng/introduction.html)
- [CIPO IP Horizons bulk data](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/canadian-intellectual-property-statistics/ip-horizons-download-intellectual-property-data)
- [Canadian Intellectual Property Data terms](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/terms-and-conditions-use-canadian-intellectual-property-data)

Contains data licensed by Her Majesty the Queen in right of Canada, as represented by the Minister of Industry, the minister responsible for the administration of the Canadian Intellectual Property Office.
