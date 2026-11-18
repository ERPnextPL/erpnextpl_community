import sys
import types
import unittest
from itertools import pairwise
from unittest.mock import MagicMock, patch

# Frappe nie jest dostępne poza środowiskiem bench — tworzymy stub modułu
_frappe_stub = types.ModuleType("frappe")
_frappe_stub.msgprint = MagicMock()
_frappe_stub._ = lambda x: x
sys.modules.setdefault("frappe", _frappe_stub)

from erpnextpl_community.erpnextpl_community.patches import (
	add_polish_tax_fields_to_supplier_and_company,
	create_community_documents,
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


def _fields_by_name(doctype):
	return {field["fieldname"]: field for field in CUSTOM_FIELDS[doctype]}


class TestPolishTaxFields(unittest.TestCase):
	def test_all_parties_have_polish_tax_fields(self):
		"""Customer, Supplier i Company mają ten sam zestaw pól podatkowych."""
		for doctype in ("Customer", "Supplier", "Company"):
			with self.subTest(doctype=doctype):
				fieldnames = [field["fieldname"] for field in CUSTOM_FIELDS[doctype]]
				self.assertEqual(fieldnames, POLISH_TAX_FIELDNAMES)

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
				with self.subTest(doctype=doctype, field=fieldname):
					self.assertEqual(fields[fieldname]["fieldtype"], fieldtype)
					self.assertEqual(fields[fieldname].get("label"), label)

	def test_section_placement(self):
		"""Sekcja jest wstawiana w odpowiednim miejscu formularza."""
		expected = {
			"Customer": "tax_withholding_category",
			"Supplier": "tax_withholding_category",
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


if __name__ == "__main__":
	unittest.main()
