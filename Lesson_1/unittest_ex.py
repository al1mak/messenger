"""Использование unittest"""
import unittest
from unittest.mock import Mock
import json
import lib


class TextSock(unittest.TestCase):

    def test3(self):

        res = \
        {
                'action': 'presence',
                'type': 'status'
        }

        res_buf = json.dumps(res).encode()

        virt_sock = Mock
        # virt_sock.send.return_value = None
        virt_sock.return_value = res_buf

        server = lib.Server(virt_sock)

        # server = lib.Server(virt_sock)
        really_result = server.receive_msg()

        self.assertEqual(res['type'], really_result['type'])


if __name__ == '__main__':
    unittest.main()
