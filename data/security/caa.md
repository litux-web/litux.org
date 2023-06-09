type: article
title: DNS Certificate Authority Authorization (CAA)
last-updated: 2023-04-01 13:01
meta-keywords: CAA, DNS, TLS, SSL, HTTPS, HTTP, Internet Security

Certificate Authority Authorization (CAA) is a DNS based security protocol that allows domain owners to define which entities are allowed to generate certificates.

[DNS Certificate Authority Authorization (CAA)](https://letsencrypt.org/docs/caa/)
> You can set CAA records on your main domain, or at any depth of subdomain. For instance, if you had www.community.example.com, … CAs will check each version, from left to right, and stop as soon as they see any CAA record. … Most people who add CAA records will want to add them to their registered domain (example.com) so that they apply to all subdomains. …

```
example.com IN CAA 0 issue letsencrypt.org
```

The DNS hosting service should have a dedicate `CAA` record type which allows to select between `issue` (only specific hostnames), `wildissue` (only wildcard hostnames), and `iodef` (report violations).

To check the CAA record, use `host` or `dig`:
```
$ host -t CAA litux.org
litux.org has CAA record 0 issue "letsencrypt.org"
litux.org has CAA record 0 iodef "mailto:…@litux.org"

$ dig +short -t CAA litux.org
0 issue "letsencrypt.org"
0 iodef "mailto:…@litux.org"
```

---
## References
* Wikipedia: [DNS Certification Authority Authorization (CAA)](https://en.wikipedia.org/wiki/DNS_Certification_Authority_Authorization)
* Lets Encript: [Certificate Authority Authorization (CAA)](https://letsencrypt.org/docs/caa/)

