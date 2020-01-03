project = baca

mypy:
	mypy --ignore-missing-imports ${project}/

errors = E123,E203,E265,E266,E501,E722,F81,W503
formatPaths = ${project}/ *.py
testPaths = ${project}/
flakeOptions = --exclude=boilerplate,abjad/__init__.py,abjad/pitch/__init__.py --max-line-length=90 --isolated

black-check:
	black --target-version py36 --exclude '.*boilerplate.*' --check --diff ${formatPaths}

black-reformat:
	black --target-version py36 --exclude '.*boilerplate.*' ${formatPaths}

flake8:
	flake8 ${flakeOptions} --ignore=${errors} ${formatPaths}

isort:
	isort \
		--case-sensitive \
		--multi-line 3 \
		--project abjad \
		--project abjadext \
		--recursive \
		--skip ${project}/__init__.py \
		--skip-glob '*boilerplate*' \
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
	make isort
	make black-reformat

test:
	make black-check
	make flake8
	make mypy
	make pytest
