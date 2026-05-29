#!/usr/bin/env python3
"""
Script to fetch all Sleep function documentation pages
"""

import requests
import os
import time
from pathlib import Path

BASE_URL = "https://sleep.dashnine.org/manual/"

# All function categories
FUNCTIONS = {
    "Arrays": ["in", "identity", "add", "addAll", "cast", "clear", "concat", "copy",
               "filter", "flatten", "map", "pop", "push", "putAll", "reduce", "remove",
               "removeAll", "removeAt", "retainAll", "reverse", "search", "shift", "size",
               "sort", "sorta", "sortd", "sortn", "splice", "sublist", "sum"],

    "DateTime": ["formatDate", "parseDate", "ticks"],

    "FileSystem": ["pr_canread", "pr_canwrite", "pr_exists", "pr_isDir", "pr_isFile",
                   "pr_isHidden", "chdir", "createNewFile", "cwd", "deleteFile", "getFileName",
                   "getFileParent", "getFileProper", "lastModified", "listRoots", "lof",
                   "ls", "mkdir", "rename", "setLastModified", "setReadOnly"],

    "Hashes": ["keys", "ohash", "ohasha", "setMissPolicy", "setRemovalPolicy", "values"],

    "InputOutput": ["pr_eof", "allocate", "available", "bread", "bwrite", "closef", "connect",
                    "exec", "fork", "getConsole", "listen", "mark", "openf", "print", "printAll",
                    "printEOF", "println", "readAll", "readAsObject", "readb", "readc", "readln",
                    "readObject", "reset", "setEncoding", "sizeof", "skip", "wait", "writeAsObject",
                    "writeb", "writeObject"],

    "Math": ["spaceship", "abs", "acos", "asin", "atan", "atan2", "ceil", "checksum",
             "cos", "degrees", "digest", "double", "exp", "floor", "formatNumber", "int",
             "log", "long", "not", "parseNumber", "radians", "rand", "round", "sin",
             "sqrt", "srand", "tan", "uint"],

    "Strings": ["hasmatch", "ismatch", "iswm", "cmp", "asc", "byteAt", "cast", "chr",
                "charAt", "find", "indexOf", "join", "lc", "left", "lindexOf", "matched",
                "matches", "mid", "pack", "replace", "replaceAt", "right", "split",
                "strlen", "strrep", "substr", "tr", "uc", "unpack"],

    "Utility": ["is", "isa", "acquire", "casti", "checkError", "compile_closure", "copy",
                "debug", "eval", "exit", "expr", "function", "getStackTrace", "global",
                "iff", "include", "inline", "invoke", "lambda", "let", "local", "newInstance",
                "popl", "profile", "pushl", "release", "scalar", "semaphore", "setf",
                "setField", "sleep", "systemProperties", "taint", "this", "typeOf",
                "untaint", "use", "warn", "watch"]
}

def fetch_and_save(func_name, category):
    """Fetch a function page and save it"""
    url = f"{BASE_URL}{func_name}.html"
    output_file = f"{func_name}.md"

    try:
        print(f"Fetching {func_name}...")
        response = requests.get(url)
        response.raise_for_status()

        # Save the content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {func_name}\n\n")
            f.write(f"**Category:** {category}\n\n")
            f.write(f"**Source:** {url}\n\n")
            f.write("---\n\n")
            f.write(response.text)

        print(f"  ✓ Saved {output_file}")
        return True

    except Exception as e:
        print(f"  ✗ Error fetching {func_name}: {e}")
        return False

def main():
    print("Fetching Sleep function documentation...")
    print("=" * 60)

    total = sum(len(funcs) for funcs in FUNCTIONS.values())
    print(f"Total functions to fetch: {total}\n")

    success_count = 0
    fail_count = 0

    for category, functions in FUNCTIONS.items():
        print(f"\n{category} ({len(functions)} functions):")
        print("-" * 60)

        for func in functions:
            if fetch_and_save(func, category):
                success_count += 1
            else:
                fail_count += 1
            time.sleep(0.1)  # Be polite to the server

    print("\n" + "=" * 60)
    print(f"Complete! Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    main()
