"""用独立的 LibreOffice 配置转换单份 Office 文档，成功后才替换目标 PDF。"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def convert_pdf(source, target):
    source, target = Path(source).resolve(), Path(target).resolve()
    binary = shutil.which('soffice') or shutil.which('libreoffice')
    if not binary:
        raise RuntimeError('Install LibreOffice and add soffice to PATH to export PDF.')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temp:
        work = Path(temp)
        result = subprocess.run(
            [binary, '-env:UserInstallation=' + (work / 'profile').as_uri(),
             '--headless', '--convert-to', 'pdf', '--outdir', str(work), str(source)],
            capture_output=True, text=True, timeout=150)
        pdf = work / source.with_suffix('.pdf').name
        if result.returncode or not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
            raise RuntimeError('LibreOffice PDF export failed: ' + result.stdout + result.stderr)
        os.replace(pdf, target)
    return target
