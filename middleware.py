import unittest
from authentication_middleware import AuthenticationMiddleware

class TestAuthenticationMiddleware(unittest.TestCase):
    def test_authentication(self):
        auth_middleware = AuthenticationMiddleware()
        auth_middleware.authenticate("Alice")

        self.assertTrue(auth_middleware.is_authenticated("Alice"))
        self.assertFalse(auth_middleware.is_authenticated("Bob"))

        auth_middleware.authenticate("Bob")
        self.assertTrue(auth_middleware.is_authenticated("Bob"))

    def test_deauthentication(self):
        auth_middleware = AuthenticationMiddleware()
        auth_middleware.authenticate("Alice")

        self.assertTrue(auth_middleware.is_authenticated("Alice"))
        auth_middleware.deauthenticate("Alice")
        self.assertFalse(auth_middleware.is_authenticated("Alice"))

if __name__ == "__main__":
    unittest.main()
