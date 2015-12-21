from __future__ import print_function

import itertools
import re
import ConfigParser
import logging

import tweepy

__author__ = "Tim Martin"
__version__ = '1.0.0'

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class Rot13Bot(object):
    def __init__(self, config_path="rot13bot.cfg"):
        self.logger = logging.getLogger(Rot13Bot.__name__)
        self.logger.setLevel(logging.INFO)

        config = ConfigParser.ConfigParser()
        config.read(config_path)
        api_key = config.get('auth', 'api_key')
        api_secret = config.get('auth', 'api_secret')
        token = config.get('auth', 'token')
        token_secret = config.get('auth', 'token_secret')

        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(token, token_secret)
        self.api = tweepy.API(self.auth)

        self.me = self.api.me()

    @staticmethod
    def _rot13(c):
        ordc = ord(c)
        if ordc in range(ord('a'), ord('z')+1):
            base = ord('a')
        elif ordc in range(ord('A'), ord('Z')+1):
            base = ord('A')
        else:
            return c

        offset = ordc - base
        return chr(base + ((offset + 13) % 26))

    @staticmethod
    def _entity_indices(entities_dict):
        """return a 140 character list representing the indices in a tweet's text where entites exist. Entities are things
        like hashtags, symbols, urls, and user_mentions."""
        indices = [False] * 140
        for entity_type_list in entities_dict.values():
            for entity in entity_type_list:
                entity_range = entity.get('indices', None)
                if entity_range:
                    for idx in range(*entity_range):
                        indices[idx] = True
        return indices


    @staticmethod
    def _rot13_tweet_text(text, entities):
        return "".join(Rot13Bot._rot13(c) if not is_entity else c
                       for c, is_entity
                       in itertools.izip(text,
                                         Rot13Bot._entity_indices(entities)))

    def _get_text_replace_me_with_them(self, text, their_screen_name):
        my_name = r"@%s" % (self.me.screen_name)
        their_name = r"@%s" % (their_screen_name)
        return re.sub(my_name, their_name, text)

    def _tweets_that_dont_need_replies(self):
        dont_need = []
        for tweet in self.api.user_timeline(user_id=self.me.id_str):
            if tweet.in_reply_to_status_id_str:
                dont_need.append(tweet.in_reply_to_status_id_str)
        return dont_need

    def reply_with_rot13(self):
        dont_need = self._tweets_that_dont_need_replies()
        replies = []
        for mention in self.api.mentions_timeline():
            if mention.author.screen_name == self.me.screen_name:
                # don't reply to myself
                continue
            if mention.id_str in dont_need:
                # don't duplicate reply
                continue
            reply_text = Rot13Bot._rot13_tweet_text(mention.text,
                                                   mention.entities)
            reply_text = self._get_text_replace_me_with_them(reply_text,
                                                       mention.author.screen_name)
            replies.append(
                    self.api.update_status(
                            status=reply_text,
                            in_reply_to_status_id=mention.id_str
                    )
            )
            self.logger.info("replying to id=%s with text=\"%s\"" % (
                mention.id_str, reply_text))
        if not replies:
            self.logger.info("no tweets to reply to")
        return replies

def reply_with_rot13():
    Rot13Bot().reply_with_rot13()

def for_lambda(event, context):
    reply_with_rot13()

if __name__ == '__main__':
    reply_with_rot13()