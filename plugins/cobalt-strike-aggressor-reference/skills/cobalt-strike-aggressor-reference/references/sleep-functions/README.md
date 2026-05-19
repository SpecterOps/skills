# Sleep Programming Language Documentation

This directory contains the complete Sleep programming language documentation, split into individual files for efficient LLM ingestion.

## Overview

**Sleep** is a Java-based scripting language heavily inspired by Perl, designed for embedding in Java applications. This documentation has been parsed from the official Sleep manual at https://sleep.dashnine.org/manual/ and organized into individual markdown files.

## Structure

### Documentation Files

- **INDEX.md** - Complete index of all documentation with links organized by category
- **intro.md** - Introduction and getting started guide  
- **187 function reference files** - Individual MD files for each Sleep function

### Categories

The documentation is organized into these categories:

1. **Tutorial** - 10 comprehensive tutorial chapters covering all aspects of Sleep
2. **Arrays** - 30 functions for array manipulation
3. **Date/Time** - 3 functions for date/time operations
4. **File System** - 21 functions for file and directory operations
5. **Hashes** - 6 functions for hash/map data structures
6. **Input/Output** - 31 functions for I/O operations
7. **Math** - 28 mathematical functions
8. **Strings** - 29 string manipulation functions
9. **Utility** - 39 utility and meta-programming functions

### Total: 197 documentation files (10 tutorials + 187 function references)

## Quick Start

1. Start with **INDEX.md** for a complete overview and navigation
2. Read **intro.md** for an introduction to Sleep
3. Browse individual function files by name (e.g., `println.md`, `foreach.md`, `regex.md`)

## File Naming

- Tutorial files use descriptive names: `intro.md`, `functions.md`, `regex.md`, etc.
- Function files are named after the function: `functionname.md`
- Predicate functions (starting with `-`) are prefixed with `pr_`: `pr_eof.md`, `pr_exists.md`

## Usage for LLM/AI

This split documentation format is optimized for:

- **Efficient context loading** - Load only the specific function/topic needed
- **Reduced token usage** - Avoid loading the entire manual at once
- **Better search/retrieval** - Each topic is self-contained
- **Skill integration** - Easy to reference specific functions from Sleep skills

## Example Queries

When working with Sleep:

- "What does the `&println` function do?" → Reference `println.md`
- "How do I work with arrays?" → Reference `datastruct.md` and array functions
- "How do regex patterns work?" → Reference `regex.md`
- "How do I create a closure?" → Reference `functions.md` and `lambda.md`

## Source

All content sourced from the official Sleep manual:
- **Website:** http://sleep.dashnine.org/
- **Manual:** https://sleep.dashnine.org/manual/
- **Version:** Sleep 2.1
- **Author:** Raphael Mudge
- **License:** LGPL (GNU Lesser General Public License)

## Related

- **Aggressor Script Documentation** - For Cobalt Strike scripting
- **BOF Development** - For Beacon Object File development
- Both use Sleep as their scripting language

## Maintenance

To update this documentation:

1. Run `fetch_docs.py` to fetch latest function pages
2. Manually update tutorial pages if needed
3. Regenerate INDEX.md with updated references

---

**Last Updated:** February 2026  
**Sleep Version:** 2.1  
**Documentation Status:** Complete
