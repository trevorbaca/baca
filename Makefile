black-check:
	black --check --diff --target-version=py38 .

black-reformat:
	black --target-version=py38 .

flake_exclude = --exclude=baca/__init__.py
flake_ignore = --ignore=E203,E266,E501,W503
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

project = baca

pytest:
	pytest baca
	find . \( -path '*/__pycache__/*' -o -name __pycache__ \) -delete
	find . \( -path '*/.pytest_cache/*' -o -name __pycache__ \) -delete

pytest-x:
	pytest -x baca
	find . \( -path '*/__pycache__/*' -o -name __pycache__ \) -delete
	find . \( -path '*/.pytest_cache/*' -o -name __pycache__ \) -delete

reformat:
	make black-reformat
	make isort-reformat

check:
	make black-check
	make flake8
	make isort-check

test:
	make black-check
	make flake8
	make isort-check
	make pytest
