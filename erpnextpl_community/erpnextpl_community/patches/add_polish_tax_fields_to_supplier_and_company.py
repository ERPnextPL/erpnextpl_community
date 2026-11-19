from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	create_custom_fields,
)


def execute():
	# Adds REGON, KRS, PESEL and VAT Tax Status to Supplier, and REGON, KRS and
	# VAT Tax Status to Company (no PESEL there), on sites where create_community_documents already ran.
	# Idempotent: existing Custom Fields are left untouched. Limited to Supplier and
	# Company so fields intentionally removed from other doctypes are not restored.
	create_custom_fields(["Supplier", "Company"])
