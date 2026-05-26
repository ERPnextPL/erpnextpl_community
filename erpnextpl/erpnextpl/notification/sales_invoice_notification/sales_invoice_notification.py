import frappe


def get_context(context):
	doc = context.get("doc")
	if not doc:
		return {}

	company_id = doc.company
	company_info = _get_company_info(company_id)
	bank_account_name = company_info.get("default_bank_account")

	if not bank_account_name:
		bank_account_name = _get_company_bank_account_name(company_id)

	bank_account = _get_bank_account(bank_account_name)
	bank = _get_bank(bank_account.get("bank"))

	return {
		"company_name": company_info.get("company_name") or company_id,
		"company_info": company_info,
		"bank_account_name": bank_account_name,
		"bank_account": bank_account,
		"bank": bank,
		"customer_name": doc.customer_name or doc.customer,
		"payment_period": doc.get("custom_okres_rozliczeniowy"),
		"service_rows": doc.items or [],
		"payment_url": frappe.utils.get_url_to_form(doc.doctype, doc.name),
	}


def _get_company_info(company_id):
	return (
		frappe.db.get_value(
			"Company",
			company_id,
			[
				"company_name",
				"email",
				"phone_no",
				"tax_id",
				"company_description",
				"company_logo",
				"default_bank_account",
			],
			as_dict=True,
		)
		or {}
	)


def _get_company_bank_account_name(company_id):
	bank_account_names = frappe.db.get_all(
		"Bank Account",
		filters={"company": company_id, "is_company_account": 1, "is_default": 1},
		pluck="name",
		limit=1,
	)
	if not bank_account_names:
		bank_account_names = frappe.db.get_all(
			"Bank Account",
			filters={"company": company_id, "is_company_account": 1},
			pluck="name",
			limit=1,
		)
	return bank_account_names[0] if bank_account_names else None


def _get_bank_account(bank_account_name):
	if not bank_account_name:
		return {}

	return (
		frappe.db.get_value(
			"Bank Account",
			bank_account_name,
			["bank", "bank_account_no", "iban"],
			as_dict=True,
		)
		or {}
	)


def _get_bank(bank_name):
	if not bank_name:
		return {}

	return (
		frappe.db.get_value(
			"Bank",
			bank_name,
			["bank_name", "swift_number"],
			as_dict=True,
		)
		or {}
	)
