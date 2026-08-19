# Profile Variants

Malleable C2 profile files, by default, contain one profile. It’s possible to pack variations of the current profile by specifying variant blocks for http-beacon, https- certificate, http-get, http-post and http-stager.

A variant block is specified as [block name] "variant name" { … }. Here’s a variant http-get block named "My Variant":

```
http-get "My Variant" { 
    client {
        parameter "bar" "blah";
```

A variant block creates a copy of the current profile with the specified variant blocks replacing the default blocks in the profile itself. Each unique variant name creates a new variant profile. You may populate a profile with as many variant names as you like.

Variants are selectable when configuring an HTTP or HTTPS Beacon listener. Variants allow each HTTP or HTTPS Beacon listener tied to a single Team Server to have network IOCs that differ from each other.
