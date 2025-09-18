import unittest
from config import DB_CONFIG


class TestConfig(unittest.TestCase):

    def test_config_has_all_keys(self):
        expected_keys = ["host", "database", "user", "password", "port"]
        for key in expected_keys:
            self.assertIn(key, DB_CONFIG)
            self.assertIsInstance(DB_CONFIG[key], str)


if __name__ == "__main__":
    unittest.main()
