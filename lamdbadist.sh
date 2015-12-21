#!/usr/bin/env sh

OUTPUT=rot13bot-lambda.zip

ABS_PATH=$(pwd)/dist/$OUTPUT

rm $ABS_PATH

zip -u $ABS_PATH rot13bot.cfg

cd rot13bot
zip -u $ABS_PATH rot13bot.py

cd $VIRTUAL_ENV"/lib/python2.7/site-packages"
zip -ru $ABS_PATH . -x \*.pyc
