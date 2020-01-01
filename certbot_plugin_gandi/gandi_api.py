import requests
import six

from collections import namedtuple
from certbot.plugins import dns_common

_GandiConfig = namedtuple('_GandiConfig', ('api_key', 'sharing_id',))
_BaseDomain = namedtuple('_BaseDomain', ('fqdn'))

def get_config(api_key, sharing_id):
    return _GandiConfig(api_key=api_key, sharing_id=sharing_id)


def _get_json(response):
    try:
        data = response.json()
    except ValueError:
        return dict()
    return data


def _get_response_message(response, default='<No reason given>'):
    return _get_json(response).get('message', default)


def _headers(cfg):
    return {
        'Content-Type': 'application/json',
        'X-Api-Key': cfg.api_key
    }


def _get_url(*segs):
    return 'https://dns.api.gandi.net/api/v5/{}'.format('/'.join(segs))

def _request(cfg, method, segs, **kw):
    headers = _headers(cfg)
    url = _get_url(*segs)
    return requests.request(method, url, headers=headers, params={'sharing_id': cfg.sharing_id}, **kw)


def _get_base_domain(cfg, domain):
    for candidate_base_domain in dns_common.base_domain_name_guesses(domain):
        response = _request(cfg, 'GET', ('domains', candidate_base_domain))
        if response.ok:
            data = _get_json(response)
            fqdn = data.get('fqdn')
            if fqdn:
                return _BaseDomain(fqdn=fqdn)
    return None


def _get_relative_name(base_domain, name):
    suffix = '.' + base_domain.fqdn
    return name[:-len(suffix)] if name.endswith(suffix) else None


def _get_txt_record(cfg, base_domain, relative_name):
    response = _request(cfg, 'GET', ['domains', base_domain.fqdn, 'records', relative_name, 'TXT'])
    if not response.ok:
        return []
    data = _get_json(response)
    vals = data.get('rrset_values')
    if vals:
        return vals
    else:
        return []


def _update_txt_record(cfg, base_domain, relative_name, rrset):
    return _request(cfg, 'PUT', ['domains', base_domain.fqdn, 'records', relative_name, 'TXT'],
                                json={'rrset_values': rrset})


def _update_record(cfg, domain, name, request_runner):

    base_domain = _get_base_domain(cfg, domain)
    if base_domain is None:
        return 'Unable to get base domain for "{}"'.format(domain)
    relative_name = _get_relative_name(base_domain, name)
    if relative_name is None:
        return 'Unable to derive relative name for "{}"'.format(name)

    response = request_runner(base_domain, relative_name)

    return None if response.ok else _get_response_message(response)


def add_txt_record(cfg, domain, name, value):

    def requester(base_domain, relative_name):
        rrset = [value] + _get_txt_record(cfg, base_domain, relative_name)
        return _update_txt_record(cfg, base_domain, relative_name, rrset)

    return _update_record(cfg, domain, name, requester)


def del_txt_record(cfg, domain, name, value):

    def requester(base_domain, relative_name):
        existing = _get_txt_record(cfg, base_domain, relative_name)
        rrset = list(filter(lambda rr: rr.strip('"') != value, existing))
        return _update_txt_record(cfg, base_domain, relative_name, rrset)

    return _update_record(cfg, domain, name, requester)


