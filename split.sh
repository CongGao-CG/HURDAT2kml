#!/usr/bin/env sh

in="$1"
outdir="single_TC"
mkdir -p "$outdir"

generated=$(awk -F',' -v dir="$outdir" '
function trim(x){sub(/^[ \t]+/, "", x); sub(/[ \t]+$/, "", x); return x}
{
    if (trim($1) ~ /^[A-Z]{2}[0-9]{6}$/) {
        id   = trim($1)
        name = trim($2); gsub(/[[:space:]]+/, "", name)
        n    = trim($3)
        fname = dir "/" id "_" name "_" n ".txt"
        if (!(fname in seen)) {
            seen[fname] = 1
            generated++
        }
        if (out) close(out)
        out = fname
    }
    print > out
}
END { print generated + 0 }
' "$in") || exit 1

folder_total=$(find "$outdir" -type f | wc -l | tr -d '[:space:]')

printf 'Generated %s files.\n' "$generated"
printf '%s contains %s files after completion.\n' "$outdir" "$folder_total"
