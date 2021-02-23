# Certbot plugin for authentication using Gandi LiveDNS

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the Gandi
LiveDNS API to allow [Gandi](https://www.gandi.net/)
customers to prove control of a domain name.

## Usage

1. Obtain a Gandi API token (see [Gandi LiveDNS API](https://doc.livedns.gandi.net/))

2. Install the plugin using `pip install certbot-plugin-gandi`

3. Create a `gandi.ini` config file with the following contents and apply `chmod 600 gandi.ini` on it:
   ```
   # live dns v5 api key
   dns_gandi_api_key=APIKEY

   # optional organization id, remove it if not used
   dns_gandi_sharing_id=SHARINGID
   ```
   Replace `APIKEY` with your Gandi API key and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file previously created:
   ```
   certbot certonly --authenticator dns-gandi --dns-gandi-credentials /etc/letsencrypt/gandi/gandi.ini -d domain.com
   ```
   Add additional options as required to specify an installation plugin etc.

Please note that this solution is usually not relevant if you're using Gandi's web hosting services as Gandi offers free automated certificates for all simplehosting plans having SSL in the admin interface. Huge thanks to Michael Porter for its original work !

Be aware that the plugin configuration must be provided by CLI, configuration for third-party plugins in `cli.ini` is not supported by certbot for the moment. Please refer to [#4351](https://github.com/certbot/certbot/issues/4351), [#6504](https://github.com/certbot/certbot/issues/6504) and [#7681](https://github.com/certbot/certbot/issues/7681) for details.

## Distribution

* PyPI: https://pypi.org/project/certbot-plugin-gandi/
* Archlinux: https://aur.archlinux.org/packages/certbot-dns-gandi-git/

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

## FAQ

> I have a warning telling me `Plugin legacy name certbot-plugin-gandi:dns may be removed in a future version. Please use dns instead.`

Certbot had moved to remove 3rd party plugins prefixes. Please use `--authenticator dns-gandi --dns-gandi-credentials`. See [certbot/8131](https://github.com/certbot/certbot/pull/8131) and [certbot-plugin-gandi/23](https://github.com/obynio/certbot-plugin-gandi/issues/23) for details. Please make sure to update the configuration file to the new format.

> Why do you keep this plugin a third-party plugin ? Just merge it with certbot ?

This Gandi plugin is a third party plugin mainly because this plugin is not officially backed by Gandi and because Certbot [does not accept](https://certbot.eff.org/docs/contributing.html?highlight=propagation#writing-your-own-plugin) new plugin submissions.

![no_submission](https://user-images.githubusercontent.com/2095991/101479748-fd9da280-3952-11eb-884f-491470718f4d.png)

