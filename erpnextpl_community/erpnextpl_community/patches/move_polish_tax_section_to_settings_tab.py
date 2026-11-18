import frappe

# Values are frozen here on purpose: this one-time migration must not change
# behaviour when CUSTOM_FIELDS is edited later.
SECTION_FIELDNAME = "polish_tax_ids_section"
PREVIOUS_ANCHOR = "tax_withholding_category"
NEW_ANCHOR = "settings_tab"


def execute():
	# Move the Polish Tax Identifiers section on existing sites to the top of the
	# Settings tab. Only sections still at the previous default are moved, so a
	# placement changed by an administrator is left alone.
	for doctype in ("Customer", "Supplier"):
		name = frappe.db.get_value(
			"Custom Field",
			{"dt": doctype, "fieldname": SECTION_FIELDNAME, "insert_after": PREVIOUS_ANCHOR},
		)
		if not name:
			continue

		frappe.db.set_value("Custom Field", name, "insert_after", NEW_ANCHOR)
		frappe.clear_cache(doctype=doctype)
