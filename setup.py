from setuptools import setup, find_packages 


setup(
    name='certbot-plugin-gandi',
    packages=find_packages(),
    install_requires=[
        'certbot',
        'zope.interface',
        'requests>=2.4.2',
    ],
    entry_points={
        'certbot.plugins': [
            'dns = certbot_plugin_gandi.main:Authenticator',
        ],
    },
)
