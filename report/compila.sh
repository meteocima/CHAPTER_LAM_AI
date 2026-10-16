#!/usr/bin/env bash
# Compila report/main.tex con latexmk e biber di TinyTeX (~/.TinyTeX, installato senza link nel
# PATH per non coprire il TeX Live di sistema usato da tools/md2pdf.py).
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
grep -nE 'undefined|Warning: (Citation|Reference)' main.log || echo "nessun riferimento indefinito"
