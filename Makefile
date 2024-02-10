.PHONY: docs

black-check:
	black --check --diff .

black-reformat:
	black .

docs:
	make -C docs/ html

flake_exclude = --exclude=baca/__init__.py
flake_ignore = --ignore=E203,E266,E501,F811,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_exclude} ${flake_ignore} ${flake_options}

isort-check:
	isort \
	--case-sensitive \
	--check-only \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--skip=baca/__init__.py \
	--thirdparty=ply \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	baca scr

isort-reformat:
	isort \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--project=abjad \
	--project=abjadext \
	--skip=baca/__init__.py \
	--thirdparty=ply \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	baca scr

mypy:
	clear
	mypy baca

pytest:
	clear
	pytest .

pytest-x:
	clear
	pytest -x .

reformat:
	make black-reformat
	make isort-reformat

check:
	clear
	make black-check
	make flake8
	make isort-check
	mypy baca

test:
	make black-check
	make flake8
	make isort-check
	mypy baca
	make pytest
