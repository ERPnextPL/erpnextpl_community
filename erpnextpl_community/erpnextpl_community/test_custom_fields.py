import json
import re
import sys
import types
import unittest
from itertools import pairwise
from pathlib import Path
from unittest.mock import MagicMock, patch

# Frappe nie jest dostępne poza środowiskiem bench — tworzymy stub modułu
_frappe_stub = types.ModuleType("frappe")
_frappe_stub.msgprint = MagicMock()
_frappe_stub._ = lambda x: x
sys.modules.setdefault("frappe", _frappe_stub)

from erpnextpl_community import install
from erpnextpl_community.erpnextpl_community.patches import (
	add_polish_tax_fields_to_supplier_and_company,
	create_community_documents,
	create_polish_banks,
	move_polish_tax_section_to_settings_tab,
)
from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	CUSTOM_FIELDS,
)

POLISH_TAX_FIELDNAMES = [
	"polish_tax_ids_section",
	"regon",
	"krs",
	"pesel",
	"column_break_polish_tax",
	"vat_tax_status",
]
COMPANY_TAX_FIELDNAMES = [f for f in POLISH_TAX_FIELDNAMES if f != "pesel"]


def _fields_by_name(doctype):
	return {field["fieldname"]: field for field in CUSTOM_FIELDS[doctype]}


class TestPolishTaxFields(unittest.TestCase):
	def test_all_parties_have_polish_tax_fields(self):
		"""Customer i Supplier mają pełny zestaw pól, Company bez PESEL."""
		expected = {
			"Customer": POLISH_TAX_FIELDNAMES,
			"Supplier": POLISH_TAX_FIELDNAMES,
			"Company": COMPANY_TAX_FIELDNAMES,
		}
		for doctype, fieldnames_expected in expected.items():
			with self.subTest(doctype=doctype):
				fieldnames = [field["fieldname"] for field in CUSTOM_FIELDS[doctype]]
				self.assertEqual(fieldnames, fieldnames_expected)

	def test_company_has_no_pesel(self):
		"""Company identyfikuje podatnika NIP-em — PESEL nie jest potrzebny."""
		self.assertNotIn("pesel", _fields_by_name("Company"))
		self.assertEqual(_fields_by_name("Company")["column_break_polish_tax"]["insert_after"], "krs")

	def test_field_types_and_labels(self):
		"""Typy pól i etykiety są takie same dla wszystkich DocType."""
		expected = {
			"polish_tax_ids_section": ("Section Break", "Polish Tax Identifiers"),
			"regon": ("Data", "REGON"),
			"krs": ("Data", "KRS"),
			"pesel": ("Data", "PESEL"),
			"column_break_polish_tax": ("Column Break", None),
			"vat_tax_status": ("Data", "VAT Tax Status"),
		}
		for doctype in ("Customer", "Supplier", "Company"):
			fields = _fields_by_name(doctype)
			for fieldname, (fieldtype, label) in expected.items():
				if fieldname not in fields:
					continue
				with self.subTest(doctype=doctype, field=fieldname):
					self.assertEqual(fields[fieldname]["fieldtype"], fieldtype)
					self.assertEqual(fields[fieldname].get("label"), label)

	def test_section_placement(self):
		"""Sekcja jest wstawiana w odpowiednim miejscu formularza."""
		expected = {
			"Customer": "settings_tab",
			"Supplier": "settings_tab",
			"Company": "date_of_establishment",
		}
		for doctype, insert_after in expected.items():
			with self.subTest(doctype=doctype):
				section = _fields_by_name(doctype)["polish_tax_ids_section"]
				self.assertEqual(section["insert_after"], insert_after)

	def test_fields_are_chained(self):
		"""Każde pole jest wstawiane po poprzednim, w stałej kolejności."""
		for doctype in ("Customer", "Supplier", "Company"):
			fields = CUSTOM_FIELDS[doctype]
			for previous, current in pairwise(fields):
				with self.subTest(doctype=doctype, field=current["fieldname"]):
					self.assertEqual(current["insert_after"], previous["fieldname"])

	def test_customer_depends_on_customer_type(self):
		fields = _fields_by_name("Customer")
		self.assertEqual(fields["regon"]["depends_on"], "eval:doc.customer_type!='Individual'")
		self.assertEqual(fields["krs"]["depends_on"], "eval:doc.customer_type!='Individual'")
		self.assertEqual(fields["pesel"]["depends_on"], "eval:doc.customer_type=='Individual'")

	def test_supplier_depends_on_supplier_type(self):
		fields = _fields_by_name("Supplier")
		self.assertEqual(fields["regon"]["depends_on"], "eval:doc.supplier_type!='Individual'")
		self.assertEqual(fields["krs"]["depends_on"], "eval:doc.supplier_type!='Individual'")
		self.assertEqual(fields["pesel"]["depends_on"], "eval:doc.supplier_type=='Individual'")

	def test_company_fields_are_always_visible(self):
		"""Company nie ma pola typu podmiotu — wszystkie pola są zawsze widoczne."""
		for field in CUSTOM_FIELDS["Company"]:
			with self.subTest(field=field["fieldname"]):
				self.assertNotIn("depends_on", field)


class TestAddPolishTaxFieldsPatch(unittest.TestCase):
	def test_patch_only_touches_supplier_and_company(self):
		"""Patch nie przywraca pól usuniętych z innych DocType (np. Customer)."""
		frappe_mock = MagicMock()
		frappe_mock.db.exists.return_value = False

		with patch.object(create_community_documents, "frappe", frappe_mock):
			add_polish_tax_fields_to_supplier_and_company.execute()

		created_doctypes = {call.args[0]["dt"] for call in frappe_mock.get_doc.call_args_list}
		self.assertEqual(created_doctypes, {"Supplier", "Company"})

	def test_patch_skips_existing_fields(self):
		"""Istniejące pola nie są tworzone ponownie ani nadpisywane (idempotentność)."""
		frappe_mock = MagicMock()
		frappe_mock.db.exists.return_value = True

		with patch.object(create_community_documents, "frappe", frappe_mock):
			add_polish_tax_fields_to_supplier_and_company.execute()

		frappe_mock.get_doc.assert_not_called()
		checked = {call.args[1]["dt"] for call in frappe_mock.db.exists.call_args_list}
		self.assertEqual(checked, {"Supplier", "Company"})


class TestMovePolishTaxSectionPatch(unittest.TestCase):
	def _run(self, existing):
		"""existing: {doctype: Custom Field name or None} for sections at the old anchor."""
		frappe_mock = MagicMock()
		frappe_mock.db.get_value.side_effect = lambda _dt, filters: existing.get(filters["dt"])

		with patch.object(move_polish_tax_section_to_settings_tab, "frappe", frappe_mock):
			move_polish_tax_section_to_settings_tab.execute()

		return frappe_mock

	def test_moves_section_still_at_previous_anchor(self):
		"""Sekcja w starym domyślnym miejscu trafia na górę zakładki Ustawienia."""
		frappe_mock = self._run({"Customer": "Customer-polish_tax_ids_section"})

		frappe_mock.db.set_value.assert_called_once_with(
			"Custom Field", "Customer-polish_tax_ids_section", "insert_after", "settings_tab"
		)
		frappe_mock.clear_cache.assert_called_once_with(doctype="Customer")

	def test_leaves_section_moved_by_admin(self):
		"""Sekcja przeniesiona ręcznie (inne insert_after) nie jest ruszana."""
		frappe_mock = self._run({})

		frappe_mock.db.set_value.assert_not_called()

	def test_only_looks_for_previous_anchor(self):
		frappe_mock = self._run({})

		for call in frappe_mock.db.get_value.call_args_list:
			self.assertEqual(call.args[1]["insert_after"], "tax_withholding_category")
		self.assertEqual(
			{call.args[1]["dt"] for call in frappe_mock.db.get_value.call_args_list},
			{"Customer", "Supplier"},
		)


class TestAfterInstall(unittest.TestCase):
	def test_runs_all_setup_steps(self):
		"""Świeża instalacja dostaje pola, dokumenty, banki i język polski."""
		with (
			patch.object(install, "create_custom_fields") as fields,
			patch.object(install, "create_standard_documents") as documents,
			patch.object(create_polish_banks, "execute") as banks,
			patch.object(install, "frappe") as frappe_mock,
		):
			frappe_mock.db.exists.return_value = True
			install.after_install()

		fields.assert_called_once_with()
		documents.assert_called_once_with(migrate_existing=False)
		banks.assert_called_once_with()
		frappe_mock.db.set_value.assert_called_once_with("Language", "pl", "enabled", 1)


class TestStandardDocumentsByFrappeVersion(unittest.TestCase):
	CHROME = "Pasek Wynagrodzenia - Timesheet"
	WKHTML = "Pasek Wynagrodzenia - Timesheet (wkhtmltopdf)"

	def _checked_names(self, version):
		app_path = Path(create_community_documents.__file__).parents[2]
		with patch.object(create_community_documents, "frappe") as frappe_mock:
			frappe_mock.__version__ = version
			frappe_mock.get_app_path.return_value = str(app_path)
			frappe_mock.db.exists.return_value = False
			create_community_documents.create_standard_documents(migrate_existing=False)
		return [call.args[0]["name"] for call in frappe_mock.get_doc.call_args_list]

	def test_frappe_15_skips_chrome_print_format(self):
		names = self._checked_names("15.80.0")
		self.assertIn(self.WKHTML, names)
		self.assertNotIn(self.CHROME, names)

	def test_frappe_16_installs_both_print_formats(self):
		names = self._checked_names("16.0.0")
		self.assertIn(self.WKHTML, names)
		self.assertIn(self.CHROME, names)

	def test_frappe_17_skips_wkhtmltopdf_print_format(self):
		names = self._checked_names("17.0.0-dev")
		self.assertIn(self.CHROME, names)
		self.assertNotIn(self.WKHTML, names)

	def test_unsupported_format_is_disabled_when_it_exists(self):
		app_path = Path(create_community_documents.__file__).parents[2]
		with patch.object(create_community_documents, "frappe") as frappe_mock:
			frappe_mock.__version__ = "15.80.0"
			frappe_mock.get_app_path.return_value = str(app_path)
			frappe_mock.db.exists.return_value = True
			create_community_documents.create_standard_documents(migrate_existing=False)
		frappe_mock.db.set_value.assert_any_call("Print Format", self.CHROME, "disabled", 1)

	def test_wkhtmltopdf_format_has_no_unsupported_css(self):
		path = (
			Path(create_community_documents.__file__).parents[1]
			/ "print_format/pasek_wynagrodzenia_timesheet_wkhtmltopdf"
			/ "pasek_wynagrodzenia_timesheet_wkhtmltopdf.json"
		)
		data = json.loads(path.read_text(encoding="utf-8"))
		self.assertEqual(data["pdf_generator"], "wkhtmltopdf")
		for unsupported in (r"display\s*:\s*(inline-)?(flex|grid)", r"linear-gradient", r"grid-template"):
			self.assertIsNone(re.search(unsupported, data["html"], re.I), unsupported)


if __name__ == "__main__":
	unittest.main()
