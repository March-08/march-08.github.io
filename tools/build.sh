#!/bin/bash
# build.sh <fetchfile> <notion-id>  — looks up slug/title/date in articles.tsv and renders the page.
set -e
FETCH="$1"; ID="$2"
DIR="$(cd "$(dirname "$0")" && pwd)"
SITE="$DIR/../site"
line="$(grep "^$ID	" "$DIR/articles.tsv")"
slug="$(printf '%s' "$line" | cut -f2)"
title="$(printf '%s' "$line" | cut -f3)"
date="$(printf '%s' "$line" | cut -f4)"
python3 "$DIR/notion2tufte.py" "$FETCH" "$SITE" "$slug" "$title" "$date"
