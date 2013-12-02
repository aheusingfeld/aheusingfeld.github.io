---
layout: post
title: Mac OS X setup tips & tricks
label: osx-setup-tips+tricks
date: 2013-03-20
revdate: 2013-03-20 23:00:00 +0200
tags: [os x, apple, setup, apps, tips]
---

With this is post I want to share with you my experience when re-setting up my MacBook and which tools and applications I use on a regular basis and thus I can recommend to you. :)


### Applications

pass::[more]


#### System

* [Little Snitch](http://www.obdev.at/products/littlesnitch/index-de.html)
 * Personal Firewall which enables you to see and disallow whenever anything tries to connect to the internet
 * MUST-HAVE, do not want to go without it anymore
* [iTerm2](http://code.google.com/p/iterm2/)
* **Homebrew** from [http://mxcl.github.com/homebrew/](http://mxcl.github.com/homebrew/)
* **[CodeWeavers' CrossOver](http://www.codeweavers.com/products/crossover-mac/)** to run Windows Applications - worth every cent!!!
* iStatMenus [http://bjango.com/mac/istatmenus/](http://bjango.com/mac/istatmenus/)
 * Nice2have configurable system monitor app for the status bar
* [AppCleaner](http://www.freemacsoft.net/appcleaner/) to completely remove apps with all related files e.g. settings, cache and "`~/Library/Application Support`"
* [Apple Mastered for iTunes - Audio Mastering Tools](https://www.apple.com/itunes/mastered-for-itunes/)
 * drag-and-drop tool to create iTunes Plus audio files

#### Preference Panes/ Settings
* Secrets.prefPane [http://code.google.com/p/blacktree-secrets/](http://code.google.com/p/blacktree-secrets/)
 * Visual interface to display and edit all preferences which are only changeable via command-line
* TinkerTool [http://www.bresink.com/osx/TinkerTool.html](http://www.bresink.com/osx/TinkerTool.html)
* RCDefaultApp [http://www.rubicode.com/Software/RCDefaultApp/](http://www.rubicode.com/Software/RCDefaultApp/)
 * Manage default application associations for specific file-types
* Relink Java preference pane
 * /Library/PreferencePanes/JavaControlPanel.prefPane
* Enhance Quicklook
 * ZIP, rar, jar -> %http://macitbetter.com/BetterZip-Quick-Look-Generator/](http://macitbetter.com/BetterZip-Quick-Look-Generator/)
 * CSV -> [http://code.google.com/p/quicklook-csv/](http://code.google.com/p/quicklook-csv/)
 * Further more -> [http://www.quicklookplugins.com/](http://www.quicklookplugins.com/)
* Quicktime Codecs
 * Flip4Mac [http://www.telestream.net/flip4mac/overview.htm](http://www.telestream.net/flip4mac/overview.htm)
 * WMA and WMV codec for Quicktime
 * XVid [http://www.xvid.org/Software.83.0.html](http://www.xvid.org/Software.83.0.html)
 * DivX
 * MPEG2 -> Apple-QuickTimeMPEG2-Codec (unsupported since OS X Lion)
 
#### General
* [Firefox](http://www.getfirefox.com)
* [MacPass](http://mstarke.github.io/MacPass/) OpenSource OS X implementation of the **KeePass* password manager
* [LibreOffice](http://libreoffice.org/)
* Burn [http://burn-osx.sourceforge.net/](http://burn-osx.sourceforge.net/)
 * free DVD authoring software
* [Cyberduck](http://cyberduck.ch/) - Great visual SCP, FTP, SFTP client
* [Zipeg](http://www.zipeg.com/)
 * view and extract contents of Archives like ZIP, RAR, JAR, WAR, tar.gz and others
 * in contrast to most other tools, Zipeg lets you look into an archive before uncompressing it to some folder
* -TotalFinder [http://totalfinder.binaryage.com/](http://totalfinder.binaryage.com/) - 18$ and worth every Cent!-
* Transmission [http://www.transmissionbt.com/](http://www.transmissionbt.com/) - Torrent client
* [Adium](https://adium.im/) messaging client for XMPP, Jabber, ICQ, AIM, MSN, Yahoo, and more
* [yEd Graph Editor](http://www.yworks.com/en/products_yed_about.html) - Best for quick diagramms; Java-based, also available for Linux + Win
* [Audacity](http://audacity.sourceforge.net/) - multi format audio file editor
* [Glims Safari-Extension](http://www.machangout.com/)
* Pixelmator - the best graphics editor around (App Store)
* [Sublime Text](http://www.sublimetext.com/3) (and the companying 'subl' command line util) - great text editor
* [Pocket](http://getpocket.com/) (App Store) - formerly known as "ReadItLater"
* [Outbank](http://www.stoeger-it.de/) (App Store) - online banking
* Keynote - for presentations (App Store)
 * Caffeine (App Store) - to block the screen dimming down
 * Display Menu (App Store) - to easily change to the screen resolution a beamer supports
* Skim (App Store) - PDF viewer
* Skitch (App Store) - Screenshot tool with support for annotations
* [ECamm's PhoneView](http://ecamm.com/mac/phoneview/) for local backup of my iDevices
* [Android File Transfer](http://www.android.com/filetransfer/) 

### Development
* [IntelliJ IDEA (Early Access Preview)](http://confluence.jetbrains.net/display/IDEADEV/EAP)
* XCode (App Store)
* [Portecle](http://portecle.sourceforge.net/) - Utility for convenient management of Java keystores
* Database Clients
  * MongoDB 2.4 -> [RoboMongo](http://www.robomongo.org/)
  * MySQL -> [Sequel Pro](http://sequelpro.com/)
  * SQLite -> [SQLite Database Browser](http://sqlitebrowser.sourceforge.net/)
  * Oracle DB -> [Oracle SQL Developer](http://www.oracle.com/technetwork/developer-tools/sql-developer/overview/index.html)
* SourceTree - Version Control client for Git and Mercurial
* Screeny - Screen recording utility (App Store)
* [Vagrant](http://www.vagrantup.com/)
* [rbenv](http://rbenv.org/) for managing your ruby versions

**Don't forget to pimp your ~/.profile**
```shell
export MAVEN_HOME=$HOME/dev/tools/apache-maven-3.1.0
export MAVEN_OPTS="-Xmx1024m -XX:MaxPermSize=512m"
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"
export PATH=$HOME/.rbenv/bin:/usr/local/bin:$PATH

  if [ -f /opt/local/etc/bash_completion ]; then
      . /opt/local/etc/bash_completion
  fi

grepcode() {
        find ~/dev/repos -type d -name .git | parallel "cd {.} && git grep --color -I --full-name -i '$@' | sed 's@^\(.*\):@{.}\1: @'";
}

source ~/.aliases
source ~/.travis/travis.sh
source ~/.bash_dont_think.sh

eval "$(rbenv init -)"
```

Also checkout the awesome dotfiles (including useful aliases) by Mathias Bynens [https://github.com/mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles)


### Glitches of the Finder

* Desktop folder behaves**different*
 * files in the Desktop folder will always be previewed in their icon
 * movie files on the desktop do always consume CPU time for preview
* hides system files
* overwrites folders of the same name
 * use TotalFinder from [http://totalfinder.binaryage.com/](http://totalfinder.binaryage.com/)
* Spotlight vs. Alfred
 * Pro Spotlight
  * built in
 * Pro Alfred [http://alfredapp.com/](http://alfredapp.com/)
  * builds on Spotlight index but add's specific configuration
  * on the fly calculations
  * directed searches
  * easily customizable
  * it's free
 

### Setup your (TimeMachine) Backup
At least backup your home directory, especially your `~/Library` (yes, it's a hidden folder)

If you liked this post, you might also be interested in "[Enhancements for Mac OS X Finder](http://aheusingfeld.github.io/2012/11/26/Productivity-for-Finder.html)" I posted some time ago.
