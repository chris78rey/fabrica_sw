import unittest

from fabrica_sw.auth_security import hash_password_secure, validate_password_complexity


class AuthSecurityTests(unittest.TestCase):
    def test_hash_is_salted_and_does_not_expose_password(self):
        password = "Seguro123!"
        first = hash_password_secure(password)
        second = hash_password_secure(password)

        self.assertNotEqual(first, second)
        self.assertEqual(len(first), 96)
        self.assertNotIn(password, first)

    def test_complexity_accepts_valid_password(self):
        self.assertTrue(validate_password_complexity("Seguro123!"))

    def test_complexity_rejects_short_password(self):
        self.assertFalse(validate_password_complexity("Seg1!"))

    def test_complexity_rejects_password_without_digit(self):
        self.assertFalse(validate_password_complexity("Seguridad!"))

    def test_complexity_rejects_password_without_uppercase(self):
        self.assertFalse(validate_password_complexity("seguro123!"))


if __name__ == "__main__":
    unittest.main()
