---
layout: post
title: Collaborator on Sonar IntelliJ Plugin
label: collaborator-on-sonar-intellij-plugin
date: 2013-04-25
comments: false
---

Lately I was granted the "Collaborator" status on the Sonar Plugin for [IntelliJ IDEA](http://www.jetbrains.com/idea/) at Github  ([https://github.com/gshakhn/sonar-intellij-plugin/](https://github.com/gshakhn/sonar-intellij-plugin/)) and I'd like to share with you the benefits of this project.

For those who aren't familiar with the benefits of [Sonar](http://www.sonarsource.org/)'s source code analysis, yet, you should really take a look. Sonar not only performs [CheckStyle](http://checkstyle.sourceforge.net/), [PMD](http://pmd.sourceforge.net/) and [FindBugs](http://findbugs.sourceforge.net/) analysis of your code and highlights the validations on the specific lines of code. But by leveraging the power of [JaCoCo Code coverage](http://www.eclemma.org/jacoco/) it is also able to determine the line- and [branch-coverage](http://www.eclemma.org/jacoco/trunk/doc/counters.html) of your JUnit-Tests.

The Sonar plugin for IntelliJ is a basic implementation of the [Sonar Plugin for Eclipse](http://docs.codehaus.org/display/SONAR/Using+Sonar+in+Eclipse) (which is maintained by SonarSource themselves). It aids you in connecting your project modules to a project in a specific Sonar instance and apply the analyzed violation report onto your local files. See the [Readme for details](https://github.com/gshakhn/sonar-intellij-plugin#using-the-plugin)

Over time we plan to implement almost all of the features which are known to the Eclipse plugin. This started with "[Feature Request: Add Web View context menu entry](https://github.com/gshakhn/sonar-intellij-plugin/issues/11)" and continues with our current work on "[Feature Request: Run local analysis ](https://github.com/gshakhn/sonar-intellij-plugin/issues/10)". 

We'd be glad if you checked the plugin out and provide us feedback on your findings. Any constructive feedback, suggestions for improvement and feature requests are very welcome! Please feel free to file a bug in the [Github Issue tracker](https://github.com/gshakhn/sonar-intellij-plugin/issues) or ping us [via Twitter](http://twitter.com/goldstift) if you experience any problems. 
