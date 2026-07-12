from datetime import datetime


def generate_audit_id():

    date = datetime.now().strftime("%Y%m%d")

    return f"AUD-{date}-001"