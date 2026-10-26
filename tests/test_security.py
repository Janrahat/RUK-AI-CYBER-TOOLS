import unittest
from modules.security import normalize_url, check_url, ip_info
class SecurityTests(unittest.TestCase):
    def test_adds_https(self): self.assertEqual(normalize_url('example.com'),'https://example.com')
    def test_rejects_ftp(self):
        with self.assertRaises(ValueError): normalize_url('ftp://example.com')
    def test_warns_http(self): self.assertTrue(check_url('http://example.com')['warnings'])
    def test_private_ip(self): self.assertTrue(ip_info('192.168.1.2')['is_private'])
    def test_invalid_ip(self): self.assertIn('error',ip_info('not-an-ip'))
if __name__=='__main__': unittest.main()
