# Certbot plugin for authentication using Gandi LiveDNS

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the Gandi
LiveDNS API to allow [Gandi](https://www.gandi.net/)
customers to prove control of a domain name.

## Usage

1. Obtain a Gandi API token (see [Gandi LiveDNS API](https://doc.livedns.gandi.net/))

2. Install the plugin using `pip install certbot-dns-gandi`

3. Create a `gandi.ini` config file with the following contents and apply `chmod 600 gandi.ini` on it:
   ```conf
   # Gandi Token
   dns_gandi_token=TOKEN

   # optional organization id, remove it if not used
   dns_gandi_sharing_id=SHARINGID
   ```
   Replace `TOKEN` with your Gandi personal access token and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file previously created:
   ```
   certbot certonly --authenticator dns-gandi --dns-gandi-credentials /etc/letsencrypt/gandi/gandi.ini -d domain.com
   ```
   Add additional options as required to specify an installation plugin etc.

Please note that this solution is usually not relevant if you're using Gandi's web hosting services as Gandi offers free automated certificates for all simplehosting plans having SSL in the admin interface.

Be aware that the plugin configuration must be provided by CLI, configuration for third-party plugins in `cli.ini` is not supported by certbot for the moment. Please refer to [#4351](https://github.com/certbot/certbot/issues/4351), [#6504](https://github.com/certbot/certbot/issues/6504) and [#7681](https://github.com/certbot/certbot/issues/7681) for details.

## Distribution

PyPI is the upstream distribution channel, other channels are not maintained by me.

* PyPI: https://pypi.org/project/certbot-dns-gandi
* Archlinux: https://aur.archlinux.org/packages/certbot-dns-gandi-git/
* Debian: https://packages.debian.org/sid/main/python3-certbot-dns-gandi
* Snap: Not yet packaged. I'm lazy.

Be careful, installing this plugin with PyPI will also install certbot via PyPI which may conflict with any other certbot already installed on your system.

## Wildcard certificates

This plugin is particularly useful when you need to obtain a wildcard certificate using dns challenges:

```
certbot certonly --authenticator dns-gandi --dns-gandi-credentials /etc/letsencrypt/gandi/gandi.ini -d domain.com -d \*.domain.com --server https://acme-v02.api.letsencrypt.org/directory
```

## Automatic renewal

You can setup automatic renewal using `crontab` with the following job for weekly renewal attempts:

```
0 0 * * 0 certbot renew -q --authenticator dns-gandi --dns-gandi-credentials /etc/letsencrypt/gandi/gandi.ini --server https://acme-v02.api.letsencrypt.org/directory
```

## Reading material

* A [blog post](https://www.linux.it/~ema/posts/letsencrypt-the-manual-plugin-is-not-working/) by [@realEmaRocca](https://twitter.com/realEmaRocca) describing how to use this plugin on Debian

## FAQ

> I don't have a personal access token, only a Gandi LiveDNS API Key

Live DNS API keys are deprecated and now unusable.

> I have a warning telling me `Plugin legacy name certbot-plugin-gandi:dns may be removed in a future version. Please use dns instead.`

Certbot had moved to remove 3rd party plugins prefixes since v1.7.0. Please switch to the new configuration format and remove any used prefix-based configuration.

> Why do you keep this plugin a third-party plugin ? Just merge it with certbot ?

This Gandi plugin is a third party plugin mainly because this plugin is not officially backed by Gandi and because Certbot [does not accept](https://certbot.eff.org/docs/contributing.html?highlight=propagation#writing-your-own-plugin) new plugin submissions.

![no_submission](https://user-images.githubusercontent.com/2095991/101479748-fd9da280-3952-11eb-884f-491470718f4d.png)

## Credits

Huge thanks to Michael Porter for its [original work](https://gitlab.com/sudoliyang/certbot-plugin-gandi) !
