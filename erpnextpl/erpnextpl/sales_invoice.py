"""
Sales Invoice customizations for ERPNextPL
"""

import frappe


def validate_service_delivery_date(doc, method=None):
	"""
	If service_delivery_date is empty, populate it with posting_date
	on validation (save and submit).
	"""
	if not doc.service_delivery_date and doc.posting_date:
		doc.service_delivery_date = doc.posting_date
		frappe.msgprint(
			frappe._("Service Delivery Date was auto-filled from Posting Date"),
			indicator="blue",
			alert=False,
		)
