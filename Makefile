VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: init install dev test run clean

init:
	./scripts/setup_venv.sh

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	PYTHONPATH=. $(PYTHON) -m pytest -q

run:
	PYTHONPATH=. $(PYTHON) -m uvicorn app.main:app --reload

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache
