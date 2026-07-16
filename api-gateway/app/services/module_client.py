import httpx



async def send_request(
    url,
    payload,
    timeout=30
):


    if not url:

        return {

            "success": False,

            "error": "Module URL not configured"

        }



    try:


        async with httpx.AsyncClient(
            timeout=timeout
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

            "error": "Module timeout",

            "timeout": timeout

        }



    except httpx.HTTPStatusError as error:


        return {

            "success": False,

            "error": f"HTTP error {error.response.status_code}"

        }



    except Exception as error:


        return {

            "success": False,

            "error": str(error)

        }