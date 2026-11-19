import json
from pathlib import Path

import frappe


def polish_tax_id_fields(
	insert_after: str, party_type_field: str | None = None, include_pesel: bool = True
) -> list[dict]:
	"""Polish tax identifier fields (REGON, KRS, PESEL, VAT Tax Status).

	When ``party_type_field`` is given, REGON/KRS are shown only for non-individuals
	and PESEL only for individuals (sole proprietors). ``include_pesel=False`` drops
	PESEL entirely (e.g. Company, which identifies the taxpayer by NIP).
	"""
	company_only = individual_only = None
	if party_type_field:
		company_only = f"eval:doc.{party_type_field}!='Individual'"
		individual_only = f"eval:doc.{party_type_field}=='Individual'"

	fields = [
		{
			"fieldname": "polish_tax_ids_section",
			"fieldtype": "Section Break",
			"insert_after": insert_after,
			"label": "Polish Tax Identifiers",
		},
		{
			"depends_on": company_only,
			"fieldname": "regon",
			"fieldtype": "Data",
			"insert_after": "polish_tax_ids_section",
			"label": "REGON",
		},
		{
			"depends_on": company_only,
			"fieldname": "krs",
			"fieldtype": "Data",
			"insert_after": "regon",
			"label": "KRS",
		},
		{
			"depends_on": individual_only,
			"fieldname": "pesel",
			"fieldtype": "Data",
			"insert_after": "krs",
			"label": "PESEL",
		},
		{
			"fieldname": "column_break_polish_tax",
			"fieldtype": "Column Break",
			"insert_after": "pesel" if include_pesel else "krs",
		},
		{
			"fieldname": "vat_tax_status",
			"fieldtype": "Data",
			"insert_after": "column_break_polish_tax",
			"label": "VAT Tax Status",
		},
	]

	if not include_pesel:
		fields = [field for field in fields if field["fieldname"] != "pesel"]

	return [{key: value for key, value in field.items() if value is not None} for field in fields]


CUSTOM_FIELDS = {
	"Customer": polish_tax_id_fields("settings_tab", "customer_type"),
	"Supplier": polish_tax_id_fields("settings_tab", "supplier_type"),
	"Company": polish_tax_id_fields("date_of_establishment", include_pesel=False),
	"Sales Invoice": [
		{
			"fieldname": "service_delivery_date",
			"fieldtype": "Date",
			"hide_days": 1,
			"insert_after": "due_date",
			"label": "Service Delivery Date",
			"translatable": 1,
		},
	],
}

STANDARD_DOCUMENTS = [
	"erpnextpl_community/print_format/faktura_vat/faktura_vat.json",
	"erpnextpl_community/print_format/wydanie_zamówienia/wydanie_zamówienia.json",
	"erpnextpl_community/print_format/pasek_wynagrodzenia_timesheet/pasek_wynagrodzenia_timesheet.json",
	"erpnextpl_community/email_template/dunning_reminder/dunning_reminder.json",
	"erpnextpl_community/email_template/sales_invoice_notification/sales_invoice_notification.json",
	"erpnextpl_community/notification/delayed_deliveries_of_to_customers/delayed_deliveries_of_to_customers.json",
	"erpnextpl_community/notification/low_stock_levels/low_stock_levels.json",
	"erpnextpl_community/notification/overdue_liabilities_(purchase_invoices)/overdue_liabilities_(purchase_invoices).json",
	"erpnextpl_community/notification/overdue_receivables/overdue_receivables.json",
	"erpnextpl_community/notification/pending_goods_receipts/pending_goods_receipts.json",
	"erpnextpl_community/notification/pending_releases_from_warehouse/pending_releases_from_warehouse.json",
	"erpnextpl_community/notification/purchase_invoice_due_date/purchase_invoice_due_date.json",
	"erpnextpl_community/notification/sales_invoice_created/sales_invoice_created.json",
	"erpnextpl_community/notification/sales_invoice_due_date/sales_invoice_due_date.json",
	"erpnextpl_community/notification/sales_invoice_notification/sales_invoice_notification.json",
	"erpnextpl_community/notification/sales_order_ready_for_fulfillment/sales_order_ready_for_fulfillment.json",
	"erpnextpl_community/notification/todo_assigned/todo_assigned.json",
]

FAKTURA_VAT_HTML_REPLACEMENTS = (
	(
		"{{ frappe.utils.fmt_float(row.qty, 2) }}",
		"{{ (row.qty or 0) | round(2) }}",
	),
	(
		"doc.in_words or money_in_words(gross_total, doc.currency)",
		"doc.in_words or frappe.utils.money_in_words(gross_total, doc.currency)",
	),
	(
		"doc.in_words or frappe.utils.frappe.utils.money_in_words(gross_total, doc.currency)",
		"doc.in_words or frappe.utils.money_in_words(gross_total, doc.currency)",
	),
)


def execute():
	create_custom_fields()
	create_standard_documents()


def create_custom_fields(doctypes: list[str] | None = None) -> None:
	"""Create missing Custom Fields, optionally only for the given doctypes."""
	for doctype, fields in CUSTOM_FIELDS.items():
		if doctypes is not None and doctype not in doctypes:
			continue

		for field in fields:
			name = f"{doctype}-{field['fieldname']}"
			if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
				continue

			doc = frappe.get_doc(
				{
					"doctype": "Custom Field",
					"dt": doctype,
					"name": name,
					"module": "ERPNextPL Community",
					**field,
				}
			)
			doc.insert(ignore_permissions=True, ignore_mandatory=True)


def create_standard_documents(migrate_existing: bool = True) -> None:
	app_path = Path(frappe.get_app_path("erpnextpl_community"))

	for relative_path in STANDARD_DOCUMENTS:
		data = json.loads((app_path / relative_path).read_text(encoding="utf-8"))

		if frappe.db.exists(data["doctype"], data["name"]):
			if migrate_existing and data["doctype"] == "Print Format" and data["name"] == "Faktura VAT":
				migrate_faktura_vat_html(data["name"])
			continue

		if data["doctype"] == "Notification":
			data["enabled"] = 0

		frappe.get_doc(data).insert(
			ignore_permissions=True,
			ignore_links=True,
			ignore_mandatory=True,
			ignore_if_duplicate=True,
		)


def migrate_faktura_vat_html(print_format_name: str) -> None:
	print_format_html = frappe.db.get_value("Print Format", print_format_name, "html") or ""
	migrated_html = apply_faktura_vat_html_replacements(print_format_html)

	if migrated_html != print_format_html:
		frappe.db.set_value("Print Format", print_format_name, "html", migrated_html)


def apply_faktura_vat_html_replacements(html: str) -> str:
	for old, new in FAKTURA_VAT_HTML_REPLACEMENTS:
		html = html.replace(old, new)

	return html
