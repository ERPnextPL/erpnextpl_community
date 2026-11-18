import frappe

from erpnextpl_community.erpnextpl_community.patches import create_polish_banks
from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	create_custom_fields,
	create_standard_documents,
)


def after_install():
	# On install-app Frappe only marks patches as executed and never runs them, so
	# run the (idempotent) setup steps here to give fresh sites the full set:
	# Custom Fields, print formats, email templates, notifications and banks.
	create_custom_fields()
	create_standard_documents()
	create_polish_banks.execute()
	enable_polish_language()


def enable_polish_language():
	if frappe.db.exists("Language", "pl"):
		frappe.db.set_value("Language", "pl", "enabled", 1)
