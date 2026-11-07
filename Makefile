PYTHON ?= python3
EVIDENCE_DIR ?= results/local-$(shell date -u +%Y%m%dT%H%M%SZ)
CASE ?= reorder_3

.PHONY: help check pilot followup comparison summarize report audit summarize-comparisons audit-comparisons
help:
	@printf '%s\n' 'make check: unit tests and repository checks' 'make pilot: build and run the pinned three-case pilot in Docker' 'make followup: controlled depth extension and fixed-witness replay' 'make comparison CASE=reorder_3: ten paired repetitions with the compatible serialized baseline' 'make summarize: regenerate the archived summaries' 'make audit: verify raw evidence and independently recount results' 'Override EVIDENCE_DIR for a fresh experiment output directory.'
check:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_repository.py
pilot:
	bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
followup:
	PERIOD_DRIVER=run_period_followup.py bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
comparison:
	bash scripts/period_container_compatible.sh "$(CASE)" "$(EVIDENCE_DIR)"
summarize: summarize-comparisons
	$(PYTHON) scripts/summarize_period.py results/2026-11-07/pilot
	$(PYTHON) scripts/summarize_followup.py

audit: audit-comparisons
	$(PYTHON) scripts/verify_period_evidence.py
	$(PYTHON) scripts/audit_period_results.py

summarize-comparisons:
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42380929383 --output results/2026-11-07/summaries/comparison-42380929383
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42381922637 --output results/2026-11-07/summaries/comparison-42381922637
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42384122902 --cases reorder_4 --repeats 3 --output results/2026-11-07/summaries/comparison-42384122902

audit-comparisons:
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42380166815 --manifest-only
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42381557337 --manifest-only
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42380929383 --output results/2026-11-07/summaries/comparison-42380929383 --check
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42381922637 --output results/2026-11-07/summaries/comparison-42381922637 --check
	$(PYTHON) scripts/summarize_comparison.py results/2026-11-07/comparison-42384122902 --cases reorder_4 --repeats 3 --output results/2026-11-07/summaries/comparison-42384122902 --check

report:
	$(PYTHON) scripts/export_stage_report.py
