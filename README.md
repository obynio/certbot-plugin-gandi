# Certbot plugin for authentication using Gandi LiveDNS

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the Gandi
LiveDNS API to allow [Gandi](https://www.gandi.net/)
customers to prove control of a domain name.

## Usage

> /!\ Certbot 1.7.0 imposed breaking changes on this plugin, make sure to remove any prefix-based configuration

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

Please note that this solution is usually not relevant if you're using Gandi's web hosting services as Gandi offers free automated certificates for all simplehosting plans having SSL in the admin interface.

Be aware that the plugin configuration must be provided by CLI, configuration for third-party plugins in `cli.ini` is not supported by certbot for the moment. Please refer to [#4351](https://github.com/certbot/certbot/issues/4351), [#6504](https://github.com/certbot/certbot/issues/6504) and [#7681](https://github.com/certbot/certbot/issues/7681) for details.

## Distribution

PyPI is the upstream distribution channel, other channels are not maintained by me.

- PyPI: https://pypi.org/project/certbot-plugin-gandi/
- Archlinux: https://aur.archlinux.org/packages/certbot-dns-gandi-git/
- Debian: https://packages.debian.org/sid/main/python3-certbot-dns-gandi

Every release pushed to PyPI is signed with GPG.

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

- A [blog post](https://www.linux.it/~ema/posts/letsencrypt-the-manual-plugin-is-not-working/) by [@realEmaRocca](https://twitter.com/realEmaRocca) describing how to use this plugin on Debian

## FAQ

> I have a warning telling me `Plugin legacy name certbot-plugin-gandi:dns may be removed in a future version. Please use dns instead.`

Certbot had moved to remove 3rd party plugins prefixes since v1.7.0. Please switch to the new configuration format and remove any used prefix-based configuration.
For the time being, you can still use prefixes, but if you do so and keep using prefix-based cli arguments, stay consistent and use prefix-based configuration in the ini file.

#### New post-prefix configuration for certbot>=1.7.0

- `--authenticator dns-gandi --dns-gandi-credentials`
- `gandi.ini`

```
# live dns v5 api key
dns_gandi_api_key=APIKEY

# optional organization id, remove it if not used
# if you use certbot<1.7.0 please use certbot_plugin_gandi:dns_sharing_id=SHARINGID
dns_gandi_sharing_id=SHARINGID
```

#### Legacy prefix-based configuration for certbot<1.7.0

- `-a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials`
- `gandi.ini`

```
 # live dns v5 api key
certbot_plugin_gandi:dns_api_key=APIKEY

# optional organization id, remove it if not used
certbot_plugin_gandi:dns_sharing_id=SHARINGID
```

See [certbot/8131](https://github.com/certbot/certbot/pull/8131) and [certbot-plugin-gandi/23](https://github.com/obynio/certbot-plugin-gandi/issues/23) for details. Please make sure to update the configuration file to the new format.

> I get a `Property "certbot_plugin_gandi:dns_api_key" not found (should be API key for Gandi account).. Skipping.`

See above.

> Why do you keep this plugin a third-party plugin ? Just merge it with certbot ?

This Gandi plugin is a third party plugin mainly because this plugin is not officially backed by Gandi and because Certbot [does not accept](https://certbot.eff.org/docs/contributing.html?highlight=propagation#writing-your-own-plugin) new plugin submissions.

![no_submission](https://user-images.githubusercontent.com/2095991/101479748-fd9da280-3952-11eb-884f-491470718f4d.png)

## Credits

Huge thanks to Michael Porter for its [original work](https://gitlab.com/sudoliyang/certbot-plugin-gandi) !
