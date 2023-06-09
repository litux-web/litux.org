type: article
title: Hosting static websites on GitHub Pages
last-updated: 2023-04-01 14:01
meta-keywords: GitHub Pages

GitHub allows to publish a website with static pages under either their own domain (your_username.github.io) or with your own domain. They also provide HTTPS support, including generating automatically an SSL certificate from Lets Encrypt.

---

FIXME WIP


## Setup DNS records

GitHub provides the website under <your-github-account>.github.io

subdomain CNAME <your-github-account>.github.io

Protect the subdomain with a [SPF](/email/spf) record
subdomain TXT v=spf1 -all

If the site is the primary one `www`, also set the domain
domain CNAME <your-github-account>.github.io
this is not allowed according to the DNS RFS but many DNS hosting will expand or flatten into the `A` and `AAAA` records.
if not, add them manually
 host -t A davipt.github.io
davipt.github.io has address 185.199.111.153
davipt.github.io has address 185.199.110.153
davipt.github.io has address 185.199.108.153
davipt.github.io has address 185.199.109.153
idavi:litux.org bruno$ host -t AAAA davipt.github.io
davipt.github.io has IPv6 address 2606:50c0:8001::153
davipt.github.io has IPv6 address 2606:50c0:8000::153
davipt.github.io has IPv6 address 2606:50c0:8002::153
davipt.github.io has IPv6 address 2606:50c0:8003::153

Add a [CAA](/security/caa) record so GitHub and LetsEncrypt can generate a SSL certificate
subdomain CAA 0 issue letsencrypt.org
also add one to the root domain
domain CAA 0 issuewild letsencrypt.org

If using CloudFlare, set the CNAME (or A + AAAA) records to NOT be proxied for now

## Setup GitHub repository
create a new repository

create a default README.md and set it to something welcoming to other people, also adding the domain so it can easily distinguishable from other repositories
`echo '# mydomain' > README.md`

create a new branch docs so the website updates do not pollute the home of the repository on GitHub

create a folder docs

add a file `CNAME` with the domain name
`echo mydomain.com > docs/CNAME`

don't add all content yet. add a dummy index inside for testing
`echo "Hello World" > docs/index.html`

commit and push the `docs` branch

## Setup GitHub Pages

Go to GitHub, "Repository", "Settings", "Pages"

On "Build and deployment" ensure "Deploy from a branch"

Set the branch to `docs` and the folder to `/docs` and click `Save`

The "Custom domain" field should be pre-populated already, from the `docs/CNAME` file that was committed.

GitHub should report "DNS check successful".
If not… FIXME

Enable "Enforce HTTPS"
If the option is not available:
* ensure the CAA records are set up correctly
```
$ host -t CAA mta-sts.litux.org
mta-sts.litux.org has CAA record 0 issue "letsencrypt.org"
$ host -t CAA litux.org
litux.org has CAA record 0 issue "pki.goog; cansignhttpexchanges=yes"
litux.org has CAA record 0 issuewild "comodoca.com"
litux.org has CAA record 0 issuewild "digicert.com; cansignhttpexchanges=yes"
litux.org has CAA record 0 issuewild "letsencrypt.org"
litux.org has CAA record 0 issuewild "pki.goog; cansignhttpexchanges=yes"
litux.org has CAA record 0 issue "comodoca.com"
litux.org has CAA record 0 issue "digicert.com; cansignhttpexchanges=yes"
litux.org has CAA record 0 issue "letsencrypt.org"
```
* ensure CloudFlare proxy is disable, so GitHub can see the original CNAME (A / AAAA) record pointing to github.io and not to CloudFlare

## Enable Website

the page will only be deployed upon updates on the branch
change the index.html or add more content, commit and push
go to GitHub repository, Actions, and check if the "pages build and deployment" ran and was successful

on your browser visit your domain and verify the content is correct
try loading the site as http and ensure it gets redirected to https
for the root domain with www, also check if the domain redirects to www.domain, with and without https

## Customized Action

to customize the action e.g. to run some code that auto-generates files into docs, see [GitHub Pages with Custom Action](/web/github-pages-action)

a custom action is also required in case there's dot files under docs, as the default action will not pick them up. This is required e.g. for [MTA-STS](/email/mta-sts) that needs a `.well.known/mta-sts.txt`


