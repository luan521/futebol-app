cd docs ;
sphinx-apidoc --force --maxdepth 2 --private --module-first --ext-autodoc --ext-viewcode --ext-todo  -o source/module ../cafu ;
make html