# Copyright (c) 2025, Wahni IT Solutions and contributors
# For license information, please see license.txt

import os

import firebase_admin
import frappe
from firebase_admin import credentials, messaging
from frappe import _
from frappe.utils import get_files_path


class FCMNotification:
	def __init__(self):
		self.settings = frappe.get_cached_doc("FCM Settings")
		if not self.settings.enabled:
			frappe.throw(_("FCM is not enabled"))

		certificate_path = os.path.abspath(
			os.path.join(get_files_path(is_private=True), os.path.basename(self.settings.credential))
		)
		cred = credentials.Certificate(certificate_path)
		firebase_admin.initialize_app(cred)


	def send_topic_message(self, topic, message):
		
		if isinstance(message, str):

			message = json.loads(message)

		notification_data = message.get("notification", {})
		notification = None

		if notification_data:

			notification = messaging.Notification(

                title=notification_data.get("title", ""),

                body=notification_data.get("body", ""),

            )

		message = messaging.Message(
			notification=notification,
			topic=topic,
		)
		return messaging.send(message)

# Copyright (c) 2025, Wahni IT Solutions and contributors
# For license information, please see license.txt