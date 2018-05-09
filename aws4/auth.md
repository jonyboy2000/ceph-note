
```
def canonical_request(self, request):
        cr = [request.method.upper()]
        path = self._normalize_url_path(urlsplit(request.url).path)
        cr.append(path)
        cr.append(self.canonical_query_string(request))
        headers_to_sign = self.headers_to_sign(request)
        cr.append(self.canonical_headers(headers_to_sign) + '\n')
        cr.append(self.signed_headers(headers_to_sign))
        if 'X-Amz-Content-SHA256' in request.headers:
            body_checksum = request.headers['X-Amz-Content-SHA256']
        else:
            body_checksum = self.payload(request)
        cr.append(body_checksum)
        return '\n'.join(cr)

    def _normalize_url_path(self, path):
        normalized_path = quote(normalize_url_path(path), safe='/~')
        return normalized_path


def _canonical_query_string_params(self, params):
        l = []
        for param in sorted(params):
            value = str(params[param])
            l.append('%s=%s' % (quote(param, safe='-_.~'),
                                quote(value, safe='-_.~')))
        cqs = '&'.join(l)
        return cqs
def quote(s, safe='/'):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted.

    RFC 2396 Uniform Resource Identifiers (URI): Generic Syntax lists
    the following reserved characters.

    reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" |
                  "$" | ","

    Each of these characters is reserved in some component of a URL,
    but not necessarily in all of them.

    By default, the quote function is intended for quoting the path
    section of a URL.  Thus, it will not encode '/'.  This character
    is reserved, but in typical usage the quote function is being
    called on a path where the existing slash characters are used as
    reserved characters.
    """
    # fastpath
    if not s:
        if s is None:
            raise TypeError('None object cannot be quoted')
        return s
    cachekey = (safe, always_safe)
    try:
        (quoter, safe) = _safe_quoters[cachekey]
    except KeyError:
        safe_map = _safe_map.copy()
        safe_map.update([(c, c) for c in safe])
        quoter = safe_map.__getitem__
        safe = always_safe + safe
        _safe_quoters[cachekey] = (quoter, safe)
    if not s.rstrip(safe):
        return s
    return ''.join(map(quoter, s))

def quote_plus(s, safe=''):
    """Quote the query fragment of a URL; replacing ' ' with '+'"""
    if ' ' in s:
        s = quote(s, safe + ' ')
        return s.replace(' ', '+')
    return quote(s, safe)



def unquote(s):
    """unquote('abc%20def') -> 'abc def'."""
    if _is_unicode(s):
        if '%' not in s:
            return s
        bits = _asciire.split(s)
        res = [bits[0]]
        append = res.append
        for i in range(1, len(bits), 2):
            append(unquote(str(bits[i])).decode('latin1'))
            append(bits[i + 1])
        return ''.join(res)

    bits = s.split('%')
    # fastpath
    if len(bits) == 1:
        return s
    res = [bits[0]]
    append = res.append
    for item in bits[1:]:
        try:
            append(_hextochr[item[:2]])
            append(item[2:])
        except KeyError:
            append('%')
            append(item)
    return ''.join(res)

def unquote_plus(s):
    """unquote('%7e/abc+def') -> '~/abc def'"""
    s = s.replace('+', ' ')
    return unquote(s)

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')

_safe_map = {}
for i, c in zip(xrange(256), str(bytearray(xrange(256)))):
    _safe_map[c] = c if (i < 128 and c in always_safe) else '%{:02X}'.format(i)
_safe_quoters = {}


```


```
import urllib
print urllib.quote('!')

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

canonicalrequest = '''PUT
/alpha!soup/

host:s3.ecloud.today
user-agent:Boto/2.48.0 Python/2.7.5 Linux/3.10.0-693.11.6.el7.x86_64
x-amz-content-sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
x-amz-date:20180325T035121Z

host;user-agent;x-amz-content-sha256;x-amz-date
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

hsh = hashlib.sha256(canonicalrequest.encode())
canonical_request_hash = hsh.hexdigest()  # 8022bfe928617feede7994648f87933711ea8a747ae696acca56baa0a9fb9970


signing_key = getSignatureKey("s3testuser1","20180325","us-east-1","s3")
string_to_sign = '''AWS4-HMAC-SHA256
20180325T035121Z
20180325/us-east-1/s3/aws4_request'''+'\n'+canonical_request_hash

signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
print signature  # 30dcf3967d47efecbbe8bfe3f11180cb748e4ef66abf01d7649069bf350394ad

```


![Imgur](https://i.imgur.com/AiFCtPd.png)


```
import urllib
print urllib.quote('!')  # %21
```

```
import urllib
print urllib.quote('!')

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

canonicalrequest = '''PUT
/alpha%21soup/

host:s3.ecloud.today
user-agent:Boto/2.48.0 Python/2.7.5 Linux/3.10.0-693.11.6.el7.x86_64
x-amz-content-sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
x-amz-date:20180325T035121Z

host;user-agent;x-amz-content-sha256;x-amz-date
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

hsh = hashlib.sha256(canonicalrequest.encode())
canonical_request_hash = hsh.hexdigest()  # 8022bfe928617feede7994648f87933711ea8a747ae696acca56baa0a9fb9970


signing_key = getSignatureKey("s3testuser1","20180325","us-east-1","s3")
string_to_sign = '''AWS4-HMAC-SHA256
20180325T035121Z
20180325/us-east-1/s3/aws4_request'''+'\n'+canonical_request_hash

signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
print signature   #2fb2f06d245317d467b3dce4d02b86f53e3dfdbf57434ff542443fe238b3173a
```
