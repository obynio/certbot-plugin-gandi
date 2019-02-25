# Certbot plugin for authentication using Gandi LiveDNS

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the Gandi
LiveDNS API to allow [Gandi](https://www.gandi.net/)
customers to prove control of a domain name.

## Usage

1. Obtain a Gandi API token (see [Gandi LiveDNS API](https://doc.livedns.gandi.net/))
 
2. Install the plugin using `pip install certbit-plugin-gandi`

3. Create a `gandi.ini` config file with the following contents and apply `chmod 600 gandi.ini` on it:
   ```
   certbot_plugin_gandi:dns_api_key=APIKEY
   ```
   Replace `APIKEY` with your Gandi API key and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file previously created: 
   ```
   certbot certonly -a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials gandi.ini -d domain.com
   ```
   Add additional options as required to specify an installation plugin etc.
   
## Wildcard certificates

This plugin is particularly useful when you need to obtain a wildcard certificate using dns challenges:

```
certbot certonly -a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials gandi.ini -d domain.com -d \*.domain.com --server https://acme-v02.api.letsencrypt.org/directory
```

## Automatic renewal

You can setup automatic renewal using `crontab` with the following job for weekly renewal attempts:

```
* 1 * * 1 certbot renew -q -a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials /etc/letsencrypt/gandi/gandi.ini --server https://acme-v02.api.letsencrypt.org/directory
```
