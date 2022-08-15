# Prerequisites


## System requirements

Make sure your target system meets the [system requirements](https://mailcow.github.io/mailcow-dockerized-docs/prerequisite/prerequisite-system/)!

  - The target system must be a VM or bare-metal server
  - The target system needs to have a public IP.
  - You need to have a public Domain.
  - You might want to create a dedicated volume (_maybe use [LVM](https://linuxconfig.org/linux-lvm-logical-volume-manager)_) for the data-directory (_/var/lib/docker/volumes_) - so you can easier extend/manage it.
  - ...

## Firewalling

See also: [Documentation](https://mailcow.github.io/mailcow-dockerized-docs/prerequisite/prerequisite-system/#default-ports)

### Inbound

For the server to work, you must allow the following ports using your firewall:

  - For web access: 80/tcp, 443/tcp+udp (_443 can be GeoIP/sourceIP restricted, 80 needs to be open if you are using LetsEncrypt/ACME_)
  - Mailing basic: 25/tcp, 587/tcp, 465/tcp from ANY
  - POP/IMAP over SSL: 993/tcp, 995/tcp
  - POP/IMAP with StartTLS: 110/tcp, 143/tcp

Note:
> As mailcow runs dockerized, INPUT rules have no effect on restricting access to mailcow.
Use the FORWARD chain instead.

### Outbound

**If you want** to filter outbound connections using your firewall - you will need to allow:

- Installation: while running the initial installation => please allow 80/tcp 443/tcp+udp to ANY
- Basics:
  - DNS: 53/tcp+udp to Internet (_could not find information on what servers are used_)
  - NTP: 123/udp to 0.debian.pool.ntp.org and 0.debian.pool.ntp.org
  - APT: 443/tcp+udp to deb.debian.org and security.debian.org (_or whatever main repository you are using_)
- Proxmox: 443/tcp+udp to download.proxmox.com and enterprise.proxmox.com (_tbc.._)
- Mailing: 25/tcp to Internet
- LetsEncrypt: 443/tcp+udp to acme-v02.api.letsencrypt.org and staging-v02.api.letsencrypt.org (_debug mode_)
- ClamAV: 443/tcp+udp to database.clamav.net
- SpamAssassin: 80/tcp, 443/tcp+udp to spamassassin.apache.org and domains listed in the [mirror list](https://spamassassin.apache.org/updates/MIRRORED.BY)
- CloudMark Razor: 2703/tcp to discovery.razor.cloudmark.com and CURRENTLY 208.83.137.0/24
- to be continued..

## Public DNS

To filter incoming and outgoing mails, the Proxmox Mail Gateway needs to be configured as public mailserver!

Mailcow's documentation to DNS: [LINK](https://mailcow.github.io/mailcow-dockerized-docs/prerequisite/prerequisite-dns/)

If you are interested => here's a nice overview of SPF/DKIM/DMARC: [LINK](https://seanthegeek.net/459/demystifying-dmarc/)

**Needed**:

| TYPE | KEY                             | VALUE                                          | COMMENT                                                                                                                                                                                                                                       |
|:----:|:--------------------------------|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  A   |  SRV.DOMAIN.TLD                 | SRV-PUBLIC-IP                                  | -                                                                                                                                                                                                                                             |
|  MX  | DOMAIN.TLD                 | 10 SRV.DOMAIN.TLD                              | -                                                                                                                                                                                                                                             |
| TXT  | DOMAIN.TLD                 | v=spf1 mx -all                                 | -                                                                                                                                                                                                                                             |
| TXT  | _dmarc.DOMAIN.TLD          | v=DMARC1; p=quarantine; aspf=s; adkim=s;       | You can also add a dedicated mail user to receive DMARC reports. See the 'overview' above for details. It would then look like this: 'v=DMARC1; p=quarantine; rua=mailto:ADDRESS@DOMAIN.TLD; ruf=mailto:ADDRESS@DOMAIN.TLD; aspf=s; adkim=s;' |
| TXT  | dkim._domainkey.DOMAIN.TLD | v=DKIM1; p=MIIBIjANBgkqhkiG...                 | Replace the value by YOUR DKIM record!                                                                                                                                                                                                        |
| TXT  | *.DOMAIN.TLD               | v=spf1 -all                                    | Any domain/subdomain that is not used to send mails, should IMPLICITLY DENY any senders!                                                                                                                                                      |
| PTR  | YOUR-SRV-IP | SRV.DOMAIN.TLD | You cannot set a PTR record in your DNS-Panel/management! Your internet provider/hoster has to do that. Bigger hosters will give you an option for this in their managment interface.                                                         |

**Optional**:

| TYPE | KEY                         | VALUE                                       | COMMENT                                                                                                                                                |
|:----:|:----------------------------|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
|  CNAME | PRETTY_NAME.DOMAIN.TLD      | SRV.DOMAIN.TLD                              | Just a pretty name for the webmail if your server-name isn't that nice                                                                                 |
|  CNAME | autodiscover.DOMAIN.TLD     | SRV.DOMAIN.TLD                      | If you use a mail-client (_outlook_)                                                                                                                   |
|  CNAME | autoconfig.DOMAIN.TLD       | SRV.DOMAIN.TLD                      | If you use a mail-client (_kmail, ..._)                                                                                                                |

