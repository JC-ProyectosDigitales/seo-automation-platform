from app.services.module_client import send_request
from app.services.modules import MODULES


async def run_audit(audit):

    results = {}

    for module, url in MODULES.items():

        response = await send_request(
            url,
            audit
        )

        results[module] = response

    return results