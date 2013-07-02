---
layout: post
title: Postfix and /etc/hosts
label: postfix_and_etc_hosts
date: 2013-06-27
comments: false
---
The following post is actually a note2self as I stumbled over this problem and wanted to create a reminder for myself and others with similar issues.

## Scenario
"**master**" is the host machine for multiple virtual machines (in my case they are run and managed via "libvirt").
One of these virtual machines is "**mail-host**" which holds a postfix mailserver. All of the machines are using an externally managed DNS server.
The virtual machines are only available to the outside world via NAT. They don't have public IP addresses and therefore aren't known to the external DNS server.

The last point is actually the reason for this post:

**How do I configure postfix to forward mails for "example.org" to another server if DNS states that localhost is "example.org"?**

## The Requirement 

We're running things like "rkhunter", "fail2ban" or "unattended-upgrades" on the 
master which all would like to inform root via mail about certain things going on. 

BTW: If /usr/bin/mail isn't installed, yet, you can do so via

	$ sudo apt-get install bsd-mailx

This will also install a slim variant of postfix on our "master" machine.

Next we create a mail forwarding for all mails which are send to root@master by simply creating a ".forward" file in root's home folder

	$ echo admin@example.org > /root/.forward


If we now test our setup via

	$ echo Ouch, that doesn't work! | mail -s "test mail" root


we will see something like the following in your /var/log/mail.log

	Jun 27 19:34:35 master postfix/pickup[25736]: 8D6061341019: uid=0 from=<root>
	Jun 27 19:34:35 master postfix/cleanup[25742]: 8D6061341019: message-id=<20130627173435.8D6061341019@master.localdomain>
	Jun 27 19:34:35 master postfix/qmgr[25737]: 8D6061341019: from=<root@master>, size=504, nrcpt=1 (queue active)
	Jun 27 19:34:35 master postfix/error[25744]: 8D6061341019: to=<admin@example.org>, orig_to=<root>, relay=none, delay=0.26, delays=0.2/0/0/0.06, dsn=5.0.0, status=bounced (example.org)


The DNS server tells "master" that he himself is "example.org" and therefore we have an endless loop for mail delivery. Postfix states this via the "status=bounced" error.


## Configure local domain resolution

In the next step we need to tell the postfix on "master" that it should not query DNS for domain resolution of "example.org" 
but instead rely on /etc/hosts so we can resolve the IP of our virtual machine correctly.

	$ vi /etc/hosts
	---
	# IPv4
	127.0.0.1 localhost
	192.168.123.10	example.org mail.example.org
	...

and additionally 

	$ vi /etc/postfix/main.cf
	---
	....
	relayhost = mail-host
	inet_protocols = all
	#lmtp_host_lookup = native
	smtp_host_lookup=native


Now you can test your configuration by

	$ service postfix restart
	$ echo Hi there, how are you? | mail -s "test mail" root