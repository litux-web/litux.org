type: article
title: Domain Name System Security Extensions (DNSSEC)
last-updated: 2023-04-01 13:02
meta-keywords: DNSSEC, DNS, Internet Security

Domain Name System Security Extensions (DNSSEC) is a security protocol extension for DNS to provide authentication and data integrity of DNS records.

Enabling DNSSEC for a domain is not a simple task like other security protocols like [SPF](/email/spf) or [CAA](/security/caa), but requires cooperation both from the DNS hosting service, as well as the DNS registrar. This means it might be necessary to switch DNS hosting service and even the registrar in case they do not support the feature.

The DNS hosting service needs to support DNSSEC because the protocol will add many DNS security records for each existing record, therefore not something we'd want to be performed manually.

The DNS registrar needs to support DNSSEC because there will be a DNS record together with the existing `NS` records managed by the registar. In other words, the certificate chain of trust relies on the top level domains having keys to verify the authenticity of the keys on the upper levels. For example, root certifies `uk`, then `uk` certifies `uk.com`, then `uk.com` certifies the public domains under it.

## DNS Registars
* [NetworkSolutions](https://www.networksolutions.com) seems to provide DNSSEC as a paid extension - Premium DNS at $3.99 or $4.99 per month. It's not easy to find reliable information.
* [DNS.pt](https://www.pt.pt/pt/) provides DNSSEC support for free

## DNS Hosting Services
* [ZoneEdit] seems to provide a [DNSSEC beta](https://support.zoneedit.com/en/knowledgebase/article/dnssec) for paid customers but also seems to require the domain to be registered with them. As a free customer, I don't even see the option.
* [Cloudflare](https://www.cloudflare.com) provides [DNSSEC](https://developers.cloudflare.com/dns/dnssec/) for free and as simple as (almost) a single click, so long the DNS is being managed by them. They do not need to be the registrar. Upon enabling DNSSEC, CloudFlare provides the required information to add to the registrar.

---
## Tools
* AnubisNetworks: [DNSSEC Domain Verification](https://anti.phishing.pt/pt/domain_verify/domain_verification)
* Verisign Labs: [DNSSEC Analyzer](https://dnssec-analyzer.verisignlabs.com/)
---
## References
* Wikipedia: [Domain Name System Security Extensions (DNSSEC)](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions)

