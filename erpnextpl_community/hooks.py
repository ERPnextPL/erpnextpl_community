app_name = "erpnextpl_community"
app_title = "ERPNextPL"
app_publisher = "ERPTECH sp. z o.o."
app_description = "ERPNextPL"
app_email = "biuro@erptech.pl"
app_license = "mit"

export_python_type_annotations = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnextpl_community/css/erpnextpl.css"
app_include_js = "/assets/erpnextpl_community/js/erpnextpl_fixes.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnextpl_community/css/erpnextpl.css"
# web_include_js = "/assets/erpnextpl_community/js/erpnextpl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpnextpl_community/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# Community keeps only lightweight, non-premium behavior.
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "erpnextpl_community/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "erpnextpl_community.utils.jinja_methods",
# 	"filters": "erpnextpl_community.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpnextpl_community.install.before_install"
# after_install = "erpnextpl_community.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpnextpl_community.uninstall.before_uninstall"
# after_uninstall = "erpnextpl_community.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "erpnextpl_community.utils.before_app_install"
# after_app_install = "erpnextpl_community.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "erpnextpl_community.utils.before_app_uninstall"
# after_app_uninstall = "erpnextpl_community.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnextpl_community.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes
# Community intentionally avoids premium import overrides.

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"validate": "erpnextpl_community.sales_invoice.validate_sales_invoice",
	},
	"Customer": {
		"validate": "erpnextpl_community.customer.validate_customer",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnextpl_community.tasks.all"
# 	],
# 	"daily": [
# 		"erpnextpl_community.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnextpl_community.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnextpl_community.tasks.weekly"
# 	],
# 	"monthly": [
# 		"erpnextpl_community.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "erpnextpl_community.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnextpl_community.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnextpl_community.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["erpnextpl_community.utils.before_request"]
# after_request = ["erpnextpl_community.utils.after_request"]

# Job Events
# ----------
# before_job = ["erpnextpl_community.utils.before_job"]
# after_job = ["erpnextpl_community.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpnextpl_community.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
