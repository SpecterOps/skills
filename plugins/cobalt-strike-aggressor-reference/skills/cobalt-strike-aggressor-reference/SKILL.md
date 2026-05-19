---
name: cobalt-strike-aggressor-reference
description: Provides information on how to develop Agressor script files for Cobalt Strike
license: MIT
metadata:
  author: xpn
  version: "0.1.0"
  category: security
---

# Aggressor Development Skill

## When to Use

This skill should be used when a request is made to develop an agressor script for Cobalt Strike.

Agressor is a custom scripting language used by the Cobalt Strike C2 framework for automating tasks, executing BOF files

## When NOT to use

Never use this skill unless agressor scripting development is requested, or BOF development is being completed and an aggressor script is required to load and execute the bof.

## Aggressor Overview

Aggressor Script is the scripting language built into Cobalt Strike, version 3.0, and later. Aggressor Script allows you to modify and extend the Cobalt Strike client.

Aggressor Script is the spiritual successor to Cortana, the open source scripting engine in Armitage. Cortana was made possible by a contract through DARPA's Cyber Fast Track program. Cortana allows its users to extend Armitage and control the Metasploit Framework and its features through Armitage's team server. Cobalt Strike 3.0 is a ground-up rewrite of Cobalt Strike without Armitage as a foundation. This change afforded an opportunity to revisit Cobalt Strike's scripting and build something around Cobalt Strike's features. The result of this work is Aggressor Script.

Aggressor Script is a scripting language for red team operations and adversary simulations inspired by scriptable IRC clients and bots. Its purpose is two-fold. You may create long running bots that simulate virtual red team members, hacking side-by-side with you. You may also use it to extend and modify the Cobalt Strike client to your needs.

Aggressor Script builds on Raphael Mudge's Sleep Scripting Language.

Aggressor Script will do anything that Sleep can do.

## References

* [BOF](./references/bof.md) - An introduction to developing aggressor scripts for BOFs
* [Sleep](./references/sleep.md) - An introduction to the Sleep programming language
* [Aggressor](./references/cobaltstrike.md) - A reference to the Aggressor language