last-updated: 2005-07-14 12:19:39
title: Prevent .DS_Store file creation on network volumes
meta-keywords: Apple, MacOSX, macOS


The `.DS_Store` file is a hidden file that is created by the Finder on Mac OS X. It stores information about the files and folders in a directory, such as their position, size, and modification date. This file is used by the Finder to display the contents of a directory and to keep track of changes to the directory.

When you access a network volume from a Mac, the Finder will create a `.DS_Store` file on the volume. This can be a problem if you are using a network volume that is shared with other users, as the `.DS_Store` file can contain sensitive information about the files and folders on the volume.

To prevent the Finder from creating `.DS_Store` files on network volumes, you can use the following steps:

1. Open the Terminal application.
2. Type the following command:

```
defaults write com.apple.desktopservices DSDontWriteNetworkStores true
```

3. Press Enter.

This will prevent the Finder from creating `.DS_Store` files on network volumes.

If you want to re-enable the creation of `.DS_Store` files on network volumes, you can use the following steps:

1. Open the Terminal application.
2. Type the following command:

```
defaults write com.apple.desktopservices DSDontWriteNetworkStores false
```

3. Press Enter.

This will re-enable the creation of `.DS_Store` files on network volumes.

-----
### Links
* [macosxhints.com/article.php?story=2005070300463515](https://web.archive.org/web/20051101061624/http://www.macosxhints.com/article.php?story=2005070300463515)

