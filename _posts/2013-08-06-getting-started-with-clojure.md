---
layout: single
title: "Getting started with Clojure"
date: 2013-08-06T23:15:27+0200
categories: 
  - software development
tags: 
  - clojure
  - software development
  - intellij
  - tipps

---

### Why Clojure?

As I apparently love to use many braces in my blog posts, Clojure is just a natural match! ;)
Just kidding. I wanted to dig into Clojure for about a year now, but couldn't find the time. Clojure to me seems like the most interesting member of the functional programming language family.


### Getting started
The official clojure.org website has a Getting Started page [http://clojure.org/getting_started](http://clojure.org/getting_started) which sends you to the community-driven Clojure Documentation [http://dev.clojure.org/display/doc](http://dev.clojure.org/display/doc) ...

... but there is also this one: [http://clojure-doc.org/](http://clojure-doc.org/)

... and even this one: [http://clojuredocs.org/](http://clojuredocs.org/)

... and additionally there's the official documentation at [http://clojure.org/documentation](http://clojure.org/documentation) ;-)




**Though the official documentation is definitely the most complete, I personally liked this introduction much better. So I recommend you start here:**  [http://clojure-doc.org/articles/tutorials/introduction.html](http://clojure-doc.org/articles/tutorials/introduction.html)

Another resource that has been really helpful, was the Clojure CheatSheet at [http://clojure.org/cheatsheet](http://clojure.org/cheatsheet)

After I read the Introduction I wanted to make sure that I - to some degree - internalized the basics, so I started to dig into the [Clojure Koans](http://clojurekoans.com/). "Koan" is derived from [Zen training](https://en.wikipedia.org/wiki/Koans). It is a question which shall provoke a "great doubt" in you to test your progress. Good luck! ;)

### Setup

#### Downloads

* Download the Leiningen script from  [https://raw.github.com/technomancy/leiningen/stable/bin/lein](https://raw.github.com/technomancy/leiningen/stable/bin/lein)
* place it on your `$PATH` e.g. in `/usr/local/bin` and make it executable
* run `lein version` on the command line

This will download and install the necessary binary and place them in `~/.lein/self-installs/`


#### IntelliJ IDEA

My favorite IDE, [IntelliJ IDEA](http://confluence.jetbrains.net/display/IDEADEV/EAP), supports Clojure development with the following plugins

* [La Clojure Plugin @Github](https://github.com/JetBrains/la-clojure#la-clojure)
* [Leiningen Plugin @Github](https://github.com/derkork/intellij-leiningen-plugin#the-intellij-leiningen-plugin)

Now you have context assistant, inspections and navigation support and can open a Clojure REPL in IDEA. If your project has a `project.clj` file, leiningen will read the project configuration from this file, load your dependencies as libraries into IntelliJ and provide you with a list of available build goals.

If you want to run your Clojure code in IDEA, you can simply go like this:

* open a REPL a.k.a. "Clojure Console"
* you should now see a `user=>` prompt
* next you place the cursor at this prompt and type


		user=> (load-file "src/myfolder/myclojurecode.clj")
		user=> (ns myfolder.myclojurecode)
	

**(NOTE: you'll have to adjust this according to the [namespace](http://clojure-doc.org/articles/tutorials/introduction.html#namespaces) given in your `myclojurecode.clj` file)**

Now you should see a command prompt like `myfolder.myclojurecode=>` which will let you execute any function defined in your `myclojurecode.clj` file just like this


	(my-sample-function "a parameter string") 


### Get something done

To test my new skills on a real project, I cloned the [innoQ statuses](https://github.com/innoq/statuses) app @Github - a very, very basic open-source Twitter-clone created to play with Clojure - and started working [on a concrete issue](https://github.com/innoq/statuses/issues/10). You can see the result at [https://github.com/innoq/statuses/pull/54](https://github.com/innoq/statuses/pull/54).


### Things I learned

* Clojure REPL (Read Eval Print Loop) is the command prompt to test your Clojure programs
* Clojure is a functional programming language. Yes, breaking news, but the point is, if the term "objects" is used in the context of Clojure, it doesn't refer to objects as in an object oriented mindset! The only occasion where OO objects could be meant, is when you're talking of Java objects which can easily be used inside your Clojure programs.
* Clojure is not whitespace sensitive. Commas count as whitespace and can thus be omitted. This might make your code more readable - or totally confuse newbies!
* if expressions are hard to read, thread them via "->" (see [http://clojuredocs.org/clojure_core/clojure.core/-%3E](http://clojuredocs.org/clojure_core/clojure.core/-%3E))


Hopefully I will have time to complete the Koans and add to this list soon ... :)


### Further Links

* German Podcast introducing Clojure I can highly recommend [http://www.innoq.com/de/podcast/004-clojure](http://www.innoq.com/de/podcast/004-clojure)
* Leiningen - Clojure project automation [http://leiningen.org/](http://leiningen.org/)

