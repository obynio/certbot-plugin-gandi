pip install -e /tmp/work
printf 'certbot_plugin_gandi:dns_api_key=%s\n' $GANDI_API_KEY > /tmp/config.ini && chmod 400 /tmp/config.ini 
echo 'Example: certbot certonly --test-cert -a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials /tmp/config.ini -d domain.com'
exec /bin/sh
