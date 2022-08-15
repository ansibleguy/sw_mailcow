<a href="https://mailcow.email/">
<img src="https://mailcow.email/img/cow_mailcow.svg" alt="MailCow Logo" width="300"/>
</a>

# Ansible Role - MailCow

Role to deploy [MailCow dockerized](https://github.com/mailcow/mailcow-dockerized) on a linux server.

[![Molecule Test Status](https://badges.ansibleguy.net/sw_mailcow.molecule.svg)](https://molecule.readthedocs.io/en/latest/)
[![YamlLint Test Status](https://badges.ansibleguy.net/sw_mailcow.yamllint.svg)](https://yamllint.readthedocs.io/en/stable/)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/sw_mailcow.ansiblelint.svg)](https://ansible-lint.readthedocs.io/en/latest/)
[![Ansible Galaxy](https://img.shields.io/ansible/role/60006)](https://galaxy.ansible.com/ansibleguy/sw_mailcow)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F60006%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/sw_mailcow)


**Tested:**
* Debian 11

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * Service to start containers on boot: 'mailcow.service'


  * **Default config**:
    * Directories:
      * Base: '/var/lib/mailcow'
      * Data: '/var/lib/docker/volumes' (_cannot be changed by role_)


  * **Default opt-ins**:
    * Docker => using [THIS Role](https://github.com/ansibleguy/infra_docker_minimal)
      * Dependencies
      * Server
      * Docker-compose
    * Nginx proxy on docker-host => using [THIS Role](https://github.com/ansibleguy/infra_nginx)
  
    * Features:
      * [SOGo Groupware](https://www.sogo.nu/)
      * Apache Solr
      * ClamAV (_virus scanner_)
  
    * IPv6 enabled


## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** Default credentials:

  User: admin
  Password: moohoo


* **Info:** For more detailed information - look into the [nice documentation](https://mailcow.github.io/mailcow-dockerized-docs) provided by MailCow!


* **Info:** If the setup fails after creating the config - you need to remove the config file (_/var/lib/mailcow/mailcow.conf_) manually, so the role will know it isn't initialized already!


## Prerequisites

See: [Prerequisites](https://github.com/ansibleguy/sw_mailcow/blob/stable/Prerequisites.md)


## Setup

For this role to work - you must install its dependencies first:

```
ansible-galaxy install -r requirements.yml
```


## Usage

### Config

Define the config as needed:

```yaml
mailcow:
  fqdn: 'srv.template.ansibleguy.net'
  # per example: 'srv.template.ansibleguy.net' must be a valid, public dns-hostname of the server

  nginx:  # configure the webserver settings => see: https://github.com/ansibleguy/infra_nginx
    aliases: ['mail.template.ansibleguy.net']  # additional domains to add to the certificate
    ssl:
      mode: 'letsencrypt'  # or selfsigned/ca
      #  if you use 'selfsigned' or 'ca':
      #    cert:
      #      cn: 'MailCow Server'
      #      org: 'AnsibleGuy'
      #      email: 'mailcow@template.ansibleguy.net'
    letsencrypt:
      email: 'mailcow@template.ansibleguy.net'
```

Bare minimum example:
```yaml
mailcow:
  fqdn: 'srv.template.ansibleguy.net'
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* docker
* webserver

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
