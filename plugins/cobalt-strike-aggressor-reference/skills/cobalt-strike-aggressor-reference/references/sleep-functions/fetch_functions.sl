#!/usr/bin/env sleep

# Script to fetch all Sleep function documentation pages

# Base URL
$base_url = "https://sleep.dashnine.org/manual/";

# Arrays functions
@arrays = @("in", "identity", "add", "addAll", "cast", "clear", "concat", "copy", 
            "filter", "flatten", "map", "pop", "push", "putAll", "reduce", "remove", 
            "removeAll", "removeAt", "retainAll", "reverse", "search", "shift", "size", 
            "sort", "sorta", "sortd", "sortn", "splice", "sublist", "sum");

# Date/Time functions
@datetime = @("formatDate", "parseDate", "ticks");

# File System functions
@filesystem = @("pr_canread", "pr_canwrite", "pr_exists", "pr_isDir", "pr_isFile", 
                "pr_isHidden", "chdir", "createNewFile", "cwd", "deleteFile", "getFileName",
                "getFileParent", "getFileProper", "lastModified", "listRoots", "lof", 
                "ls", "mkdir", "rename", "setLastModified", "setReadOnly");

# Hashes functions  
@hashes = @("in", "add", "clear", "copy", "keys", "ohash", "ohasha", "putAll", 
            "remove", "setMissPolicy", "setRemovalPolicy", "size", "values");

# Input/Output functions
@io = @("pr_eof", "allocate", "available", "bread", "bwrite", "closef", "connect",
        "exec", "fork", "getConsole", "listen", "mark", "openf", "print", "printAll",
        "printEOF", "println", "readAll", "readAsObject", "readb", "readc", "readln",
        "readObject", "reset", "setEncoding", "sizeof", "skip", "wait", "writeAsObject",
        "writeb", "writeObject");

# Math functions
@math = @("spaceship", "abs", "acos", "asin", "atan", "atan2", "ceil", "checksum",
          "cos", "degrees", "digest", "double", "exp", "floor", "formatNumber", "int",
          "log", "long", "not", "parseNumber", "radians", "rand", "round", "sin",
          "sqrt", "srand", "tan", "uint");

# Strings functions
@strings = @("hasmatch", "ismatch", "iswm", "cmp", "asc", "byteAt", "cast", "chr",
             "charAt", "find", "indexOf", "join", "lc", "left", "lindexOf", "matched",
             "matches", "mid", "pack", "replace", "replaceAt", "right", "split",
             "strlen", "strrep", "substr", "tr", "uc", "unpack");

# Utility functions
@utility = @("is", "isa", "acquire", "casti", "checkError", "compile_closure", "copy",
             "debug", "eval", "exit", "expr", "function", "getStackTrace", "global",
             "iff", "include", "inline", "invoke", "lambda", "let", "local", "newInstance",
             "popl", "profile", "pushl", "release", "scalar", "semaphore", "setf",
             "setField", "sleep", "systemProperties", "taint", "this", "typeOf",
             "untaint", "use", "warn", "watch");

println("Arrays: " . size(@arrays) . " functions");
println("Date/Time: " . size(@datetime) . " functions");
println("Filesystem: " . size(@filesystem) . " functions");
println("Hashes: " . size(@hashes) . " functions");
println("I/O: " . size(@io) . " functions");
println("Math: " . size(@math) . " functions");
println("Strings: " . size(@strings) . " functions");
println("Utility: " . size(@utility) . " functions");

$total = size(@arrays) + size(@datetime) + size(@filesystem) + size(@hashes) + 
         size(@io) + size(@math) + size(@strings) + size(@utility);
println("Total: " . $total . " functions to fetch");
