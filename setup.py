from setuptools import setup, find_packages 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='certbot-plugin-gandi',
    version='1.0.1',
    author="Yohann Leon",
    author_email="yohann@leon.re",
    description="Certbot plugin for authentication using Gandi LiveDNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obynio/certbot-plugin-gandi",
    packages=find_packages(),
    python_requires=' >=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
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
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        ],
)
