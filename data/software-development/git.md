type: article
title: GIT
last-updated: 2023-04-01 15:01
meta-keywords: git

FIXME WIP

## sudo push
git push --force

## multiple accounts
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_other" git push --force
via .ssh/config ?
SuperUser Question: [How to tell git which private key to use?](https://superuser.com/questions/232373/how-to-tell-git-which-private-key-to-use)
SuperUser Answer: [Environment variable GIT_SSH_COMMAND](https://superuser.com/a/912281)



## automatically track local and remote branches
```
fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```
`git config --global --edit`
```
[push]
        autoSetupRemote = true
```
or just
`git config --global --add push.autoSetupRemote true`

