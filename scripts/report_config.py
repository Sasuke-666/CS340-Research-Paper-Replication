"""One revision date for the current report and its exported documents."""
from calendar import month_name
from datetime import date
from pathlib import Path


def revision_date(root):
    """Reject an invalid date or a report header that has drifted from it."""
    root = Path(root)
    value = (root / 'report/REVISION_DATE').read_text(encoding='utf-8').strip()
    result = date.fromisoformat(value)
    if result.isoformat() != value:
        raise ValueError('report/REVISION_DATE must use YYYY-MM-DD')
    marker = 'Stage report revised %d %s %d.' % (
        result.day, month_name[result.month], result.year)
    paragraphs = (root / 'report/EXPANDED_REPORT.md').read_text(encoding='utf-8').split('\n\n')
    if len(paragraphs) < 2 or marker not in paragraphs[1]:
        raise ValueError('Report header does not match report/REVISION_DATE')
    return result
