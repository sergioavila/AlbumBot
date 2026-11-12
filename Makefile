VENV := .venv
BIN := $(VENV)/bin
GATE := $(BIN)/python scripts/adoption_gate.py --

.PHONY: setup-dev floor lint typecheck test coverage coverage-strict check-fast \
	check-task check-full security security-secrets security-secrets-strict \
	security-code security-code-strict security-deps security-deps-strict

setup-dev:
	python3 -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -r requirements-dev.txt

floor:
	$(BIN)/python scripts/floor_guard.py

lint:
	$(GATE) $(BIN)/ruff check .

typecheck:
	$(GATE) env MYPYPATH=app $(BIN)/mypy app scripts

test:
	$(GATE) env PYTHONPATH=app:. $(BIN)/pytest

coverage:
	$(GATE) $(MAKE) coverage-strict

coverage-strict:
	$(BIN)/coverage erase
	PYTHONPATH=app:. $(BIN)/pytest --cov --cov-report=xml --cov-report=term-missing
	$(BIN)/diff-cover coverage.xml --compare-branch=HEAD --fail-under=80

check-fast: floor lint typecheck

check-task: check-fast coverage

security-secrets:
	$(GATE) $(MAKE) security-secrets-strict

security-secrets-strict:
	docker run --rm -v "$(CURDIR):/repo" -w /repo \
		zricethezav/gitleaks:v8.24.0 detect --source . --no-git --redact --no-banner

security-code:
	$(GATE) $(MAKE) security-code-strict

security-code-strict:
	docker run --rm -v "$(CURDIR):/src" semgrep/semgrep:1.101.0 \
		semgrep scan --config p/default --config p/owasp-top-ten \
		--severity ERROR --no-git-ignore /src/app

security-deps:
	$(GATE) $(MAKE) security-deps-strict

security-deps-strict:
	docker run --rm -v "$(CURDIR):/src" ghcr.io/google/osv-scanner:v2.0.2 \
		scan source -r --format json /src | $(BIN)/python scripts/check_osv.py

security: security-secrets security-code security-deps

check-full: check-task security
