import frappe

from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	create_custom_fields,
)


def after_install():
	# Patches are only marked as executed on install, never run, so create the
	# Custom Fields here to give fresh sites the full set (idempotent).
	create_custom_fields()
	enable_polish_language()


def enable_polish_language():
	if frappe.db.exists("Language", "pl"):
		frappe.db.set_value("Language", "pl", "enabled", 1)
