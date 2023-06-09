type: article
title: SPF (Sender Policy Framework)
last-updated: 2023-04-01 12:01
meta-keywords: SPF, DNS, email, security

SPF (Sender Policy Framework) is an email authentication and security protocol that allows domain owners to explicitly declare which email servers are allowed to send emails to the given domain.

This allows email servers to consult this information and decide if an email should be accepted, rejected, or flagged as suspicious.

SPF is a DNS TXT record added to the domain.

For each domain and subdomain not supposed to be used to send emails (e.g. "www") set a TXT record rejecting any email. Lookout for any DNS record for CNAME, A, or AAAA
```
example.com IN TXT "v=spf1 -all"
```

For each domain supposed to send emails, add a TXT record with a list of servers allowed to send emails.
```
example.com IN TXT "v=spf1 […allowed servers…] -all"
```

In many cases the email is delegated to some service, so we can include their own shared SPF record.
* Google: `include:_spf.google.com`
* iCloud:  `include:icloud.com`

An acceptable security level is either reject or flag emails sent from non-authorized servers. This means ideally the `-all`, but in some situations, it might be needed to use `~all` to avoid rejecting legitimate emails.

To check the SPF record, use `host` or `dig`:
```
$ host -t TXT litux.org | grep spf
litux.org descriptive text "v=spf1 include:_spf.google.com include:icloud.com -all"

$ dig +short -t TXT litux.org | grep spf
"v=spf1 include:_spf.google.com include:icloud.com -all"
```

---
## Tools
* AnubisNetworks: [SPF Domain Verification](https://anti.phishing.pt/pt/domain_verify/domain_verification)
---
## References
* Wikipedia: [SPF (Sender Policy Framework)](https://en.wikipedia.org/wiki/Sender_Policy_Framework)

