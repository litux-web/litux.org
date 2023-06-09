last-updated: 2020-05-31
title: MacBook Pro 2011 Defective GPU
meta-keywords: macOS, MacBookPro, GPU, 2011

Boot using `Command + s`. Press `enter` if the shell doesn't appear.

Disable discrete GPU: manually type `nvram fa4ce28d-b62f-4c99-9cc3-6815686e30f9:gpu-power-prefs=%01%00%00%00` and run it.

Manually type `nvram boot-args="-v"` and run it.

Reboot with `sync; reboot`.

Boot using `Command + r` (this time it boots fine, no grey screen).

Disable SIP: manually type `csrutil disable` and run it.

Manually type `nvram fa4ce28d-b62f-4c99-9cc3-6815686e30f9:gpu-power-prefs=%01%00%00%00` and run it

Manually type `nvram boot-args="-v"` and run it

Reboot with `sync; reboot`.

Boot using `Command + s`.

Manually type `/sbin/mount -uw /` and run it.

Manually type `mkdir -p /System/Library/Extensions-off` and run it.

Manually type `mv /System/Library/Extensions/AMDRadeonX3000.kext /System/Library/Extensions-off/` and run it.

Manually type `touch /System/Library/Extensions/` and run it.

Reboot with `sync; reboot`.

