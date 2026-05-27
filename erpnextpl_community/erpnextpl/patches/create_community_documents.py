import json
from pathlib import Path

import frappe

CUSTOM_FIELDS = {
	"Customer": [
		{
			"fieldname": "polish_tax_ids_section",
			"fieldtype": "Section Break",
			"insert_after": "tax_withholding_category",
			"label": "Polish Tax Identifiers",
		},
		{
			"depends_on": "eval:doc.customer_type!='Individual'",
			"fieldname": "regon",
			"fieldtype": "Data",
			"insert_after": "polish_tax_ids_section",
			"label": "REGON",
		},
		{
			"depends_on": "eval:doc.customer_type!='Individual'",
			"fieldname": "krs",
			"fieldtype": "Data",
			"insert_after": "regon",
			"label": "KRS",
		},
		{
			"depends_on": "eval:doc.customer_type=='Individual'",
			"fieldname": "pesel",
			"fieldtype": "Data",
			"insert_after": "krs",
			"label": "PESEL",
		},
		{
			"fieldname": "column_break_polish_tax",
			"fieldtype": "Column Break",
			"insert_after": "pesel",
		},
		{
			"fieldname": "vat_tax_status",
			"fieldtype": "Data",
			"insert_after": "column_break_polish_tax",
			"label": "VAT Tax Status",
		},
	],
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
	"erpnextpl/print_format/faktura_vat/faktura_vat.json",
	"erpnextpl/print_format/wydanie_zamówienia/wydanie_zamówienia.json",
	"erpnextpl/email_template/dunning_reminder/dunning_reminder.json",
	"erpnextpl/email_template/sales_invoice_notification/sales_invoice_notification.json",
	"erpnextpl/notification/delayed_deliveries_of_to_customers/delayed_deliveries_of_to_customers.json",
	"erpnextpl/notification/low_stock_levels/low_stock_levels.json",
	"erpnextpl/notification/overdue_liabilities_(purchase_invoices)/overdue_liabilities_(purchase_invoices).json",
	"erpnextpl/notification/overdue_receivables/overdue_receivables.json",
	"erpnextpl/notification/pending_goods_receipts/pending_goods_receipts.json",
	"erpnextpl/notification/pending_releases_from_warehouse/pending_releases_from_warehouse.json",
	"erpnextpl/notification/purchase_invoice_due_date/purchase_invoice_due_date.json",
	"erpnextpl/notification/sales_invoice_created/sales_invoice_created.json",
	"erpnextpl/notification/sales_invoice_due_date/sales_invoice_due_date.json",
	"erpnextpl/notification/sales_invoice_notification/sales_invoice_notification.json",
	"erpnextpl/notification/sales_order_ready_for_fulfillment/sales_order_ready_for_fulfillment.json",
	"erpnextpl/notification/todo_assigned/todo_assigned.json",
]


def execute():
	create_custom_fields()
	create_standard_documents()


def create_custom_fields() -> None:
	for doctype, fields in CUSTOM_FIELDS.items():
		for field in fields:
			name = f"{doctype}-{field['fieldname']}"
			if frappe.db.exists("Custom Field", name):
				continue

			doc = frappe.get_doc(
				{
					"doctype": "Custom Field",
					"dt": doctype,
					"name": name,
					"module": "erpnextpl",
					**field,
				}
			)
			doc.insert(ignore_permissions=True, ignore_mandatory=True)


def create_standard_documents() -> None:
	app_path = Path(frappe.get_app_path("erpnextpl_community"))

	for relative_path in STANDARD_DOCUMENTS:
		data = json.loads((app_path / relative_path).read_text(encoding="utf-8"))
		if frappe.db.exists(data["doctype"], data["name"]):
			continue

		if data["doctype"] == "Notification":
			data["enabled"] = 0

		frappe.get_doc(data).insert(
			ignore_permissions=True,
			ignore_links=True,
			ignore_mandatory=True,
			ignore_if_duplicate=True,
		)
