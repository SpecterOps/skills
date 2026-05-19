# Introduction

**Category:** Tutorial

**Source:** https://sleep.dashnine.org/manual/intro.html

---

## I. What is Sleep?

The java world currently has Jacl for TCL, Jython for Python, and JRuby for Ruby. One offering is missing from this bunch: what Java scripting language exists for the Perl hackers of the world?

Sleep is a Java-based scripting language heavily inspired by Perl. Sleep started out as a weekend long hack fest in April 2002. When nothing like Perl was available to build a scriptable Internet Relay Chat client, I set out to build the scripting language I wanted.

Go ahead and download jIRCii to see what Sleep can do. http://jircii.dashnine.org/

Sleep has evolved beyond its beginnings as a scripting engine for a chat program. Today Sleep primitives include strings, doubles, integers, and containers for holding objects and functions. Arrays and hashes can combine these primitives into complex data structures. Closures that respond to "messages" act as a flexible means of abstraction. Also The entire Java API is accessible as if the Java Objects were functions that respond to "messages".

### Sleep Website

It is about 11:30pm on a Friday night and I would love to know where I can get some sleep. All puns aside, the latest version of Sleep is always available at the Sleep homepage:

http://sleep.dashnine.org/

You will find documentation, script examples, articles, and extensions at the Sleep homepage.

### How to receive support

Most sleep discussion takes place on a google group. Through this group you can see what is on the horizon with Sleep and comment on open ideas. This is also a great place to report bugs and receive support.

http://groups.google.com/group/sleep-developers/

If you prefer to chat with a living person, you may find me and some Sleep hackers on internet relay chat (IRC). We are in the **#jIRCii** channel on the EFNet IRC network. A list of EFNet servers is available at http://www.efnet.org/

### Sleep Snippets Blog

O'Reilly and Associates has a successful series of books on technology hacks. These books consist of about 100 stand-alone tips and code snippets around a core subject. In this spirit Sleep has the Sleep Snippets Weblog. Each new snipppet (with explanation) shows off cool Sleep capabilities.

http://jroller.com/page/sleepsnip

## II. Manual Conventions

This manual consists of two sections. The first section is a tutorial on the Sleep language. This section is small on purpose. Read it to get a good grounding in the terminology, idioms, and features of the Sleep language. The second section is a man-page style reference on the standard Sleep library. This reference includes descriptions of each parameter, example code, and related topics.

The following conventions exist throughout this manual.

A monospaced font signals source code.

```sleep
println("hello world");
```

Italicized text refers to variable names.

$variable, @array, %hash.

This guide displays function names in a monospaced font.

&foo

Examples will occasionally show input or user originated commands. A strong typeface marks this.

```
java -jar sleep.jar
```

Program output is below:

```
I am some output
```

This manual also highlights frequently asked questions.

### What are these boxes?

This is a frequently asked questions box. These point out questions folks have asked in the past.

## III. Acknowledgements

I'll keep this list short and sweet. I just want to quickly acknowledge some of the folks whose input has shaped Sleep. I'm still doing this project for the fun of it but its good to know these guys are out there. I'd like to thank Andreas Ravnestad for his work on Slumber. Andreas and Serge Baranov both deserve thanks for their contributions to jIRCii in the past. The jIRCii community put up with a very rough scripting language a few years ago. To that end I owe a thanks to Dan "phos" Fare, mexis, T.J "ceelow" Smith, tijiez, neuken, [rza], blue-elf, drakx, and all the others who put their creativity and enthusiasm into writing Sleep scripts for jIRCii. Thanks for finding the issues so others don't have to. I'd like to thank Kurt von Finck (mneptok) for his support and advocacy. Marty Sheppard deserves mad greets. He is one of the drivers throwing Sleep at real projects. His work and input has had quite an influence on Sleep. I also want to say thanks to skape, shane, ratdog, brian, and the rest of the hick.org crew. Hick hosted the Sleep and jIRCii sites for the first several years of their existence. Thanks to Brandon Mumby for providing me a place to run my experimental Sleep webserver. This "experimental" server is currently hosting the jIRCii and Sleep websites. Also I'll thank those of you who come out of nowhere emailing me oddball questions about Sleep in weird contexts. Thanks for keeping me amused.
