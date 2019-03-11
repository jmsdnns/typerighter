import re

from . import base
from . import primitives
from . import domains


# Patterns

REGEX_HEX = r'0-9a-f'
REGEX_PORT = r'[0-9]{2,5}'

REGEX_IPV4 = r'( ((%(octet)s\.){3} %(octet)s) )' % {
    'octet': '( 25[0-5] | 2[0-4][0-9] | [0-1]?[0-9]{1,2} )'
}

# 16 hex bytes
REGEX_IPV6_H16 = '[%s]{1,4}' % REGEX_HEX

# 16 hex bytes + traditional ip address
REGEX_IPV6_L32 = '(%(h16)s:%(h16)s|%(ipv4)s)' % {
    'h16': REGEX_IPV6_H16,
    'ipv4': REGEX_IPV4
}

# All allowed variations of H16 + L32
REGEX_IPV6 = r"""(
                                    (%(h16)s:){6}%(l32)s  |
                                ::  (%(h16)s:){5}%(l32)s  |
    (               %(h16)s )?  ::  (%(h16)s:){4}%(l32)s  |
    ( (%(h16)s:){,1}%(h16)s )?  ::  (%(h16)s:){3}%(l32)s  |
    ( (%(h16)s:){,2}%(h16)s )?  ::  (%(h16)s:){2}%(l32)s  |
    ( (%(h16)s:){,3}%(h16)s )?  ::  (%(h16)s:){1}%(l32)s  |
    ( (%(h16)s:){,4}%(h16)s )?  ::               %(l32)s  |
    ( (%(h16)s:){,5}%(h16)s )?  ::               %(h16)s  |
    ( (%(h16)s:){,6}%(h16)s )?  :: )""" % {
    'h16': REGEX_IPV6_H16,
    'l32': REGEX_IPV6_L32
}

REGEX_IP = r'^%s|%s$' % (REGEX_IPV4, REGEX_IPV6)

REGEX_MAC = r"""(
    ^([%(hex)s]{2}[-]){5}([%(hex)s]{2})$  |
    ^([%(hex)s]{2}[:]){5}([%(hex)s]{2})$  |
    ^([%(hex)s]{12})                      |
    ^([%(hex)s]{6}[-:]([%(hex)s]{6}))$    |
    ^([%(hex)s]{4}(\.[%(hex)s]{4}){2})$ 
)""" % {
    'hex': REGEX_HEX
}

_URL_GEN_DELIMS = set(':/?#[]@')
_URL_SUB_DELIMS = set('!$&\'()*+,;=')
_URL_UNRESERVED = set('-_.~')
_URL_PCHAR = _URL_SUB_DELIMS | _URL_UNRESERVED | set('%:@')
_URL_QUERY_EXTRAS = set('[]') # nonstandard

_URL_VALID_CHARS = _URL_GEN_DELIMS | _URL_SUB_DELIMS | _URL_UNRESERVED | set('%')
_URL_VALID_CHAR_STRING = str.join('', _URL_VALID_CHARS)
_URL_UNSAFE_CHAR_STRING = '\x00-\x20<>{}|"`\\^\x7F-\x9F'


def _uri_chars(allowed_chars):
    pattern = str.join('', _URL_VALID_CHARS - allowed_chars)

    pairs = [
        ('%', '%%'),
        (']', r'\]'),
        ('-', r'\-')
    ]
    for p in pairs:
        pattern = pattern.replace(p[0], p[1])

    return ('^' + _URL_UNSAFE_CHAR_STRING + pattern)


URI_PATTERNS = {
    'scheme' : r'[%s]+' % ('A-Z0-9.+-'),
    'user'   : r'[%s]+' % _uri_chars(_URL_UNRESERVED | _URL_SUB_DELIMS | set('%:')),
    'port'   : r'[0-9]{2,5}',
    'host4'  : REGEX_IPV4,
    'host6'  : r'[%s]+' % (REGEX_HEX + ':'),
    'hostn'  : r'[%s]+' % _uri_chars(set('.-')),
    'path'   : r'[%s]*' % _uri_chars(_URL_PCHAR | set('/')),
    'query'  : r'[%s]*' % _uri_chars(_URL_PCHAR | set('/?') | _URL_QUERY_EXTRAS),
    'frag'   : r'[%s]*' % _uri_chars(_URL_PCHAR | set('/?')),
}

REGEX_URL = r"""^(
        (?P<scheme> %(scheme)s ) ://
    (   (?P<user>   %(user)s   ) @   )?
    (\[ (?P<host6>  %(host6)s  ) ]
        | (?P<host4>  %(host4)s  )
        | (?P<hostn>  %(hostn)s  )     )
    ( : (?P<port>   %(port)s   )     )?
        (?P<path> / %(path)s   )?
    (\? (?P<query>  %(query)s  )     )?
    (\# (?P<frag>   %(frag)s   )     )?)$""" % URI_PATTERNS



REGEX_EMAIL = r"""^(
    ( ( [%(atext)s]+ (\.[%(atext)s]+)* ) | ("( [%(qtext)s\s] | [\\%(vchar)s\s] )*") )
    @((?!-)[A-Z0-9-]{1,63}(?<!-)\.)+[A-Z]{2,63})$""" % {
    'atext': '-A-Z0-9!#$%&\'*+/=?^_`{|}~',
    'qtext': '\x21\x23-\x5B\\\x5D-\x7E',
    'vchar': '\x21-\x7E'
}


# Types

class IPAddressType(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_IP, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)



class IPv4Type(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_IPV4, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)

    
    
class IPv6Type(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_IPV6, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)


class MACAddressType(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_MAC, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)

    

class URLType(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_URL, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)


class EmailType(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_EMAIL, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)
