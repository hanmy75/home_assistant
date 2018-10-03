#! /bin/bash

# Disable nginx
systemctl stop nginx

# Renew cert
certbot renew --quiet

# Enable nginx
systemctl start nginx
