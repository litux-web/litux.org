type: article
title: GitHub Pages with Custom Actions
last-updated: 2023-04-01 14:02
meta-keywords: GitHub Pages

[GitHub Pages](github-pages) uses a default action to publish static content that uses Jekyll templates and, at the moment, can't cope with files or folders with a leading dot.

The transition to a customizable action is simple, allowing the freedom and to be extended with addicional features, including but not limited to using our own code to generate or process the content, support for dot files, and additional jobs like notifications upon completion.

---

[GitHub Pages](/web/github-pages)

To run code that dynamically generates content inside the `docs` folder, or to personalize the deployment, or to include dot files (see [MTA-STS](/email/mta-sts)), a custom action is required.

After setting up the default GitHub Pages action according to [GitHub Pages](/web/github-pages), so GitHub gets automatically setup in regards of environments and other stuff, reconfigure it to use a dedicated action

On "Settings", "Pages", switch "Source" from "Deploy from a branch" to "GitHub Actions (beta)". Do not pick any suggested workflow.

Verify the Custom Domain is still setup correctly and GitHub reports "DNS check successful" and "Enforce HTTPS" is enabled.

On the `docs` branch, add a new file under `.github/workflows/` with `.yml` extension, e.g. simply `main.yml`

Add and adjust the following content:
```
on:
  workflow_dispatch:

  # runs upon push into the "docs" branch
  push:
    branches: [ "docs" ]

jobs:

  build:
    name: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        # enable if the repository uses submodules
        #with:
        #  submodules: true

      # build your content here
      #- name: do stuff
      #  run: echo hello world > docs/index.html

      - name: Upload GitHub Pages artifact
        uses: actions/upload-pages-artifact@v1.0.8
        with:
          path: "docs"

  deploy:
    needs: build
    name: deploy
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    permissions:
      pages: write
      id-token: write
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2

      # perform additional actions after deploy e.g. notification via IFTTT
      #- name: IFTTT Webhook
      #  uses: alfredosalzillo/ifttt-webhook-action@v1
      #  with:
      #    event: ${{ secrets.IFTTT_EVENT }}
      #    key: ${{ secrets.IFTTT_KEY }}
      #    value1: "Deploy complete"
      #    value2: ${{ steps.deployment.outputs.page_url }}
      #    value3: ""
```

## Environment

if the action requires secrets e.g. on the example above the IFTTT event and key go to `Environments` a there should be already a `githup-pages` environment setup when the default GitHub Pages ran the first time

Click on the environment name and add the key and values into the "Environment secrets" section. For the example above, `IFTTT_EVENT` and `IFTTT_KEY`

Take the opportunity to remove the `main` branch from the `Deployment branches` section, leaving only the `docs` branch.

## Setup action

commit and push the `.github/workflows/main.yml` file into the `docs` branch

Go to GitHub Actions and check the action running. The title will be the commit's first line

