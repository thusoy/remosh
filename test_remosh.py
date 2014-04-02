import remosh

import os
import tempfile
import unittest

class RemoshTest(unittest.TestCase):

    def setUp(self):
        self.test_commands = tempfile.NamedTemporaryFile(delete=False)
        self.test_commands.write('secretid: echo "Hello, World!"\n'.encode('utf-8'))
        self.test_commands.close()
        self.app = remosh.create_app(self.test_commands.name, 'test.log')
        self.app.debug = True
        self.client = self.app.test_client()


    def tearDown(self):
        os.remove(self.test_commands.name)


    def test_invalid_command(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/?id=foobar')
        self.assertEqual(response.status_code, 400)


    def test_valid_command(self):
        response = self.client.post('/?id=secretid')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
