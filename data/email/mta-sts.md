type: article
title: MTA-STS (MTA Strict Transport Security)
last-updated: 2023-04-01 12:04
meta-keywords: MTA-STS, DNS, email, security

MTA-STS (MTA Strict Transport Security) is an email authentication and security protocol used to signal the desire to use encrypted channels in between email server.

MTA-STS needs two `TXT` records added to the domain's DNS into the name `_mta-sts` and `_smtp._tls`, in conjunction with a dedicated HTTPS server and sub-domain to host the policy file.

```
_mta-sts.example.com IN TXT "v=STSv1; id=20230601000000"
_smtp._tls.example.com IN TXT "v=TLSRPTv1; rua=mailto:…@example.com"
```

The `id` is a unique value (here, a date-time) that shall be changed in case the policy changes.

The `rua` is an email address used to receive reports about failed emails, similar to the parameter in [DKIM](dkim).

The policy definition needs to be hosted on an HTTPS server under the sub-domain `mta-sts` and inside a file called `mta-sts.txt` under a folder `.well-known`. The website shall be available using HTTPS and a valid certificate.


To check the MTA-STS record, use `host` or `dig`:
```
$ host -t TXT _mta-sts.litux.org
_mta-sts.litux.org descriptive text "v=STSv1; id=20230601000000"
$ host -t TXT _smtp._tls.litux.org
_smtp._tls.litux.org descriptive text "v=TLSRPTv1; rua=mailto:…@litux.org"

$ dig +short -t TXT _mta-sts.litux.org
"v=STSv1; id=20230601000000"
$ dig +short -t TXT _smtp._tls.litux.org
"v=TLSRPTv1; rua=mailto:…@litux.org"
```

To check the MTA-STS policy use `curl` or `wget` or a browser:
```
$ curl -s 'https://mta-sts.litux.org/.well-known/mta-sts.txt'
version: STSv1
mode: enforce
mx: …
max_age: 604800
```

A simple and free website can be provisioned through GitHub Pages.

However, the default `pages` action does not deploy folders with a leading dot unless a config file `_config.yml` is added. [José Ferreira](https://github.com/jcbf/) from [AnubisNetworks](https://www.anubisnetworks.com) has a ready-made template at [MTA-STS Website template using GitHub Pages](https://github.com/jcbf/jcbf-mta-sts).

An alternative is to use a dedicated and extendable action. See [GitHub Pages](/web/github-pages) and [GitHub Pages Action](/web/github-pages-action), as well as this site's [mta.sts.litux.org action workflow](https://github.com/litux-web/mta-sts.litux.org/blob/docs/.github/workflows/main.yml).

The MTA-STS DNS and website can be validated using Google if the domain is set up on Google Workspace under "Apps" - "Google Workspace" - "Gmail" - "Compliance" and at the end of the page there is a link to [nofollow:validate MTA-STS](https://admin.google.com/ac/apps/cs/diagnostic).
Note: the Google Workspace Admin Help mentions a "Security Health" page but the Google Workspace "legacy" does not show any item there.

---
## Tools
* AnubisNetworks: [MTA-STS Domain Verification](https://anti.phishing.pt/pt/domain_verify/domain_verification)
* AnubisNetworks: [MTA-STS Website template using GitHub Pages](https://github.com/jcbf/jcbf-mta-sts)
* Litux.org: [MTA-STS Website using GitHub Pages](https://github.com/litux-web/mta-sts.litux.org) and the [mta-sts action](https://github.com/litux-web/mta-sts.litux.org/blob/docs/.github/workflows/main.yml) to support the `.well-known` folder with a leading dot
* Google Workspace Admin Help: [Turn on MTA-STS and TLS reporting](https://support.google.com/a/answer/9276512)
* Google Workspace Admin Help: [Check your MTA-STS configuration](https://support.google.com/a/answer/9276419)
---
## References
* Wikipedia: [MTA-STS (MTA Strict Transport Security)](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol#SMTP_MTA_Strict_Transport_Security)
* Freddie Leeman: [MTA-STS explained](https://www.uriports.com/blog/mta-sts-explained/) (2019-04-18)

