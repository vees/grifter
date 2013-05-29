import base64, string, hashlib, binascii

#base64.b32encode(hashlib.md5('test').digest())[:-6].translate(string.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567","0123456789ABCDEFGHJKMNPQRSTVWXYZ"),"=").lower()

__std2crock = string.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
)
__crock2std = string.maketrans(
    "0123456789ABCDEFGHJKMNPQRSTVWXYZ",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
)

def b32encode(s):
    return base64.b32encode(s).translate(__std2crock, '=').lower()

def b32decode(b32, casefold=None, map01=None):
    # Ensure the manatory padding is correct:
    b32=b32.upper()
    b32 += '=' * ((8 - len(b32) % 8) % 8)
    return base64.b32decode(b32.translate(__crock2std),
        casefold=casefold, map01=map01)

if __name__ == '__main__':
    #binascii.a2b_hex("00000000000000000000000000000000")
    hello = hashlib.md5('hello world')
    print hello.hexdigest()
    print b32encode(hello.digest())
    print b32decode('btv3qez03vqd14yb4axryppdrc').encode('hex')

