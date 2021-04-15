from foodgram.tests.base_classes import UrlsTestBase


class AboutUrlsTest(UrlsTestBase):
    def test_exists(self):
        urls = ['/about/project/', '/about/tech/']
        self.check_exists(urls)

    def test_redirects_remote(self):
        redirects = {'/about/author/': 'https://github.com/dmitriyperetoka'}
        self.check_redirects(redirects, remote=True)
