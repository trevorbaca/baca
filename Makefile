.PHONY: black-check black-reformat clean docs flake8 install isort-check \
	isort-reformat mypy pytest reformat lint test

black-check:
	black --check --diff .

black-reformat:
	black .

clean:
	find . -name '*.pyc' -delete
	rm -rf __pycache__ *.egg-info .cache .tox build dist htmlcov prof

docs:
	make -C docs/ html

flake_exclude = --exclude=source/baca/__init__.py
flake_ignore = --ignore=E203,E266,E501,F811,W503
flake_options = --isolated --max-line-length=88

flake8:
	flake8 ${flake_exclude} ${flake_ignore} ${flake_options}

install:
	python -m pip install -e .

isort-check:
	isort --case-sensitive --check-only --line-width=88 --multi-line=3 \
	      --thirdparty=abjad --thirdparty=abjadext --thirdparty=baca \
	      --thirdparty=ply --thirdparty=uqbar --trailing-comma --use-parentheses .

isort-reformat:
	isort --case-sensitive --line-width=88 --multi-line=3 \
	      --thirdparty=abjad --thirdparty=abjadext --thirdparty=baca \
	      --thirdparty=ply --thirdparty=uqbar --trailing-comma --use-parentheses .

mypy:
	mypy source

pytest:
	pytest .

reformat: black-reformat isort-reformat

lint: black-check flake8 isort-check mypy

test: lint pytest
