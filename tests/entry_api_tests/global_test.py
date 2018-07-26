from tests.entry_api_tests.base_test import BaseTestCase


class GlobalTestCase(BaseTestCase):

    def test_invalid_urls_trigger_not_found(self):
        responses = []
        data = {'title': 'A title', 'body': 'A body'}
        urls = ['/gibberish', '/api/v1/entries/', '/api/v1/entries/x']
        for url in urls:
            responses.append(self.get(url))
            responses.append(self.post(url, data=data))
            responses.append(self.put(url, data=data))
            responses.append(self.delete(url))
        for response in responses:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.mimetype, 'application/json')
