<a href="https://mailcow.email/">
<img src="https://www.servercow.de/img/cow_mailcow.svg" alt="MailCow Logo" width="300"/>
</a>

# Ansible Role - MailCow

Role to deploy [MailCow dockerized](https://github.com/mailcow/mailcow-dockerized) on a linux server.

This role follows the official [installation instructions](https://mailcow.github.io/mailcow-dockerized-docs/de/i_u_m/i_u_m_install/).

[![Molecule Test Status](https://badges.ansibleguy.net/sw_mailcow.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/sw_mailcow.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/sw_mailcow.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/sw_mailcow.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://badges.ansibleguy.net/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/ansibleguy/sw_mailcow)


**Tested:**
* Debian 11

## Install

```bash
ansible-galaxy install ansibleguy.sw_mailcow

# or to custom role-path
ansible-galaxy install ansibleguy.sw_mailcow --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * Service to start containers on boot: 'mailcow.service'


  * **Default config**:
    * Directories:
      * Base: '/var/lib/mailcow'
      * Data: '/var/lib/docker/volumes' (_cannot be changed by role_)
      * Backup: '/var/backups/mailcow'


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
    * Daily backup using the [backup script](https://mailcow.github.io/mailcow-dockerized-docs/backup_restore/b_n_r-backup/)
    
  * **Default opt-outs**:
    * Auto update using the [update script](https://mailcow.github.io/mailcow-dockerized-docs/i_u_m/i_u_m_update/)  (_NOTE: actually working very well!_)


## Info

* **Info:** Consider using a **Mail Gateway to gain Security**!

  Per example: [Proxmox Mail Gateway](https://github.com/ansibleguy/sw_proxmox_mail_gw)


* **Info:** Check out the troubleshooting information: [Troubleshooting](https://github.com/ansibleguy/sw_mailcow/blob/stable/Troubleshooting.md)

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:** Default credentials:

  User: admin

  Password: moohoo


* **Info:** For more detailed information - look into the [nice documentation](https://mailcow.github.io/mailcow-dockerized-docs) provided by MailCow!


* **Info:** If the setup fails after creating the config - you need to remove the config file (_/var/lib/mailcow/mailcow.conf_) manually, so the role will know it isn't initialized already!


* **Warning:** The automatic **BACKUPS** are placed on the same system and need to be copied to a **REMOTE** location to be SAFE!


## Prerequisites

See: [Prerequisites](https://github.com/ansibleguy/sw_mailcow/blob/stable/Prerequisites.md)


## Usage

### Config

Define the config as needed:

```yaml
mailcow:
  fqdn: 'srv.template.ansibleguy.net'
  # per example: 'srv.template.ansibleguy.net' must be a valid, public dns-hostname of the server

  # if you don't have IPv6
  ipv6: false  

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

  config:  # add config overrides for 'mailcow.conf'
    WEBAUTHN_ONLY_TRUSTED_VENDORS: 'y'

  auto_update:
    enable: true  # enable auto-updates

  backup:
    retention_days: 60  # default = 14
```

Bare minimum example:
```yaml
mailcow:
  fqdn: 'srv.template.ansibleguy.net'
```

If you want to use the built-in (_not ansible-managed_) webserver:
```yaml
mailcow:
  fqdn: 'srv.template.ansibleguy.net'
  # per example: 'srv.template.ansibleguy.net' must be a valid, public dns-hostname of the server

  manage:
    webserver: false

  config:
    HTTP_PORT: 80
    HTTPS_PORT: 443
    # if you want to use the built-in letsencrypt support
    SKIP_LETS_ENCRYPT: 'n'
    ACME_CONTACT: 'mailcow@template.ansibleguy.net'
    ADDITIONAL_SAN: 'smtp.template.ansibleguy.net,mail.*'
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
