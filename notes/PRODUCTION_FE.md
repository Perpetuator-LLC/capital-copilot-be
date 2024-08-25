# Why front-end in back-end repo?

Currently, because ansible is a python tool and the environment works. An infra repository might be created where both
FE and BE deployment scripts and configuration can be moved to.

# Ansible

For setup see: [ANSIBLE.md](ANSIBLE.md)

To see what deploy will do:

```shell
ansible-playbook deploy-fe.yml --check
```

Then to deploy the Angular server:

```shell
ansible-playbook deploy-fe.yml 
```

# Production Deployment

The [WAF.md](WAF.md) explains the network setup. This document explains the deployment process.

## Django Debug in Container

To see the logs and follow:

```shell
docker-compose logs -f
```

To debug inside the container:

```shell
docker exec -it copilot_fe_angular sh
```

```shell
docker-compose up -d --build
```

# Docker Compose Invocation

To control the port the Angular server is running on (`4200` by default):

```shell
COPILOT_ANGULAR_PORT=4321 docker-compose up -d --build
```

NOTE: Internally the port is set to 80. We can serve to a different port on the server, but we have to tell the nginx
host to forward to the correct port. All traffic routed to port 80 on the server will be forwarded to the Angular
server/appropriate container for handling from an nginx reverse proxy.

Even though it is served on port 80, the Angular server is running on port 4200 or the specified port. You could visit
the site at:

```shell
http://192.168.1.123:4200
```

# Back-up

To back-up the database we need to run:

```shell
cp db.sqlite3{,-$(date +%Y%m%d)}
```

The `.env` file should be backed up too.

# Debug in Container

To see the logs and follow:

```shell
docker-compose logs -f
```

```shell
docker exec -it copilot_fe_angular sh
```
