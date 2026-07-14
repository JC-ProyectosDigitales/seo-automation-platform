import httpx


async def send_request(url, payload):

    if not url:

        return {

            "success": False,

            "error": "Module URL not configured"

        }


    try:

        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:

            response = await client.post(
                url,
                json=payload
            )

            response.raise_for_status()

            return response.json()


    except httpx.TimeoutException:

        return {

            "success": False,

            "error": "Module timeout"

        }


    except Exception as error:

        return {

            "success": False,

            "error": str(error)

        }