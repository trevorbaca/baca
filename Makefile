black_exclude = --exclude='boilerplate'

black-check:
	black --check --diff ${black_exclude} --target-version=py38 .

black-reformat:
	black ${black_exclude} --target-version=py38 .

flake_exclude = --exclude=baca/__init__.py,boilerplate
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
	--thirdparty=roman \
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
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	baca scr

mypy:
	# mypy baca

project = baca

pytest:
	pytest baca
	find . -name __pycache__ -type d -exec rm -r {} +
	find . -name .pytest_cache -type d -exec rm -r {} +

pytest-x:
	pytest -x baca
	find . -name __pycache__ -type d -exec rm -r {} +
	find . -name .pytest_cache -type d -exec rm -r {} +

reformat:
	make black-reformat
	make isort-reformat

check:
	make black-check
	make flake8
	make isort-check
	make mypy

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
