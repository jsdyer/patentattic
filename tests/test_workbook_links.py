"""Keep recognizing CIPO's dated workbook as its filename changes."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from pregrants import SOURCE, WorkbookLinks, parse_workbook
from io import BytesIO
from openpyxl import Workbook
from urllib.parse import urljoin


class WorkbookLinkTests(unittest.TestCase):
    def test_old_and_current_cipo_names(self):
        for name in (
            "opic_brevets_preoctrois_hebdomadaires-cipo_patents_weekly_pre-grants-2026-11-13.xlsx",
            "Weekly_Pre_Grant_Completed_2026-11-24.xlsx",
        ):
            with self.subTest(name=name):
                parser = WorkbookLinks()
                href = "/site/canadian-intellectual-property-office/sites/default/files/documents/" + name
                parser.feed(f'<a href="{href}">Download XLSX version</a>')
                self.assertEqual(parser.urls, [urljoin(SOURCE, href)])

    def test_rejects_other_hosts_formats_and_unrelated_workbooks(self):
        parser = WorkbookLinks()
        for href in (
            "https://example.com/pre-grants.xlsx",
            "http://ised-isde.canada.ca/pre-grants.xlsx",
            "/pre-grants.pdf",
            "/unrelated.xlsx",
        ):
            parser.feed(f'<a href="{href}">Download</a>')
        self.assertEqual(parser.urls, [])

    def workbook(self, fee=None):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Pre-Grant Report"
        sheet.append(["Données / Data : 2026-11-24 08:00:00 AM"])
        sheet.append(["Numéro de demande - Application Number", "Queue", "English Title",
                      "French Title", "Applicants", "Classification", "Final Fee Received Date", "Statut / Status"])
        sheet.append([2983327, 13947, None, None, None, None, fee, None])
        output = BytesIO()
        workbook.save(output)
        return output.getvalue()

    def test_retains_identifiers_with_blank_source_metadata(self):
        edition = parse_workbook(self.workbook(), "https://example.com/source.xlsx")
        self.assertEqual(edition["rows"], [["2983327", "", "", "", "", 13947, ""]])
        self.assertEqual(edition["count"], 1)

    def test_rejects_invalid_nonempty_fee_date(self):
        with self.assertRaisesRegex(ValueError, "Invalid final fee date"):
            parse_workbook(self.workbook("not a date"), "https://example.com/source.xlsx")
