// Fix: frappe.meta.get_label() returns raw English label without calling __()
// This patches validate_company_and_party to translate the field label properly.
if (typeof erpnext !== "undefined" && erpnext.TransactionController) {
	erpnext.TransactionController.prototype.validate_company_and_party = function () {
		var me = this;
		var valid = true;

		if (frappe.flags.ignore_company_party_validation) {
			return valid;
		}

		$.each(["company", "customer"], function (i, fieldname) {
			if (
				frappe.meta.has_field(me.frm.doc.doctype, fieldname) &&
				!["Purchase Order", "Purchase Invoice"].includes(me.frm.doc.doctype)
			) {
				if (!me.frm.doc[fieldname]) {
					frappe.msgprint(
						__("Please specify") +
							": " +
							__(
								frappe.meta.get_label(
									me.frm.doc.doctype,
									fieldname,
									me.frm.doc.name
								)
							) +
							". " +
							__("It is needed to fetch Item Details.")
					);
					valid = false;
				}
			}
		});
		return valid;
	};
}
