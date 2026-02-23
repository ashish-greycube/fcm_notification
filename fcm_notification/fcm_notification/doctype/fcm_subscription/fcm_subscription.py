# Copyright (c) 2025, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import firebase_admin
from firebase_admin import credentials, messaging, exceptions
from fcm_notification.firebase_admin_client import get_firebase_app

app = get_firebase_app()

class FCMSubscription(Document):
	def validate(self):
		user_token = get_selected_users_tokens(self)

		subscribe_to_topic(user_token, self.topic)


def subscribe_to_topic(token_or_list, topic_name):
	"""Subscribes one or more FCM registration tokens to a topic."""
	try:
        # messaging.subscribe_to_topic accepts a string (single) or list (multiple)
		response = messaging.subscribe_to_topic(token_or_list, topic_name)
		print(f"Successfully subscribed {response.success_count} tokens to {topic_name}", "="*100)
	except exceptions.FirebaseError as e:
		print(e, "="*100)


def get_selected_users_tokens(self):
	user_token = []
	for i in self.fcm_user:
		user_token.append(frappe.get_value("FCM User", i.users, "registration_token"))

	return user_token