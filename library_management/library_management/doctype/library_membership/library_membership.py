# Copyright (c) 2023, frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_to_date
from frappe.model.document import Document

class LibraryMembership(Document):
	# pass
	def before_submit(self):
		exists = frappe.db.exists('Library Membership',{
			'library_member': self.library_member,
			'docstatus': 1,
			'to_date': ('>', self.from_date),
			}
		)
		if exists:
			frappe.throw('There is an active membership for this member')

		#get loan period and compute to_date by adding loan_period to from_date
		loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
		self.to_date = add_to_date(self.from_date, loan_period or 30)