from setuptools import setup, find_packages 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='certbot-plugin-gandi',
    version='1.0.0',
    author="Yohann Leon",
    author_email="yohann@leon.re",
    description="Certbot plugin for authentication using Gandi LiveDNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obynio/certbot-plugin-gandi",
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
        ],
)
