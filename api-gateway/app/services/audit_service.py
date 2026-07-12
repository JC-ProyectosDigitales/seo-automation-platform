from app.utils.audit_id import generate_audit_id


def create_audit(data):

    audit_id = generate_audit_id()


    return {

        "audit_id": audit_id,

        "website": data.website,

        "keyword": data.keyword,

        "status": "created"

    }