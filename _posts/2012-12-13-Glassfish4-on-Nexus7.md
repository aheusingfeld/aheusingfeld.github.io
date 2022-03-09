---
layout: single
title: Glassfish 4 on Nexus7
date: 2012-12-13T23:00:00+0200
categories: 
  - software development
tags: 
  - software development
  - java
  - glassfish
  - ubuntu
  - linux
  - android
  - debugging

---

As you might have read in [my previous blog post](http://aheusingfeld.github.com/2012/11/30/Ubuntu%2BJava-on-Nexus7.html) I'm currently doing Proof-Of-Concepts on what is possible with Java on a tablet like the [Google Nexus7 device](https://play.google.com/store/devices/details?id=nexus_7_16gb) meaning a Nvidia Tegra chip which itself is an ARMv7 processor.

Thankfully there is a team at [Ubuntu](http://www.ubuntu.org/) which dedicates its work to bringing a desktop linux to the tablet which supports the well-known standardized Java Runtime Environments out there.


### Installation
	
Unfortunately the installer doesn't install glassfish correctly so I tried the ZIP distribution which worked like a charm

	$ wget http://dlc.sun.com.edgesuite.net/glassfish/4.0/promoted/glassfish-4.0-web-b66.zip
	$ unzip glassfish-4.0-web-b66.zip
	$ cd glassfish3
	$ bin/asadmin start-domain
	
In order to exec the GlassFish Admin Gui from a remote system via browser you have to enable the secure access. This can be done with the following commands:

	$ bin/asadmin change-admin-password
	$ bin/asadmin enable-secure-admin
	$ bin/asadmin restart-domain

### Findings

Surprising to me, the [unix gui installer](http://dlc.sun.com.edgesuite.net/glassfish/4.0/promoted/glassfish-4.0-web-b66-unix.sh) works on the nexus 7 if the "DISPLAY" variable is correctly set to ":0". You can do this by typing:

	$ export DISPLAY=":0"

Now you can checkout the GlassFish Admin Gui via the installed Firefox at http://localhost:4848/ and you can even deploy simple web applications.

### Conclusion

The Nvidia Tegra chip inside the Nexus7 isn't the fastest, therefore I'd not recommend opening Firefox while you have an application deployed to the running GlassFish. Simply give him a little more RAM to swim in. 
As accessing the Glassfish Admin Gui from a remote system is just a matter of enabling secure admin (see above) and finding out your Nexus' IP which works with

	$ ifconfig
	

Then you can simply type http://192.168.1.101:4848/ into your remote system's browser and play around with your GlassFish.

![Screenshot of GlassFish admin console called from Firefox on my Mac and output of top command on the Nexus7](/gfx/glassfish-nexus-admconsole-screenshot.png)


At least in my case there were only about 86MB free RAM (see screenshot) but a small HTML5 game with WebSocket support could be deployed and run without a problem.

Have fun.


### To be continued...

I'll continue the Proof-Of-Concepts with findings on JavaFX in a follow-up post. In the meantime you can [follow me on Twitter](http://twitter.com/goldstift) to stay up to date.

Any comments, optimization requests and suggestions are very warm welcome!


### Links of further interest:
* [GlassFish 4.0 Promoted Builds (Developer Preview)](http://dlc.sun.com.edgesuite.net/glassfish/4.0/promoted/)
* [Known Issues Ubuntu-Nexus7](https://wiki.ubuntu.com/Nexus7/KnownIssues)
* [Bugtracker for Ubuntu-Nexus7](https://bugs.launchpad.net/ubuntu-nexus7)
