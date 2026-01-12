# Nginx Configuration Guide

How to deploy the UCP Merchant behind Nginx.

## Basic Proxy Setup

Add this to your Nginx site configuration:

```nginx
server {
    server_name yourdomain.com;

    # UCP API - Proxy to Flask app
    location /api/ucp/ {
        proxy_pass http://127.0.0.1:5000/api/ucp/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS headers for cross-origin API access
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization, UCP-Agent" always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    # UCP Discovery file at standard location
    location /.well-known/ucp.json {
        proxy_pass http://127.0.0.1:5000/api/ucp/discovery;
        proxy_set_header Host $host;
        add_header Access-Control-Allow-Origin "*" always;
    }

    # ... rest of your site config
}
```

## With SSL (Let's Encrypt)

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # UCP API
    location /api/ucp/ {
        proxy_pass http://127.0.0.1:5000/api/ucp/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;

        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    location /.well-known/ucp.json {
        proxy_pass http://127.0.0.1:5000/api/ucp/discovery;
        proxy_set_header Host $host;
        add_header Access-Control-Allow-Origin "*" always;
    }
}

# HTTP redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
```

## Proxy to Remote Server

If running the Flask app on a different server:

```nginx
location /api/ucp/ {
    proxy_pass https://your-ucp-server.com/api/ucp/;
    proxy_set_header Host your-ucp-server.com;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_ssl_server_name on;  # Important for HTTPS upstream

    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type" always;

    if ($request_method = 'OPTIONS') {
        return 204;
    }
}
```

## Testing Configuration

```bash
# Test config syntax
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Test the API
curl https://yourdomain.com/api/ucp/health
curl https://yourdomain.com/.well-known/ucp.json
```

## Systemd Service

Create `/etc/systemd/system/ucp-merchant.service`:

```ini
[Unit]
Description=UCP Merchant Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ucp-merchant
ExecStart=/path/to/ucp-merchant/venv/bin/python src/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ucp-merchant
sudo systemctl start ucp-merchant
```

## With Gunicorn (Production)

For production, use Gunicorn instead of the Flask dev server:

```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 src.app:app
```

Systemd service with Gunicorn:

```ini
[Unit]
Description=UCP Merchant (Gunicorn)
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ucp-merchant
ExecStart=/path/to/ucp-merchant/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 src.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
