from setuptools import setup, find_packages

from rot13bot import rot13bot

install_requires = [
    'tweepy'
]

tests_requires = [
    'pytest'
]

setup(
        name='rot13bot',
        version=rot13bot.__version__,
        packages=find_packages(),
        author=rot13bot.__author__,
        install_requires=install_requires,
        tests_requires=tests_requires,
        url="http://timmart.in",
        author_email="tim@timmart.in"
)
