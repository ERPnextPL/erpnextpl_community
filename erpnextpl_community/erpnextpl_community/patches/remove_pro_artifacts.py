import frappe


def execute():
	delete_doc_if_exists("Notification", "Sales invoice issued in KSeF")
	delete_doc_if_exists("DocType", "MT940 Profile")
	delete_doc_if_exists("DocType", "ERPNextPL Settings")
	delete_doc_if_exists("Custom Field", "Bank-mt940_profile")

	for property_setter in frappe.get_all(
		"Property Setter",
		filters={
			"doc_type": "Sales Order",
			"field_name": "disable_rounded_total",
			"property": "default",
		},
		pluck="name",
	):
		delete_doc_if_exists("Property Setter", property_setter)


def delete_doc_if_exists(doctype: str, name: str) -> None:
	if frappe.db.exists(doctype, name):
		frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)
