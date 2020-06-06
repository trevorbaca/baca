project = baca

errors = E123,E203,E231,E265,E266,E501,E722,F81,W503
formatPaths = ${project}/ *.py
testPaths = ${project}/
flakeOptions = --exclude=baca/__init__.py --max-line-length=90 --isolated

black-check:
	black --check --diff --target-version py38 ${formatPaths}

black-reformat:
	black --target-version py38 ${formatPaths}

flake8:
	flake8 ${flakeOptions} --ignore=${errors} ${formatPaths}

isort-check:
	isort \
		--case-sensitive \
		--check-only \
		--line-width=88 \
		--multi-line=3 \
		--project=abjad \
		--project=abjadext \
		--recursive \
		--skip=${project}/__init__.py \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

isort-reformat:
	isort \
		--apply \
		--case-sensitive \
		--line-width=88 \
		--multi-liner=3 \
		--project=abjad \
		--project=abjadext \
		--recursive \
		--skip=${project}/__init__.py \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

mypy:
	mypy ${project}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

pytest-x:
	rm -Rf htmlcov/
	pytest \
		-x \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

reformat:
	make black-reformat
	make isort-reformat

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
