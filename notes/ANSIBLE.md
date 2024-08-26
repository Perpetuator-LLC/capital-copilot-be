# Ansible Installation

```shell
poetry shell
poetry add --dev ansible
```

Another option (not yet tested) if you don't want to use Python then run it from a docker container:

```shell
docker run -it --rm -v $(pwd):/ansible -w /ansible ansible/ansible:latest ansible-playbook -i hosts.ini setup.yml
```

# Secrets Management

```shell
ansible-vault create stage.secret.yml
ansible-vault edit stage.secret.yml
```

# Running a Playbook

## First create the hosts file

```shell
cp hosts.ini.example hosts.ini
```

Then update the `hosts.ini` file with the IP address of the server.

```ini
```

## To deploy the Django server

```shell
ansible-playbook -i prod.hosts.ini deploy-be.yml --check
```

The password file and inventory file can be set in the `ansible.cfg` file.

```shell
[defaults]
inventory = prod.hosts.ini
vault_password_file = ~/.ans.copilot.pass.txt
```

Then to debug the server:

```shell
ansible-playbook deploy-be.yml --check -vvv
```

To debug variables, use the `debug` module:

```yaml
- name: Display all variables/facts collected for a host
  debug:
    var: hostvars[inventory_hostname]
  tags: always
```
