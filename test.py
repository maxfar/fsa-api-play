import app
import httpretty
import unittest


class TestAuthoritiesGetting(unittest.TestCase):

    @httpretty.activate
    def test_returns_none_if_no_authorities(self):
        no_authorities = open('test_no_authorities', 'r').read()
        httpretty.register_uri(
            httpretty.GET,
            "http://api.ratings.food.gov.uk/Authorities/basic",
            body=no_authorities)

        result = app.get_authorities()
        self.assertEquals(result, None)

    def test_only_returns_authorities_list(self):
        result = app.get_authorities()
        self.assertEquals(type(result), list)

    @httpretty.activate
    def test_transform_is_correct(self):
        stub = open('test_establishment', 'r').read()
        httpretty.register_uri(
            httpretty.GET,
            "http://api.ratings.food.gov.uk/Establishments?localAuthorityId=1",
            body=stub)

        result = app.get_authority_results(1)
        self.assertEquals(result['5'], "100%")


if __name__ == '__main__':
    unittest.main()
