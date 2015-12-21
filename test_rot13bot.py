import string

import pytest
import mock

from rot13bot.rot13bot import Rot13Bot

class TestRot13Bot(object):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rot13(self):
        for a, b in zip("abcdefghijklmnopqrstuvwxyz",
                        "nopqrstuvwxyzabcdefghijklm"):
            assert a == Rot13Bot._rot13(b)
        for a, b in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                        "NOPQRSTUVWXYZABCDEFGHIJKLM"):
            assert a == Rot13Bot._rot13(b)
        for a, b in zip(string.punctuation, string.punctuation):
            a == Rot13Bot._rot13(b)
