import frappe

# Setup patches that must also run on a fresh install.
#
# `bench install-app` marks every patch from patches.txt as completed
# (frappe.installer.set_all_patches_as_completed) without executing it, so the
# setup they perform would be skipped on new sites. All of them are idempotent,
# so running them here is safe even if the app is reinstalled.
#
# Keep this list in sync with patches.txt when adding a setup patch.
INSTALL_PATCHES = (
	"erpnextpl_community.erpnextpl_community.patches.create_community_documents",
	"erpnextpl_community.erpnextpl_community.patches.create_polish_banks",
)


def after_install() -> None:
	for patch in INSTALL_PATCHES:
		frappe.get_attr(f"{patch}.execute")()

	frappe.db.commit()
