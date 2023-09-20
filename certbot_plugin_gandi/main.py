import logging
import uuid

from certbot import interfaces, errors
from certbot.plugins import dns_common

from . import gandi_api

logger = logging.getLogger(__name__)

def register_authenticator(cls):
    try:
        interfaces.Authenticator.register(cls)
    except AttributeError:
        import zope.interface
        zope.interface.implementer(interfaces.IAuthenticator)(cls)
        zope.interface.provider(interfaces.IPluginFactory)(cls)
    return cls

@register_authenticator
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Gandi (using LiveDNS)."""

    description = 'Obtain certificates using a DNS TXT record (if you are using Gandi for DNS).'


    def __init__(self, config, name, **kwargs):
        super(Authenticator, self).__init__(config, name, **kwargs)
        self.credentials = None


    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Gandi credentials INI file.')


    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Gandi LiveDNS API.'

    def _validate_sharing_id(self, credentials):
        sharing_id = credentials.conf('sharing-id')
        if sharing_id:
            try:
                uuid.UUID(sharing_id, version=4)
            except ValueError:
                raise errors.PluginError("Invalid sharing_id: {0}.".format(sharing_id))

    def _validate(self, credentials):
        self._validate_sharing_id(credentials)

        # Either api-key or token must be set
        if not credentials.conf('api-key') and not credentials.conf('token'):
            raise errors.PluginError(
                'Missing property in credentials configuration file {0}: {1}'.format(
                    credentials.confobj.filename, 'dns_gandi_api_key or dns_gandi_token must be set')
                )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Gandi credentials INI file',
            {},
            self._validate
        )


    def _perform(self, domain, validation_name, validation):
        error = gandi_api.add_txt_record(self._get_gandi_config(), domain, validation_name, validation)
        if error is not None:
            raise errors.PluginError('An error occurred adding the DNS TXT record: {0}'.format(error))


    def _cleanup(self, domain, validation_name, validation):
        error = gandi_api.del_txt_record(self._get_gandi_config(), domain, validation_name, validation)
        if error is not None:
            logger.warn('Unable to find or delete the DNS TXT record: %s', error)


    def _get_gandi_config(self):
        return gandi_api.get_config(
            api_key = self.credentials.conf('api-key'),
            sharing_id = self.credentials.conf('sharing-id'),
            personal_access_token = self.credentials.conf('token'),
        )
