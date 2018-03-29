from OpenSSL import crypto
from socket import gethostname
"""
voir aussi:
http://www.yothenberg.com/validate-x509-certificate-in-python/
"""

k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

cert = crypto.X509()
cert.get_subject().C = "FR"
cert.get_subject().ST = "grenoble"
cert.get_subject().O = "atos"
cert.get_subject().OU = "worldgrid"
cert.get_subject().CN = gethostname()
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years expiry date
cert.set_issuer(cert.get_subject())  # self-sign this certificate

cert.set_pubkey(k)
cert.sign(k, 'sha256')
# pass certificate around, but of course keep private.key
open("selfsign.crt", 'wt').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
open("private.key", 'wt').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

# Now the real world use case; use certificate to verify signature
f = open("private.key")
pv_buf = f.read()
f.close()
priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, pv_buf)

f = open("selfsign.crt")
ss_buf = f.read()
f.close()
ss_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ss_buf)

# sign and verify PASS
sig = crypto.sign(priv_key, 'ninovsnino', 'sha256')
crypto.verify(ss_cert, sig, 'ninovsnino', 'sha256')

# sign and verify FAIL; bad hash
sig_bad = crypto.sign(priv_key, 'ninovsnino', 'sha1')
crypto.verify(ss_cert, sig_bad, 'ninovsnino', 'sha256') # Error: [('rsa routines', 'INT_RSA_VERIFY', 'algorithm mismatch')]

# sign and verify FAIL; bad message
sig_bad = crypto.sign(priv_key, 'ninovsnina', 'sha256')
crypto.verify(ss_cert, sig_bad, 'ninovsnino', 'sha256') # Error: [('rsa routines', 'INT_RSA_VERIFY', 'bad signature')]