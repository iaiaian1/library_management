# Copyright (c) 2023, frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryTransact(Document):
	# pass
	# Theres no function that stores id in the transact database
	# fix by issuing the unique transact ID and remove that on return

	def before_submit(self):
		if self.type == 'Issue':
			self.validate_issue()
			self.validate_maximum_limit()
			# set the article status to be Issued
			article = frappe.get_doc('Article', self.article)
			article.status = 'Issued'
			article.save()

		elif self.type == 'Return':
			self.validate_return()
			# self.transact_return()
			# set the article status to be Issued
			article = frappe.get_doc('Article', self.article)
			article.status = 'Available'
			article.save()
		
	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc('Article', self.article)
		# article cannot be issued if it is already issued
		if article.status == 'Issued':
			frappe.throw('Article is already issued by another member')

	def validate_return(self):
		self.validate_membership()
		article = frappe.get_doc('Article', self.article)
		# article cannot be returned if its not issued first
		if article.status == 'Available':
			frappe.throw('Article cannot be returned while not issued')

	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value('Library Settings', 'max_articles')
		count = frappe.db.count('Library Transact', {
			'library_member': self.library_member,
			'type': 'Issue',
			'docstatus': 1
		})
		if count >= max_articles:
			frappe.throw("Maximum limit reached for issuing articles")

	# def transact_return(self):
	# 	frapp


	def validate_membership(self):
		valid_membership = frappe.db.exists('Library Membership', {
			'library_member': self.library_member,
			'docstatus' : 1,
			'from_date': ('<=', self.date),
			'to_date': ('>=', self.date)
		},)

		if not valid_membership:
			frappe.throw('The member does not have a valid membership')