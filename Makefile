project = baca

mypy:
	mypy --ignore-missing-imports ${project}/

errors = E123,E203,E265,E266,E501,E722,F81,W503
formatPaths = ${project}/ *.py
testPaths = ${project}/
flakeOptions = --exclude=baca/__init__.py --max-line-length=90 --isolated

black-check:
	black --target-version py37 --check --diff ${formatPaths}

black-reformat:
	black --target-version py37 ${formatPaths}

flake8:
	flake8 ${flakeOptions} --ignore=${errors} ${formatPaths}

isort-check:
	isort \
		--case-sensitive \
		--check-only \
		--line-width 90 \
		--multi-line 3 \
		--project abjad \
		--project abjadext \
		--recursive \
		--skip ${project}/__init__.py \
		--thirdparty ply \
		--thirdparty roman \
		--thirdparty uqbar \
		--trailing-comma \
		--use-parentheses -y \
		${formatPaths}

isort-reformat:
	isort \
		--case-sensitive \
		--line-width 90 \
		--multi-line 3 \
		--project abjad \
		--project abjadext \
		--recursive \
		--skip ${project}/__init__.py \
		--thirdparty ply \
		--thirdparty roman \
		--thirdparty uqbar \
		--trailing-comma \
		--use-parentheses -y \
		${formatPaths}

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
