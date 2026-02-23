import firebase_admin
from firebase_admin import credentials
import frappe
import os
from frappe.utils import get_files_path

_app = None

def get_firebase_app():
    global _app
    
    # 1. Return if already initialized in this worker's memory
    if _app is not None:
        return _app

    # 2. Double check if Firebase already has an app instance (safety for pre-fork)
    if firebase_admin._apps:
        _app = firebase_admin.get_app()
        return _app

    # 3. Initialize fresh
    settings = frappe.get_cached_doc("FCM Settings")
    if not settings.enabled:
        frappe.throw("FCM is not enabled in FCM Settings")

    if not settings.credential:
        frappe.throw("Firebase credentials are missing in FCM Settings")

    # Resolve the path to the private file
    certificate_path = os.path.abspath(
        os.path.join(get_files_path(is_private=True), os.path.basename(settings.credential))
    )

    if not os.path.exists(certificate_path):
        frappe.throw(f"Firebase Certificate not found at {certificate_path}")

    cred = credentials.Certificate(certificate_path)
    _app = firebase_admin.initialize_app(cred)
    
    return _app