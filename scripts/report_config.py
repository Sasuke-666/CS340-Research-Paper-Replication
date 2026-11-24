"""One revision date for the current report and its exported documents."""
from calendar import month_name
from datetime import date
from pathlib import Path


def report_identity(root):
    """Read a dated stage or final report and reject an inconsistent header."""
    root = Path(root)
    value = (root / 'report/REVISION_DATE').read_text(encoding='utf-8').strip()
    result = date.fromisoformat(value)
    if result.isoformat() != value:
        raise ValueError('report/REVISION_DATE must use YYYY-MM-DD')
    paragraphs = (root / 'report/EXPANDED_REPORT.md').read_text(encoding='utf-8').split('\n\n')
    for label in ('Stage report', 'Final report'):
        marker = '%s revised %d %s %d.' % (
            label, result.day, month_name[result.month], result.year)
        if len(paragraphs) >= 2 and marker in paragraphs[1]:
            return result, label, marker
    raise ValueError('Report header does not match report/REVISION_DATE')


def revision_date(root):
    return report_identity(root)[0]


def revision_marker(root):
    return report_identity(root)[2]
