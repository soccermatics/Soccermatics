# Minimal makefile for Sphinx documentation
# Sphinx makes it easy to create intelligent and beautiful documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=  # defines any additional options for the Sphinx command
SPHINXBUILD   ?= sphinx-build  # specify location of the Sphinx build command
SOURCEDIR     = source
BUILDDIR      = build

# help target
# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


# % (Catch-all) target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
