import frappe
from frappe import _
from frappe.utils import getdate


def validate_sales_invoice(doc, method=None):
	validate_service_delivery_date(doc)
	set_due_date_from_posting(doc)
	validate_due_date_not_before_posting(doc)


def validate_service_delivery_date(doc):
	if not doc.get("service_delivery_date"):
		doc.set("service_delivery_date", doc.posting_date)


def set_due_date_from_posting(doc):
	if not doc.get("due_date"):
		doc.set("due_date", doc.posting_date)


def validate_due_date_not_before_posting(doc):
	if doc.get("due_date") and getdate(doc.due_date) < getdate(doc.posting_date):
		frappe.throw(
			_("Due Date {0} cannot be before Posting Date {1}.").format(
				frappe.bold(doc.due_date), frappe.bold(doc.posting_date)
			)
		)
