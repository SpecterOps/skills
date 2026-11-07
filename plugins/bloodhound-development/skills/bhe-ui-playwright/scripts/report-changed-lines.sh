#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <absolute-repo-path> [base-ref]" >&2
    exit 2
fi

repo_path="$1"
base_ref="${2:-origin/main}"

git -C "$repo_path" rev-parse --verify "$base_ref" >/dev/null

{
    git -C "$repo_path" diff --numstat "$base_ref" --
    while IFS= read -r -d '' file_path; do
        line_count="$(wc -l < "$repo_path/$file_path" | tr -d ' ')"
        printf '%s\t0\t%s\n' "$line_count" "$file_path"
    done < <(git -C "$repo_path" ls-files --others --exclude-standard -z)
} | awk -F '\t' '
    function is_test(path) {
        return path ~ /(^|\/)(test|tests|__tests__)(\/|$)/ || path ~ /\.(test|spec)\./
    }
    $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {
        added += $1
        deleted += $2
        if (is_test($3)) {
            test_added += $1
            test_deleted += $2
            kind = "test"
        } else {
            production_added += $1
            production_deleted += $2
            kind = "production"
        }
        files[++file_count] = sprintf("%s\t+%s\t-%s\t%s", kind, $1, $2, $3)
    }
    END {
        printf "TOTAL\tadded=%d\tdeleted=%d\n", added, deleted
        printf "PRODUCTION\tadded=%d\tdeleted=%d\n", production_added, production_deleted
        printf "TEST\tadded=%d\tdeleted=%d\n", test_added, test_deleted
        print "FILES"
        for (row = 1; row <= file_count; row++) print files[row]
    }
'
