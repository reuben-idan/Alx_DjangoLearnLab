# Deployment Configuration

To enable HTTPS, you need to configure your web server (e.g., Apache or Nginx) to use SSL/TLS certificates.

## Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/ssl_certificate.crt;
    ssl_certificate_key /path/to/your/ssl_certificate.key;

    # ... other configurations ...
}
```

## Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    SSLEngine on
    SSLCertificateFile /path/to/your/ssl_certificate.crt
    SSLCertificateKeyFile /path/to/your/ssl_certificate.key
    # ... other configurations ...
</VirtualHost>
```

Replace `/path/to/your/ssl_certificate.crt` and `/path/to/your/ssl_certificate.key` with the actual paths to your SSL certificate and key files.