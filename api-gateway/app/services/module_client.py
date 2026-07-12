import httpx


async def send_request(url, payload):

    try:

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                json=payload
            )

            return response.json()


    except Exception as error:

        return {

            "success":False,

            "error":str(error)

        }