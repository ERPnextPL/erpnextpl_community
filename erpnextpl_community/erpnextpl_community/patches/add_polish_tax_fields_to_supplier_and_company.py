from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	create_custom_fields,
)


def execute():
	# Adds the Polish tax identifier fields (REGON, KRS, PESEL, VAT Tax Status)
	# to Supplier and Company on sites where create_community_documents already ran.
	# Idempotent: existing Custom Fields are left untouched.
	create_custom_fields()
