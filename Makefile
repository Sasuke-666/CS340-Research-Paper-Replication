PYTHON ?= python3
EVIDENCE_DIR ?= results/local-$(shell date -u +%Y%m%dT%H%M%SZ)

.PHONY: help check pilot followup comparison summarize report checklist presentation deliverables audit summarize-comparisons audit-comparisons audit-member layout audit-layout summarize-layout audit-member-reviews audit-report audit-acceptance audit-twostage audit-validation
help:
	@printf '%s\n' 'make check: unit tests and repository checks' 'make pilot: build and run the pinned three-case pilot in Docker' 'make followup: controlled depth extension and fixed-witness replay' 'make comparison CASE=reorder_3: ten paired repetitions with the compatible serialized baseline' 'make summarize: regenerate the archived summaries' 'make audit: verify raw evidence, summaries and report tables' 'make audit-report: check report numbers, scope and references' 'make deliverables: export all six report, slide and handbook files' 'make layout CASE=account: run the capacity-only diagnostic in Docker' 'make summarize-layout: regenerate the registered diagnostic tables' 'Override EVIDENCE_DIR for a fresh experiment output directory.'
check:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_repository.py
pilot:
	bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
followup:
	PERIOD_DRIVER=run_period_followup.py bash scripts/period_container_pilot.sh "$(EVIDENCE_DIR)"
comparison: CASE ?= reorder_3
comparison:
	bash scripts/period_container_compatible.sh "$(CASE)" "$(EVIDENCE_DIR)"
summarize: summarize-comparisons
	$(PYTHON) scripts/summarize_period.py results/2026-11-07/pilot
	$(PYTHON) scripts/summarize_followup.py

audit: audit-comparisons audit-member audit-layout audit-member-reviews audit-acceptance audit-twostage audit-validation
	$(PYTHON) scripts/verify_period_evidence.py
	$(PYTHON) scripts/audit_period_results.py
	$(PYTHON) scripts/audit_report.py
	$(PYTHON) scripts/audit_report_explanations.py

audit-report:
	$(PYTHON) scripts/audit_report.py
	$(PYTHON) scripts/audit_report_explanations.py

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

audit-member-reviews:
	$(PYTHON) scripts/audit_member_reviews.py

audit-member:
	$(PYTHON) scripts/summarize_comparison.py results/member-reruns/1240001156-account-20261108T122201Z --cases account --repeats 10 --output results/member-reruns/1240001156-account-20261108T122201Z-summary --check

audit-acceptance:
	$(PYTHON) scripts/check_acceptance.py results/2026-11-22/acceptance-45015126850-attempt1 --output results/2026-11-22/summaries/acceptance-45015126850-attempt1 --check

audit-twostage:
	$(PYTHON) scripts/recount_twostage_acceptance.py

audit-validation:
	$(PYTHON) scripts/audit_1240001156_acceptance_metrics.py
	$(PYTHON) scripts/audit_1240001156_validation_evidence.py --check

layout: CASE ?= account
layout:
	bash scripts/period_container_layout.sh "$(CASE)" "$(EVIDENCE_DIR)"

summarize-layout:
	$(PYTHON) scripts/summarize_layout.py results/2026-11-14/layout-43570556202 --cases lazy01 --output results/2026-11-14/summaries/layout-43570556202-lazy01
	$(PYTHON) scripts/summarize_layout.py results/2026-11-14/layout-recovery-43575584325 --cases account --output results/2026-11-14/summaries/layout-recovery-43575584325-account

audit-layout:
	$(PYTHON) scripts/summarize_layout.py results/2026-11-14/layout-43570556202 --cases lazy01 --output results/2026-11-14/summaries/layout-43570556202-lazy01 --check
	$(PYTHON) scripts/summarize_layout.py results/2026-11-14/layout-recovery-43575584325 --cases account --output results/2026-11-14/summaries/layout-recovery-43575584325-account --check

report: audit-report
	$(PYTHON) scripts/export_stage_report.py

checklist:
	$(PYTHON) scripts/export_member_checklist.py --pdf

presentation:
	$(PYTHON) scripts/export_presentation.py

deliverables: report checklist presentation
