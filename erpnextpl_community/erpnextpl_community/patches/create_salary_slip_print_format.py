from erpnextpl_community.erpnextpl_community.patches.create_community_documents import (
	create_standard_documents,
)


def execute():
	# Creates the "Pasek Wynagrodzenia - Timesheet" print format (and any other
	# missing standard document) on sites where create_community_documents already ran.
	create_standard_documents(migrate_existing=False)
