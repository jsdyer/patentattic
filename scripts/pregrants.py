"""Read the public CIPO pre-grant workbook and retain its search fields."""
from datetime import date, datetime, timezone
import hashlib
from html.parser import HTMLParser
from io import BytesIO
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from openpyxl import load_workbook

SOURCE = "https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/patents/pre-grant-patent-applications-xlsx"


class WorkbookLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href", "")
        url = urljoin(SOURCE, href)
        parsed = urlsplit(url)
        filename = parsed.path.rsplit("/", 1)[-1].lower()
        if (tag == "a" and parsed.scheme == "https"
                and parsed.netloc == urlsplit(SOURCE).netloc
                and filename.endswith(".xlsx")
                and re.search(r"pre[-_]grants?", filename)):
            self.urls.append(url)


def download(url, limit):
    with urlopen(Request(url, headers={"User-Agent": "CoolCode Patent Attic"}), timeout=90) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Source exceeds expected size")
    return data


def parse_workbook(raw, url):
    workbook = load_workbook(BytesIO(raw), read_only=True, data_only=True)
    columns = {}
    updated = None
    rows = []
    seen = set()
    for cells in workbook["Pre-Grant Report"].values:
        if not columns:
            for cell in cells:
                if isinstance(cell, str) and cell.startswith("Données / Data"):
                    updated = date.fromisoformat(re.search(r"\d{4}-\d{2}-\d{2}", cell)[0]).isoformat()
            if "Numéro de demande - Application Number" in cells:
                columns = {str(value).strip().split(" - ")[-1]: i for i, value in enumerate(cells)}
            continue
        def value(key):
            return cells[columns[key]]
        number = value("Application Number")
        if number is None:
            continue
        number = str(number)
        if not re.fullmatch(r"\d{7}", number) or number in seen:
            raise ValueError("Unexpected or duplicate application number")
        seen.add(number)
        title = value("English Title") or value("French Title")
        fee = value("Final Fee Received Date")
        ipc = value("Classification")
        if fee is not None and not isinstance(fee, (date, datetime)):
            raise ValueError("Invalid final fee date")
        # CIPO sometimes publishes an identifier and queue position with blank
        # descriptive fields. Preserve that row without inventing its metadata.
        text = lambda item: str(item).strip() if item is not None else ""
        rows.append([number, text(title), text(value("Applicants")), text(ipc),
                     fee.isoformat()[:10] if fee is not None else "",
                     int(value("Queue")), value("Statut / Status") or ""])
    workbook.close()
    if not updated or not rows:
        raise ValueError("Missing source date or pre-grant applications")
    return dict(updated=updated, count=len(rows), source=SOURCE, workbook=url,
                sha256=hashlib.sha256(raw).hexdigest(), rows=rows)


def fetch_edition():
    parser = WorkbookLinks()
    parser.feed(download(SOURCE, 2_000_000).decode())
    if len(set(parser.urls)) != 1:
        raise ValueError("Expected one English CIPO pre-grant workbook")
    url = parser.urls[0]
    edition = parse_workbook(download(url, 32_000_000), url)
    edition["retrieved_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return edition
