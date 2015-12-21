Rot13Bot
========

A Twitter bot that replies to mentions with the `ROT13 <https://en.wikipedia.org/wiki/ROT13>`_ substitution of the mention.

Tweet entities such as hashtags, urls, and user mentions are preserved--
except that the mention of this bot is replaced with the original tweet author.

This will probably be running on AWS Lambda, scheduled to reply every 5 minutes.

Example:

.. image:: http://i.imgur.com/wFr03wh.png
    :align: center
    :alt: `https://twitter.com/tmmrtn/status/678772968906878978`_

By Tim Martin