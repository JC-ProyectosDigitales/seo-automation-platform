from app.services.module_client import send_request


async def run_audit(audit):

    results = {}


    modules = {

        "seo_onpage": "http://seo-onpage:5001/audit",

        "seo_content": "http://seo-content:5003/audit",

        "seo_technical": "http://seo-technical:5002/audit",

        "seo_monitor": "http://seo-monitor:5004/audit"

    }


    for module, url in modules.items():

        results[module] = await send_request(
            url,
            audit
        )


    return results
