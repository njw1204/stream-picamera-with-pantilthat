import hashlib, hmac, base64

def SHA256(message):
    message = message.encode('utf-8')
    return hashlib.sha256(message).hexdigest()


def HMAC_SHA256(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')
    return hmac.new(key, message, hashlib.sha256).digest()


def Base64Encode(message, urlSafe=False, ignorePadding=False):
    if type(message) == str:
        bt = message.encode('utf-8')
    else:
        bt = message

    if urlSafe:
        b64 = str(base64.urlsafe_b64encode(bt), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(bt), encoding='utf-8')

    if ignorePadding:
        return b64.rstrip('=')
    else:
        return b64


def Base64Decode(message, urlSafe=False):
    # if not Base64 string, raise Exception
    message += '==='
    if urlSafe:
        bt = base64.urlsafe_b64decode(message)
    else:
        bt = base64.b64decode(message)
    return str(bt, encoding='utf-8')