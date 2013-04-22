---
layout: post
title: Mac OS X setup tips & tricks
label: osx-setup-tips+tricks
date: 2013-03-20
comments: false
---

With this is post I want to share with you my experience when re-setting up my MacBook and which tools and applications I use on a regular basis and thus I can recommend to you. :)

## Connect to iCloud
I've had too many bad experiences with iTunes to use it for syncing my data between different devices. That's why I chose to synchronize my calendars, contacts and notes via iCloud. Therefore connecting my iCloud account/ AppleID to my MacBook is pretty much the first thing to do. For syncing all other kinds of files I use my Dropbox account.

For local backup of my iPhone, iPad and iPod I rely on [ECamm's PhoneView](http://ecamm.com/mac/phoneview/) for more than 2 years now. It never let me down - which I cannot say about iTunes at all! Maybe you'd like to check it out.


## Install applications

### Manual Installations

* Firefox
* LibreOffice
* IntelliJ IDEA 
* iTerm2 [http://code.google.com/p/iterm2/](http://code.google.com/p/iterm2/)
* Little Snitch [http://www.obdev.at/products/littlesnitch/index-de.html](http://www.obdev.at/products/littlesnitch/index-de.html)
 * Personal Firewall which enables you to see and disallow whenever anything tries to connect to the internet
 * MUST-HAVE, do not want to go without it anymore
* Cyberduck [http://cyberduck.ch/](http://cyberduck.ch/)
 * Great visual SCP, FTP, SFTP client
* Zipeg [http://www.zipeg.com/](http://www.zipeg.com/)
 * view and extract contents of Archives like ZIP, RAR, JAR, WAR, tar.gz and others
 * in contrast to most other tools, Zipeg lets you look into an archive before uncompressing it to some folder
* Secrets.prefPane [http://code.google.com/p/blacktree-secrets/](http://code.google.com/p/blacktree-secrets/)
 * Visual interface to edit preferences which are only changeable via command-line
* TinkerTool [http://www.bresink.com/osx/TinkerTool.html](http://www.bresink.com/osx/TinkerTool.html)
* TotalFinder [http://totalfinder.binaryage.com/](http://totalfinder.binaryage.com/)
 * -> 18$ and worth every Cent!
* Transmission [http://www.transmissionbt.com/](http://www.transmissionbt.com/)
 * Torrent download utility
* yEd Graph Editor [http://www.yworks.com/en/products_yed_about.html](http://www.yworks.com/en/products_yed_about.html)
 * Best for Quick Diagramms; Java-based, available for Linux + Win
* Portecle [http://portecle.sourceforge.net/](http://portecle.sourceforge.net/)
 * Utility for convenient management of Java keystores
* Dropbox
* Burn [http://burn-osx.sourceforge.net/](http://burn-osx.sourceforge.net/)
 * free DVD authoring software
* RCDefaultApp [http://www.rubicode.com/Software/RCDefaultApp/](http://www.rubicode.com/Software/RCDefaultApp/)
 * Manage default application associations for specific file-types
* Sequel Pro [http://sequelpro.com/](http://sequelpro.com/)
 * Great MySQL Client for OS X
* Audacity [http://audacity.sourceforge.net/](http://audacity.sourceforge.net/)
 * multi format audio file editor
* iStatMenus [http://bjango.com/mac/istatmenus/](http://bjango.com/mac/istatmenus/)
 * Nice2have configurable system monitor app for the status bar
* Glims [http://www.machangout.com/](http://www.machangout.com/)
 * Safari-Extension
* Skype (if you can't avoid it)


### Recommended AppStore Applications

* Pixelmator
* TextWrangler
* SourceTree
* Pocket
* Outbank
* iPhoto
* Keynote
 * Caffeine
 * Display Menu
* Sitesucker
* XCode
* Screeny * Screen recording utility
* Skim


## Configure accounts

* Yahoo
* Google
* Flickr
* iCloud
* Jabber
* Twitter
* Facebook

## Specialties

* Quicktime Codecs
 * Flip4Mac [http://www.telestream.net/flip4mac/overview.htm](http://www.telestream.net/flip4mac/overview.htm)
  * WMA and WMV codec for Quicktime
 * XVid [http://www.xvid.org/Software.83.0.html](http://www.xvid.org/Software.83.0.html)
 * DivX
 * MPEG2 -> Apple-QuickTimeMPEG2-Codec (unsupported since OS X Lion)
* Terminal
 * use iTerm2 [http://iterm2.com/](http://iterm2.com/)
 * modify your .profile
 * Checkout the awesome dotfiles by Mathias Bynens [https://github.com/mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles)
* Install Homebrew [http://mxcl.github.com/homebrew/](http://mxcl.github.com/homebrew/)
* Relink Java preference pane
 * /Library/PreferencePanes/JavaControlPanel.prefPane
* [Apple Mastered for iTunes - Audio Mastering Tools](https://www.apple.com/itunes/mastered-for-itunes/)
 * drag-and-drop tool to create iTunes Plus audio files
* Enhance Quicklook
 * ZIP, rar, jar -> %http://macitbetter.com/BetterZip-Quick-Look-Generator/](http://macitbetter.com/BetterZip-Quick-Look-Generator/)
 * CSV -> [http://code.google.com/p/quicklook-csv/](http://code.google.com/p/quicklook-csv/)
 * Further more -> [http://www.quicklookplugins.com/](http://www.quicklookplugins.com/)
  
## Glitches of the Finder

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
 

## Setup your (TimeMachine) Backup
At least backup your home directory, expecially your ~/Library (yes, it's a hidden folder)
