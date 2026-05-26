import re

import frappe
from frappe import _

NIP_WEIGHTS = [6, 5, 7, 2, 3, 4, 5, 6, 7]


def validate_customer(doc, method=None):
	validate_nip(doc)


def validate_nip(doc):
	if doc.territory not in ("Polska", "Poland"):
		return

	if doc.customer_type != "Company":
		return

	if not doc.tax_id:
		return

	nip = re.sub(r"[\s\-]", "", doc.tax_id)

	if not nip.isdigit() or len(nip) != 10:
		frappe.msgprint(
			_("NIP '{0}' is invalid — must consist of exactly 10 digits.").format(doc.tax_id),
			indicator="orange",
			alert=True,
		)
		return

	checksum = sum(int(nip[i]) * NIP_WEIGHTS[i] for i in range(9)) % 11

	if checksum == 10 or checksum != int(nip[9]):
		frappe.msgprint(
			_("NIP '{0}' is invalid (incorrect checksum).").format(doc.tax_id),
			indicator="orange",
			alert=True,
		)
