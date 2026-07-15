from datetime import datetime


def generate_audit_id():

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    return f"AUD-{timestamp}"
