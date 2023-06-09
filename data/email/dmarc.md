type: article
title: DMARC (Domain-based Message Authentication, Reporting and Conformance)
last-updated: 2023-04-01 12:03
meta-keywords: DMARC, DNS, email, security

DMARC (Domain-based Message Authentication, Reporting and Conformance) is an email authentication and security protocol used in conjunction with [SPF](spf) and [DKIM](dkim) so that emails that fail the authentication can be reported back to the domain owner, or to many services that can generate reports out of those emails.

DMARC is a `TXT` record added to the domain's DNS into the name `_dmarc`.

```
_dmarc.example.com IN TXT "v=DMARC1; p=quarantine; rua=mailto:xxx@example.com,mailto:yyy@zzz; pct=100; ri=86400"
```

## Policy
The `p` parameter is used by email servers to decide what to do with the message.
* `none` to do nothing
* `reject` to reject the message
* `quarantine` to flag the message, which can mean marking it as spam or storing it in a separate folder

The `pct` parameter should remain at 100(%) for low-traffic domains so the protocol applies to all messages.

The `ri` parameter is a hint on how often to report the failed messages. The value of `86400`, daily, is a good default value.

To check the DMARC record, use `host` or `dig`:
```
$ host -t TXT _dmarc.litux.org
_dmarc.litux.org descriptive text "v=DMARC1;p=quarantine;rua=mailto:…@litux.org,mailto:…;pct=100;ri=86400"

$ dig +short -t TXT _dmarc.litux.org
"v=DMARC1;p=quarantine;rua=mailto:…@litux.org,mailto:…;pct=100;ri=86400"```
```

---
## Tools
* AnubisNetworks: [DMARC Domain Verification](https://anti.phishing.pt/pt/domain_verify/domain_verification)
---
## References
* Wikipedia: [DMARC (Domain-based Message Authentication, Reporting and Conformance)](https://en.wikipedia.org/wiki/DMARC)

