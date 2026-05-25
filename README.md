# CV Analyzer — local development

Bootstrapping a reproducible virtual environment and installing dependencies:

```bash
# create venv and install runtime + dev deps
./scripts/setup_venv.sh

# activate
source venv/bin/activate

# run tests
PYTHONPATH=. venv/bin/python -m pytest
```

Common shortcuts via `make`:

```bash
make init   # create venv and install requirements
make dev    # install dev dependencies
make test   # run the test suite
make run    # run the FastAPI app with uvicorn
```
