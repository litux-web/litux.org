last-updated: 2018-04-24
title: Enable debug for Apple Contacts
meta-keywords: macOS, Contacts, Addressbook, Debug, Debugging


For CardDAV logs, in `Terminal` type:
```
defaults write -g ABMigrationLogEnabled -bool YES
defaults write com.apple.AddressBook.CardDAVPlugin EnableDebug -bool YES
defaults write com.apple.AddressBook.CardDAVPlugin LogConnectionDetails -bool YES
```

Then relaunch `Contacts` and see if you can reproduce the problem.
If so, then attach the following: `~/Library/Containers/com.apple.AddressBook/Data/Library/Logs/CardDAVPlugin`

Then disable the logging by typing in `Terminal` again:
```
defaults delete -g ABMigrationLogEnabled
defaults delete com.apple.AddressBook.CardDAVPlugin EnableDebug
defaults delete com.apple.AddressBook.CardDAVPlugin LogConnectionDetails
```
