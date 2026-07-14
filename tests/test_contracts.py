from shared.contracts import (
    AuditRequest,
    ModuleResponse,
    AuditResponse
)


def test_audit_request():

    request = AuditRequest(
        website="https://ejemplo.com",
        keyword="marketing digital"
    )

    assert str(request.website) == "https://ejemplo.com/"
    assert request.keyword == "marketing digital"



def test_module_response():

    response = ModuleResponse(
        success=True,
        module="seo-content",
        audit_id="AUD-001",
        data={
            "message": "ok"
        },
        errors=[]
    )

    assert response.success is True
    assert response.module == "seo-content"



def test_audit_response():

    response = AuditResponse(
        success=True,
        audit_id="AUD-001",
        website="https://ejemplo.com",
        status="completed",
        results={
            "seo-content": {
                "status": "completed"
            }
        }
    )

    assert response.success is True
    assert response.status == "completed"