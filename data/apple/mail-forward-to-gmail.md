last-updated: 2023-05-07 15:00
title: How to forward local email to Gmail
meta-keywords: macOS, cron, crontab, mail, Gmail, postfix

On macOS, if we want to forward local email to an external account on Gmail, e.g. for `crontab` results or other automation, we can use the default `postfix` server and just reconfigure it to deliver the mails externally.

Note: this assumes local usernames match the user part of the email.

On `/etc/postfix/main.cf` add the following lines:
```
myorigin = <enter your public domain here>
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_sasl_mechanism_filter = login
smtp_use_tls = yes
```

Generate a dedicated app password on Google Account's page at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

On `/etc/postfix/sasl_passwd` add your username and the dedicated app password:
```
[smtp.gmail.com]:587 <your email>:<password>
```

Protect the `/etc/postfix/sasl_passwd`:
```
sudo chmod 600 /etc/postfix/sasl_passwd
```

Update the `postfix` password file:
```
sudo postmap /etc/postfix/sasl_passwd
```

Restart `postfix`:
```
sudo launchctl stop org.postfix.master
sudo launchctl start org.postfix.master
```

Look at the logs to confirm the service is working properly:
```
sudo log stream --predicate  '(process == "smtpd") || (process == "smtp")' --info &
```

Send a test email:
```
echo Hello World | mail -s "Test Subject" <my email>
```

Check for queued emails:
```
sudo mailq
```

Clear the queue in case of pending emails due to tests or bad configuration:
```
sudo postfix flush
```
