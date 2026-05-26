import sys
import types
import unittest
from unittest.mock import MagicMock

# Frappe nie jest dostępne poza środowiskiem bench — tworzymy stub modułu
_frappe_stub = types.ModuleType("frappe")
_frappe_stub.msgprint = MagicMock()
_frappe_stub._ = lambda x: x
sys.modules.setdefault("frappe", _frappe_stub)

# Upewniamy się, że moduł customer jest przeładowany ze stubem frappe
if "erpnextpl.customer" in sys.modules:
	del sys.modules["erpnextpl.customer"]


def _make_customer(territory="Poland", customer_type="Company", tax_id=""):
	doc = MagicMock()
	doc.territory = territory
	doc.customer_type = customer_type
	doc.tax_id = tax_id
	return doc


class TestValidateNip(unittest.TestCase):
	def setUp(self):
		import frappe

		frappe.msgprint = MagicMock()

	def _validate(self, **kwargs):
		from erpnextpl.customer import validate_nip

		validate_nip(_make_customer(**kwargs))

	def _assert_msgprint_called_with(self, fragment, **kwargs):
		import frappe

		self._validate(**kwargs)
		frappe.msgprint.assert_called_once()
		msg = frappe.msgprint.call_args[0][0]
		self.assertIn(fragment, msg)

	def _assert_no_msgprint(self, **kwargs):
		import frappe

		self._validate(**kwargs)
		frappe.msgprint.assert_not_called()

	# --- warunki wejścia ---

	def test_non_polish_territory_skips_validation(self):
		"""Dla terytorium innego niż Polska/Poland walidacja jest pomijana."""
		self._assert_no_msgprint(territory="Germany", tax_id="ssss")

	def test_individual_customer_type_skips_validation(self):
		"""Dla osób fizycznych (Individual) walidacja jest pomijana."""
		self._assert_no_msgprint(customer_type="Individual", tax_id="ssss")

	def test_empty_tax_id_passes_without_warning(self):
		"""Brak NIP nie powoduje ostrzeżenia."""
		self._assert_no_msgprint(tax_id="")

	# --- nieprawidłowy format ---

	def test_non_digit_nip_shows_format_warning(self):
		"""NIP zawierający litery wywołuje ostrzeżenie o złym formacie."""
		self._assert_msgprint_called_with("10 digits", tax_id="ssssss2wawsd")

	def test_too_short_nip_shows_format_warning(self):
		"""NIP krótszy niż 10 cyfr wywołuje ostrzeżenie."""
		self._assert_msgprint_called_with("10 digits", tax_id="12345")

	# --- błędna suma kontrolna ---

	def test_invalid_checksum_nip_shows_warning(self):
		"""NIP z błędną sumą kontrolną wywołuje ostrzeżenie."""
		self._assert_msgprint_called_with("checksum", tax_id="1234567890")

	# --- poprawny NIP ---

	def test_valid_nip_passes_without_warning(self):
		"""Poprawny NIP (8971729222) nie wywołuje ostrzeżenia."""
		self._assert_no_msgprint(tax_id="8971729222")

	def test_valid_nip_with_dashes_passes(self):
		"""NIP z myślnikami (897-172-92-22) jest akceptowany po oczyszczeniu."""
		self._assert_no_msgprint(tax_id="897-172-92-22")

	def test_valid_nip_with_spaces_passes(self):
		"""NIP ze spacjami (897 172 92 22) jest akceptowany po oczyszczeniu."""
		self._assert_no_msgprint(tax_id="897 172 92 22")

	# --- obsługa obu wartości terytorium ---

	def test_territory_polska_triggers_validation(self):
		"""Terytorium 'Polska' również uruchamia walidację."""
		self._assert_msgprint_called_with("10 digits", territory="Polska", tax_id="ssss")

	def test_territory_poland_english_triggers_validation(self):
		"""Terytorium 'Poland' uruchamia walidację."""
		self._assert_msgprint_called_with("10 digits", territory="Poland", tax_id="ssss")
