---
layout: post
title: Ubuntu on Nexus7 with JavaFX
label: ubuntu-on-Nexus7-with-JavaFX
date: 2012-12-02
comments: false
---

	$ sudo apt-get install openjdk-7-jdk icedtea-7-plugin
	The following NEW packages will be installed:
	  ca-certificates-java icedtea-7-jre-jamvm icedtea-7-plugin icedtea-netx icedtea-netx-common java-common libatk-wrapper-java libatk-wrapper-java-jni libbonobo2-0  libbonobo2-common libgconf2-4 libgif4 libgnome2-0 libgnome2-bin libgnome2-common libgnomevfs2-0 libgnomevfs2-common libice-dev libidl-common libidl0 libnss3-1d liborbit2 libpthread-stubs0 libpthread-stubs0-dev libsm-dev libx11-dev libx11-doc libxau-dev libxcb1-dev libxdmcp-dev libxt-dev openjdk-7-jdk openjdk-7-jre openjdk-7-jre-headless openjdk-7-jre-lib ttf-dejavu-extra tzdata-java x11proto-core-dev x11proto-input-dev x11proto-kb-dev xorg-sgml-doctools xtrans-dev
	0 upgraded, 42 newly installed, 0 to remove and 0 not upgraded.


### System stabilization
Currently there are some bugs in Unity and Nux which are already fixed in the Unity-Team PPA. To get the fixes you need to add their ppa via
	
	$ sudo add-apt-repository ppa:unity-team/ppa
	$ sudo apt-get update
	$ sudo apt-get upgrade
	The following packages will be upgraded:
	  bamfdaemon gir1.2-unity-5.0 libbamf3-0 libunity-protocol-private0 libunity9 nux-tools unity-lens-photos
	7 upgraded, 0 newly installed, 0 to remove and 10 not upgraded.
	$ sudo service lightdm restart



Nice to know: Ubuntu for Nexus7 image uses hard-float ABI (aka armhf/gnueabihf) but #JavaFX embedded uses SoftFloat (aka 'armel'). See 
[https://groups.google.com/d/msg/pandaboard/bb53tEV5GKA/OaU2L3Qqz5EJ](https://groups.google.com/d/msg/pandaboard/bb53tEV5GKA/OaU2L3Qqz5EJ) for reference.

Following my last blog post I tried to start the JavaFX FXMLLoginDemo and got the following error:

	$ sudo /opt/java/jdk1.7.0_10/bin/java -Djavafx.platform=fb -cp /opt/java/jdk1.7.0_10/jre/lib/jfxrt.jar:/home/ubuntu/Downloads/javafx-samples-2.2.3/FXML-LoginDemo.jar com.javafx.main.Main
	SEVERE: com.sun.glass.ui.lens.LensApplication _initialize 2928 src/fb-input/fbCursor.c:66 fbCursorInitialize: Cannot query plane info
	SEVERE: com.sun.glass.ui.lens.LensApplication _initialize 2928 src/fb-input/fbCursor.c:130 fbCursorClose: Failed to disable cursor plane
	Exception in Application start method
	java.lang.NoClassDefFoundError: Could not initialize class com.sun.javafx.css.StyleHelper
		at com.sun.javafx.css.StyleManager.getStyleHelper(StyleManager.java:898)
		at javafx.scene.Node.impl_processCSS(Node.java:7459)
		at javafx.scene.Parent.impl_processCSS(Parent.java:1179)
		at javafx.scene.Node.processCSS(Node.java:7426)
		at javafx.scene.Scene.doCSSPass(Scene.java:446)
		at javafx.scene.Scene.access$3800(Scene.java:171)
		at javafx.scene.Scene$ScenePulseListener.pulse(Scene.java:2217)
		at com.sun.javafx.tk.Toolkit.firePulse(Toolkit.java:346)
		at com.sun.javafx.tk.quantum.QuantumToolkit.pulse(QuantumToolkit.java:502)
		at com.sun.javafx.tk.quantum.QuantumToolkit$11.run(QuantumToolkit.java:355)
		at com.sun.glass.ui.lens.LensApplication$RunnableEvent.dispatch(Unknown Source)
		at com.sun.glass.ui.lens.LensApplication._runLoop(Unknown Source)
		at com.sun.glass.ui.lens.LensApplication.access$400(Unknown Source)
		at com.sun.glass.ui.lens.LensApplication$4.run(Unknown Source)
		at java.lang.Thread.run(Thread.java:722)
	java.lang.reflect.InvocationTargetException
		at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
		at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
		at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
		at java.lang.reflect.Method.invoke(Method.java:601)
		at com.javafx.main.Main.launchApp(Main.java:642)
		at com.javafx.main.Main.main(Main.java:805)
	Caused by: java.lang.RuntimeException: Exception in Application start method
		at com.sun.javafx.application.LauncherImpl.launchApplication1(LauncherImpl.java:376)
		at com.sun.javafx.application.LauncherImpl.access$000(LauncherImpl.java:47)
		at com.sun.javafx.application.LauncherImpl$1.run(LauncherImpl.java:115)
		at java.lang.Thread.run(Thread.java:722)
	Caused by: java.lang.UnsatisfiedLinkError: /opt/java/jdk1.7.0_10/jre/lib/arm/libjavafx-font.so: libstdc++.so.6: cannot open shared object file: No such file or directory
		at java.lang.ClassLoader$NativeLibrary.load(Native Method)
		at java.lang.ClassLoader.loadLibrary1(ClassLoader.java:1939)
		at java.lang.ClassLoader.loadLibrary0(ClassLoader.java:1864)
		at java.lang.ClassLoader.loadLibrary(ClassLoader.java:1825)
		at java.lang.Runtime.load0(Runtime.java:792)
		at java.lang.System.load(System.java:1059)
		at com.sun.glass.utils.NativeLibLoader.loadLibraryFullPath(Unknown Source)
		at com.sun.glass.utils.NativeLibLoader.loadLibraryInternal(Unknown Source)
		at com.sun.glass.utils.NativeLibLoader.loadLibrary(Unknown Source)
		at com.sun.t2k.T2KFontFactory$1.run(T2KFontFactory.java:57)
		at java.security.AccessController.doPrivileged(Native Method)
		at com.sun.t2k.T2KFontFactory.<clinit>(T2KFontFactory.java:54)
		at com.sun.javafx.font.PrismFontLoader.getSystemFontSize(PrismFontLoader.java:496)
		at javafx.scene.text.Font.getDefaultSystemFontSize(Font.java:69)
		at javafx.scene.text.Font.getDefault(Font.java:85)
		at com.sun.javafx.css.StyleHelper.<clinit>(StyleHelper.java:1600)
		at com.sun.javafx.css.StyleManager.getStyleHelper(StyleManager.java:898)
		at javafx.scene.Node.impl_processCSS(Node.java:7459)
		at javafx.scene.Parent.impl_processCSS(Parent.java:1179)
		at javafx.scene.Node.processCSS(Node.java:7426)
		at javafx.scene.Scene.doCSSPass(Scene.java:446)
		at javafx.scene.Scene.preferredSize(Scene.java:1455)
		at javafx.scene.Scene.impl_preferredSize(Scene.java:1522)
		at javafx.stage.Window$10.invalidated(Window.java:723)
		at javafx.beans.property.BooleanPropertyBase.markInvalid(BooleanPropertyBase.java:106)
		at javafx.beans.property.BooleanPropertyBase.set(BooleanPropertyBase.java:140)
		at javafx.stage.Window.setShowing(Window.java:786)
		at javafx.stage.Window.show(Window.java:801)
		at javafx.stage.Stage.show(Stage.java:230)
		at demo.Main.start(Main.java:44)




As system user "ubuntu" change into directory "/usr/lib" and create the following symlinks:

	$ cd /usr/lib
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libXext.so.6 libXext.so.6
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libXext.so.6.4.0 libXext.so.6.4.0
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libstdc++.so.6 libstdc++.so.6
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libstdc++.so.6.0.17 libstdc++.so.6.0.17
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libX11.so.6.3.0 libX11.so.6
	$ sudo ln -s /usr/lib/arm-linux-gnueabihf/libX11.so.6.3.0 libX11.so.6.3.0

Afterwards you should see the following:

	$ ls -la /usr/lib/libXext*
	lrwxrwxrwx 1 root root 41 Dec  1 10:28 /usr/lib/libXext.so.6 -> /usr/lib/arm-linux-gnueabihf/libXext.so.6
	lrwxrwxrwx 1 root root 45 Dec  1 10:28 /usr/lib/libXext.so.6.4.0 -> /usr/lib/arm-linux-gnueabihf/libXext.so.6.4.0
	$ ls -la /usr/lib/libstdc*
	lrwxrwxrwx 1 root root 43 Dec  1 21:12 /usr/lib/libstdc++.so.6 -> /usr/lib/arm-linux-gnueabihf/libstdc++.so.6
	lrwxrwxrwx 1 root root 48 Dec  1 21:13 /usr/lib/libstdc++.so.6.0.17 -> /usr/lib/arm-linux-gnueabihf/libstdc++.so.6.0.17


Unfortunately rendering directly to the framebuffer didn't work, so I tried to render via OpenGL next. 

	$ sudo /opt/java/jdk1.7.0_10/bin/java -Djavafx.platform=eglfb -cp /opt/java/jdk1.7.0_10/jre/lib/jfxrt.jar:/home/ubuntu/Downloads/javafx-samples-2.2.3/FXML-LoginDemo.jar com.javafx.main.Main

	Graphics Device initialization failed for :  es2
	Error initializing QuantumRenderer: no suitable pipeline found
	java.lang.RuntimeException: java.lang.RuntimeException: Error initializing QuantumRenderer: no suitable pipeline found
		at com.sun.javafx.tk.quantum.QuantumRenderer.getInstance(QuantumRenderer.java:271)
		at com.sun.javafx.tk.quantum.QuantumToolkit.init(QuantumToolkit.java:261)
		at com.sun.javafx.tk.Toolkit.getToolkit(Toolkit.java:190)
		at com.sun.javafx.application.PlatformImpl.startup(PlatformImpl.java:120)
		at com.sun.javafx.application.LauncherImpl.launchApplication1(LauncherImpl.java:163)
		at com.sun.javafx.application.LauncherImpl.access$000(LauncherImpl.java:47)
		at com.sun.javafx.application.LauncherImpl$1.run(LauncherImpl.java:115)
		at java.lang.Thread.run(Thread.java:722)
	Caused by: java.lang.RuntimeException: Error initializing QuantumRenderer: no suitable pipeline found
		at com.sun.javafx.tk.quantum.QuantumRenderer$PipelineRunnable.init(QuantumRenderer.java:76)
		at com.sun.javafx.tk.quantum.QuantumRenderer$PipelineRunnable.run(QuantumRenderer.java:97)
		... 1 more

Therefore the following additional packages seem to be needed:

	$ sudo apt-get install libjogl2-java libjogl2-jni
	
These are then installed to `/usr/lib/jni` and have to be specified via the parameter `-Djava.library.path`

	sudo strace -o strace-javafx.txt -f /opt/java/jdk1.7.0_10/bin/java -Djavafx.platform=eglfb -Djava.library.path=/usr/lib/jni -Dcom.sun.javafx.isEmbedded=false -cp /opt/java/jdk1.7.0_10/jre/lib/jfxrt.jar:/home/ubuntu/Downloads/javafx-samples-2.2.3/FXML-LoginDemo.jar com.javafx.main.Main	

this created the following file: https://gist.github.com/4208893

Any comments, optimization requests and suggestions are very warm welcome!







### Links of further interest:
* [Please explain softfloat vs softfp vs hardfp](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=7796)
* Linux Packages Search http://pkgs.org/ubuntu-12.10/ubuntu-universe-i386/libsfstdc++6-armhf-cross_4.7.2-1ubuntu1cross1.70_all.deb.html
* http://stackoverflow.com/questions/12764023/visualvm-can-not-start
* https://forums.oracle.com/forums/thread.jspa?threadID=2451224
* [Known Issues](https://wiki.ubuntu.com/Nexus7/KnownIssues)
* [Bugtracker for ubuntu-Nexus7](https://bugs.launchpad.net/ubuntu-nexus7)
* [Ubuntu uses Ginn for Multitouch](https://wiki.ubuntu.com/Multitouch/Ginn)







In my previous post I described how to setup [Ubuntu Linux](http://www.ubuntu.org/) and [Oracle Java](http://java.oracle.net/) on the [Nexus7 device](https://play.google.com/store/devices/details?id=nexus_7_16gb) as the single operating system. In this post 'm going to setup a multiboot solution so you are able to use Android and Ubuntu. 
My environment is a Macbook Pro (MBP) running on OS X 10.8 (Mountain Lion). The Nexus 7 (in my case the 16gb version) is attached to the MBP via its USB cable.





#### Install OpenSSH as recovery console
To be able to interact with the device when the X11-Server crashes (or you chose an unusable Desktop environment - like me I wanted to try "Openbox") your first step should be the installation of the OpenSSH server.

	$ sudo apt-get install openssh-server

Via "ipconfig" you get the ip of your device and can login from a remote machine (username: ubuntu; password: ubuntu).
	
	
#### Decrease memory consumption
On of the [Known Issues](https://wiki.ubuntu.com/Nexus7/KnownIssues) is a quiet large memory consumption of the unity desktop. To compress memory and decrease memory consumption you can install the following

	$ sudo apt-get install zram-config 

Another way would be to install a more lightweight desktop environment like LXDE
	$ sudo apt-get install lxde

### Installing Oracle Java
For my installation I used Oracle JDK 7 (1.7.10 Developer Preview available here: [http://jdk7.java.net/fxarmpreview/](http://jdk7.java.net/fxarmpreview/))

	$ sudo mkdir -p /opt/java
	$ wget http://www.java.net/download/JavaFXarm/jdk-7u10-ea-fx-8_0_0-embedded-linux-arm-sfp.tar.gz
	$ sudo tar xzvf jdk-7u10-ea-fx-8_0_0-embedded-linux-arm-sfp.tar.gz -C /opt/java

Finally we need to add the JAVA_HOME variable to the .bashrc file so it is set for every shell session

	$ echo export JAVA_HOME=/opt/java/jdk1.7.0_10 >> ~/.bashrc
	$ echo export PATH=\$JAVA_HOME/bin:\$PATH >> ~/.bashrc

If you now try to start java you should get an error like the following

	/opt/java/jdk1.7.0_10/bin/java: No such file or directory
	
or if you're already one step further this one

	/opt/java/jdk1.7.0_10/bin/java: error while loading shared libraries: libgcc_s.so.1: cannot open shared object file: No such file or directory


I'm totally new to the embedded business so please spare me, but as far as I found out, the above mentioned java version goes well with ARM softfp shared libraries for armhf. So we need to install a special version of libc6 for java on our Nvidia Tegra ([ARM Cortex-A9](http://www.arm.com/products/processors/cortex-a/cortex-a9.php)) and also the according "gcc1" version:
	$ sudo apt-get install libc6-armel libsfgcc1

After this you should be able to run the "java" command successfully:	

	$ /opt/java/jdk1.7.0_10/bin/java -version
	  java version "1.7.0_10-ea"
	  Java(TM) SE Runtime Environment (build 1.7.0_10-ea-b08)
	  Java HotSpot(TM) Client VM (build 23.6-b03, mixed mode)

### To be continued...

As this post is already rather long, I'll continue the findings on JavaFX in a follow-up post. In the meantime you can [follow me on Twitter](http://twitter.com/goldstift) to stay up to date.

