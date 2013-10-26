check:
	pep8 git-sweep setup.py
	pylint \
		--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' \
		--errors-only \
		--disable=E1101 \
		--rcfile=/dev/null \
		git-sweep setup.py
	check-manifest
	python setup.py --long-description | rst2html.py --strict > /dev/null
	scspell setup.py README.rst

readme:
	@restview --long-description --strict
