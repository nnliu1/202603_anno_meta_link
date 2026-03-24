# Compilation of slides

## 1. Run LuaLaTeX to generate the .bcf in the 'out' folder
lualatex --output-directory=out main.tex

## 2. Run Biber, pointing it to the 'out' folder
biber --input-directory=out --output-directory=out main

## 3. Final LuaLaTeX passes
lualatex --output-directory=out main.tex
lualatex --output-directory=out main.tex