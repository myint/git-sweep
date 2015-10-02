check:
	pep8 git-sweep setup.py
	pylint \
		--rcfile=/dev/null \
		--reports=no \
		--disable=invalid-name \
		--disable=no-member \
		git-sweep setup.py
	check-manifest
	python setup.py --long-description | rstcheck -
	scspell setup.py README.rst

readme:
	@restview --long-description --strict
