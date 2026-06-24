import frappe

# (bank_name, website, swift_number)
POLISH_BANKS = [
	("PKO Bank Polski SA", "https://www.pkobp.pl", "BPKOPLPW"),
	("Bank Pekao SA", "https://www.pekao.com.pl", "PKOPPLPW"),
	("Santander Bank Polska SA", "https://www.santander.pl", "WBKPPLPP"),
	("ING Bank Śląski SA", "https://www.ing.pl", "INGBPLPW"),
	("mBank SA", "https://www.mbank.pl", "BREXPLPW"),
	("Bank Millennium SA", "https://www.bankmillennium.pl", "BIGBPLPW"),
	("Alior Bank SA", "https://www.aliorbank.pl", "ALBPPLPW"),
	("BNP Paribas Bank Polska SA", "https://www.bnpparibas.pl", "PPABPLPK"),
	("Nest Bank SA", "https://www.nestbank.pl", "NESBPLP2"),
	("Citi Handlowy SA", "https://www.citihandlowy.pl", "CITIPLPX"),
	("Credit Agricole Bank Polska SA", "https://www.credit-agricole.pl", "AGRIPLPR"),
	("Bank Ochrony Środowiska SA", "https://www.bosbank.pl", "EBOSPLPW"),
	("VeloBank SA", "https://www.velobank.pl", "GBWCPLPP"),
	("Bank Pocztowy SA", "https://www.bankpocztowy.pl", "PBPLPLPW"),
	("Toyota Bank Polska SA", "https://www.toyotabank.pl", "TOBAPLPW"),
]


def execute():
	for bank_name, website, swift in POLISH_BANKS:
		if not frappe.db.exists("Bank", bank_name):
			frappe.get_doc(
				{
					"doctype": "Bank",
					"bank_name": bank_name,
					"website": website,
					"swift_number": swift,
				}
			).insert(ignore_permissions=True, ignore_mandatory=True)
