from foodgram.tests.base_classes import UrlsTestBase


class ApiUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = ['/api/v1/ingredients/']
        self.check_exists(urls)
