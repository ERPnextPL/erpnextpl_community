import frappe

from erpnextpl_community.erpnextpl_community.patches.create_community_documents import CUSTOM_FIELDS

# Earlier releases placed the section after this field (in the Tax tab).
PREVIOUS_ANCHOR = "tax_withholding_category"


def execute():
	# Move the Polish Tax Identifiers section on existing sites to the anchor used
	# for fresh installs. Only sections still at the previous default are moved, so
	# a placement changed by an administrator is left alone.
	for doctype in ("Customer", "Supplier"):
		section = next(f for f in CUSTOM_FIELDS[doctype] if f["fieldname"] == "polish_tax_ids_section")
		name = frappe.db.get_value(
			"Custom Field",
			{"dt": doctype, "fieldname": "polish_tax_ids_section", "insert_after": PREVIOUS_ANCHOR},
		)
		if not name:
			continue

		frappe.db.set_value("Custom Field", name, "insert_after", section["insert_after"])
		frappe.clear_cache(doctype=doctype)
