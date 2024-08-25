# Cloudflare

This project is served from:

- https://copilot.perpetuator.io

The Staging area is:

- https://copilot-staging.perpetuator.io

## Setup

Register root domains with CloudFlare and then add subdomains etc. in CloudFlare

Go to cloudflare.com

- Add existing domain
- Let it import all DNS settings
- Disable DNSSEC, actually had to disable, remove, and then delete the DNSSEC key before things would work...
  - WAIT 24 HOURS
- Change the DNS servers to Cloudflare's
  - For AWS Route53 two changes: 1) NSes in Hosted Zones and 2) NSes in Registered Domains
- Add the domain to Cloudflare
  - Add the sub-domains, e.g., `copilot.example.io`
  - The IP should point to the server in Cloudflare but Proxy should be on (orange cloud) for security
  - This means that the IP address of the server is hidden
- Now that the domain is in Cloudflare, enable DNSSEC
  - WAIT 24 HOURS
- Enable SSL/TLS
  - Full (strict)
  - Always use HTTPS
  - HTTP Strict Transport Security (HSTS)?
- Enable Firewall
  - Security Level: High
  - Challenge Passage: 30 days
  - Browser Integrity Check: On
  - Hotlink Protection: On
  - IP Geolocation: On
  - WAF: On
  - Rate Limiting: On
  - Bot Management: On
  - Managed Rules: On
- Enable DNSSEC

# Design

Client -> Cloudflare -> AWS/Servers/etc.

This is for load balancing and security.

# Testing the Domain Resolution

The IP address should be the Cloudflare IP addresses...

```shell
dig copilot.example.io
```

# Server Routing

On the server we route to different docker containers using nginx.

To see if nginx is running on the server:

```shell
$ docker ps
eab8c1f9aef6   jrcs/letsencrypt-nginx-proxy-companion  
    letsencrypt
ef12b193518d   jwilder/nginx-proxy                     
    0.0.0.0:80->80/tcp, :::80->80/tcp, 0.0.0.0:443->443/tcp, :::443->443/tcp  nginx-proxy
```

To see the logs for this nginx container it is generally a command like

```shell
cd /opt/multi-host
docker-compose logs -f --tail=10
```

Try to visit the site, if the logs are not showing anything then the site is not being hit. Make sure that the firewall
is not blocking the site and that the port is open.

Once the site is being hit, then you can debug the nginx configuration. The next step is to check the logs for the nginx
container running that specific service. If the logs are not showing anything on that side, then teh routing from nginx
to the container is not working.

Set SSL/TLS encryption mode to : **Full**

> Your plan includes a shared Cloudflare Universal SSL certificate. To get a dedicated certificate with custom hostnames

- We have an active Edge cert, what about: Client and Origin certs?
- If you get 301 redirects and it says too many redirects, then you forgot to do this
