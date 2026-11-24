#!/usr/bin/env python3
"""Build the browser catalogue from individually verified Canadian publications."""
from datetime import date
import json
from pathlib import Path
import re
import shutil

from pregrants import fetch_edition

ROOT = Path(__file__).resolve().parent.parent
CIPO = "https://cipo-opic.ic.gc.ca/opic-cipo/cpd/eng/introduction.html"
IP_HORIZONS = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/canadian-intellectual-property-statistics/ip-horizons-download-intellectual-property-data"
LICENCE = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/terms-and-conditions-use-canadian-intellectual-property-data"
ATTRIBUTION = (
    "Contains data licensed by Her Majesty the Queen in right of Canada, as represented by the Minister of Industry, "
    "the minister responsible for the administration of the Canadian Intellectual Property Office."
)


def row(item):
    publication = item["id"]
    match = re.fullmatch(r"CA(\d{7})(A1|C)", publication)
    if not match:
        raise ValueError(f"Invalid Canadian publication number: {publication}")
    number, kind = match.groups()
    published = date.fromisoformat(item["date"])
    title = item["title"]
    if not title.strip():
        raise ValueError(f"Missing title for {publication}")
    category = item["topic"]
    author = item.get("applicant")
    publication_type = "Published application" if kind == "A1" else "Patent grant"
    summary = author or publication_type
    decade = f"{published.year // 10 * 10}s"
    cipo_item = f"https://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/{number}/summary.html"
    google = f"https://patents.google.com/patent/{publication}/en"
    return {
        "title": title, "date": published.isoformat(), "kicker": f"{category} / {publication_type}",
        "summary": summary, "highlight": publication, "a": category, "b": publication_type, "c": decade,
        "keywords": f"{publication} {number} CA {number} {kind} Canadian patent {author or ''}",
        "fields": {
            "Publication": publication, "CIPO number": number, "Publication date": published.isoformat(),
            "Document kind": publication_type, "Topic": category, "Original applicant as listed": author,
        },
        "links": [
            {"label": "Publication and drawings", "url": google},
            {"label": "Official CIPO record", "url": cipo_item},
            {"label": "Open Canadian patent search", "url": CIPO},
        ],
    }


def main():
    source = json.loads((ROOT / "data/curated.json").read_text())
    records = [row(item) for item in source["records"]]
    if len({r["highlight"] for r in records}) != len(records) or not records:
        raise ValueError("Expected unique Canadian publications")
    catalog = {
        "slug": "patentattic", "coverage": f"{len(records)} selected Canadian publications", "updated": source["checked"],
        "method": "Titles, document kinds and publication dates were checked against published Canadian documents. "
                  "Topic tags are editorial. The public IP Horizons bulk host returned a service error at validation, "
                  "so this release uses the checked individual records. " + ATTRIBUTION,
        "facets": ["Topic", "Publication type", "Decade"], "examples": ["Optical", "Autofocus", "Neural network", "BlackBerry"],
        "sources": [
            {"label": "Canadian Patents Database", "url": CIPO},
            {"label": "CIPO IP Horizons", "url": IP_HORIZONS},
            {"label": "Canadian IP data licence", "url": LICENCE},
        ],
        "records": records,
    }
    edition = fetch_edition()
    dist = ROOT / "dist"
    shutil.copytree(ROOT / "web", dist, dirs_exist_ok=True)
    (dist / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")))
    (dist / "pregrants.json").write_text(json.dumps(edition, ensure_ascii=False, separators=(",", ":")))
    (dist / "manifest.json").write_text(json.dumps({
        "date": edition["updated"], "retrieved_at": edition["retrieved_at"], "count": edition["count"], "curated": len(records),
        "source": edition["workbook"], "sha256": edition["sha256"]
    }, indent=2))
    print(f"CIPO pre-grant applications: {edition['count']} as of {edition['updated']}")
    print(f"Patent Attic: {len(records)} Canadian publications")


if __name__ == "__main__":
    main()
