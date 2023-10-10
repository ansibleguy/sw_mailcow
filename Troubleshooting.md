# Troubleshooting

## Self-Signed certificate expired

If IMAP/SMTP stops working and you are using no ACME/LetsEncrypt, this might be it.

```bash
# check
openssl x509 -in /var/lib/mailcow/data/assets/ssl/cert.pem -text

# renew
cd /var/lib/mailcow/data/assets/ssl
openssl req -new -key key.pem -out cert.csr
openssl x509 -req -in cert.csr -signkey key.pem -out cert.pem -days 720
# re-check
openssl x509 -in /var/lib/mailcow/data/assets/ssl/cert.pem -text

systemctl restart mailcow.service
```
