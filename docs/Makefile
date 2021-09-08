# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

LIBARY 	      = volcengine_ml_platform
SOURCELIBARY  = ../$(LIBARY)
# Put it first so that "make" without argument is like "make help".pip install myst-parser
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).

update:
	rm source/$(LIBARY)*.rst  modules.rst -f
	sphinx-apidoc -fo  ./source  $(SOURCELIBARY)  $(SOURCELIBARY)/constant.py  $(SOURCELIBARY)/config $(SOURCELIBARY)/modelrepo  $(SOURCELIBARY)/tos $(SOURCELIBARY)/util $(SOURCELIBARY)/infrastructure

markdown: update
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
