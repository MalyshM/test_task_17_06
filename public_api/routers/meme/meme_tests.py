import asyncio
import unittest
import aiohttp as aiohttp


class MainPageTests(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:8090'
        self.loop = asyncio.get_event_loop()

    async def get_request(self, url: str, **params) -> dict:
        async with aiohttp.ClientSession(trust_env=True) as session:
            temp_str = '?'
            for key, value in params.items():
                temp_str += key + '=' + str(value) + '&'
            if temp_str[-1] == '&': temp_str = temp_str[:-1]
            if len(temp_str) == 1: temp_str = ''
            res = await session.get(self.base_url + url + temp_str)
            response_json = "Internal Server Error"
            try:
                response_json = await res.json()
            except:
                pass
            return {'status': res.status,
                    'response_json': response_json,
                    'response_text': await res.text(),
                    'headers': res.headers}

    def test_update_meme_successful(self):
        url = '/memes/5'
        response = self.loop.run_until_complete(self.get_request(url=url))

        self.assertEqual(response['status'], 200)

        response_json = response['response_json']
        self.assertIsInstance(response_json['id'], int)
        self.assertIsInstance(response_json['name'], str)
        self.assertIsInstance(response_json['link'], str)
        self.assertIsNotNone(response_json['id'])
        self.assertIsNotNone(response_json['name'])
        self.assertIsNotNone(response_json['link'])
        self.assertIn('https://', response_json['link'])
        self.assertIn(response_json['name'], response_json['link'])

    def test_update_meme_not_found(self):
        url = '/memes/666'
        response = self.loop.run_until_complete(self.get_request(url=url))

        self.assertEqual(response['status'], 404)

    def test_update_meme_validation_error(self):
        url = '/memes/id'
        response = self.loop.run_until_complete(self.get_request(url=url))

        self.assertEqual(response['status'], 422)


if __name__ == '__main__':
    unittest.main()
