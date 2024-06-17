import asyncio

import aiohttp


async def fetch_get(session, url, as_csv: bool):
    try:
        async with session.get(url, ssl=False) as response:
            if as_csv:
                return await response.json()
            else:
                return {'response': await response.json(), "url": url}
    except Exception as e:
        print(e)
        raise e


async def fetch_post(session, url, data):
    try:
        async with session.post(url, ssl=False, data=data) as response:
            return await response.json()
    except Exception as e:
        print(e)
        raise e


async def make_request(url: str, crud_type: int, data=None):
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    cookie_jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(trust_env=True, headers={}, timeout=timeout, connector=conn,
                                     cookie_jar=cookie_jar) as session:
        match crud_type:
            case 0:
                res = await fetch_post(session, url, data)
    return res
