black-check:
	black --check --diff --target-version=py38 .

black-reformat:
	black --target-version=py38 .

flake_ignore = --ignore=E203,E266,E501,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_exclude} ${flake_ignore} ${flake_options}

# TODO: eventually do not skip __metadata__.py, __persist__.py

isort-check:
	isort \
	--case-sensitive \
	--check-only \
	--line-width=88 \
	--multi-line=3 \
	--skip=__metadata__.py \
	--skip=__persist__.py \
	--thirdparty=abjad \
	--thirdparty=abjadext \
	--thirdparty=baca \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

isort-reformat:
	isort \
	--case-sensitive \
	--line-width=88 \
	--multi-line=3 \
	--skip=__metadata__.py \
	--skip=__persist__.py \
	--thirdparty=abjad \
	--thirdparty=abjadext \
	--thirdparty=baca \
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

mypy:
	mypy .

project = baca

pytest:
	rm -Rf htmlcov/
	pytest \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov=${project} \
	.

pytest-x:
	rm -Rf htmlcov/
	pytest \
	-x \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov=${project} \
	.

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
