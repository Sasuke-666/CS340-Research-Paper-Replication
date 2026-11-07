PYTHON ?= python3
EVIDENCE_DIR ?= results/local-$(shell date -u +%Y%m%dT%H%M%SZ)

.PHONY: help check pilot followup summarize report audit
help:
	@printf '%s\n' 'make check: unit tests and repository checks' 'make pilot: build and run the pinned three-case pilot in Docker' 'make followup: controlled depth extension and fixed-witness replay' 'make summarize: verify and summarize the archived pilot' 'Override EVIDENCE_DIR for a fresh experiment output directory.'
check:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_repository.py
pilot:
	bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
followup:
	PERIOD_DRIVER=run_period_followup.py bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
summarize:
	$(PYTHON) scripts/summarize_period.py results/2026-11-07/pilot
	$(PYTHON) scripts/summarize_followup.py

audit:
	$(PYTHON) scripts/verify_period_evidence.py
	$(PYTHON) scripts/audit_period_results.py

report:
	$(PYTHON) scripts/export_stage_report.py
