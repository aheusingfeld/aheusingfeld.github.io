---
layout: post
title: JBoss Forge in IntelliJ IDEA
label: jboss-forge-in-intellij
date: 2012-11-03
revdate: 2012-11-03 23:00:00 +0200
tags: [java, jboss, forge, bash, intellij, tool, java ee]
---

At this year's JavaOne I attended a [talk](https://oracleus.activeevents.com/connect/sessionDetail.ww?SESSION_ID=10659) by Marius Bogoevici ([@mariusbogoevici](http://twitter.com/mariusbogoevici)) and was once again pointed at the JBoss Forge project. Last time I took a look at Forge it was still called Seam Forge which was about a year ago. It seriously matured since then.

[JBoss Forge](http://forge.jboss.org/) is a shell for rapid-application development at a command-line level. It supports developers setting up Java applications by reducing the need to write boilerplate code. In case you ever have to start a project from scratch you should really take a glance at JBoss Forge as it makes life easier!


pass::[more]


### Daily usage
As I'm using Forge on a regular basis, I often see myself switching between the IDE and the command line which seems quite inefficient. There is a neat integration for Eclipse but unfortunately there isn't any integration into IDEs like Netbeans or my favourite IntelliJ IDEA.
Nevertheless as Forge operates at command-line level it can easily be integrated into any IDE supporting input via a console window.

In IntelliJ IDEA (I'm using the [IntelliJ IDEA 12 EAP](http://confluence.jetbrains.net/display/IDEADEV/IDEA+12+EAP)) this is done via an "External Tools" configuration. Therefore open IntelliJ's "Settings" dialog and navigate to "External Tools". Then click on the "+"-Button to create a new "External Tool" configuration.

### Configuration for Mac OS X

On Mac OS X I entered the following:
- Name: forge
- group: 
- description: JBoss Forge
- Program: /bin/bash
- Parameter: --init-file /Users/USERNAME/.bash_profile -i -c $FORGE_HOME/bin/forge
- Working Directory: $ProjectFileDir$

![Screenshot of "External Tools" configuration for JBoss Forge](/gfx/idea-external-tool-jboss-forge.png)

My "~/.profile" contains the following lines:

	export FORGE_HOME=/Users/ahe/dev/tools/forge-distribution-1.1.1.Final
	export PATH=/opt/local/bin:/opt/local/sbin:$FORGE_HOME/bin:$PATH

### Other operating systems

In case you ain't working on Mac OS X, you will have to adjust the above mentioned paths accordingly. 
For Windows users I can recommend the bash packaged with [Git For Windows](https://code.google.com/p/msysgit/).

