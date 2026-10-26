"""Use the packaged document rasterizer with native Word PDF conversion on Windows."""
import importlib.util, os, subprocess, sys
from pathlib import Path
SKILL=Path('C:/Users/PUVKID/.codex/plugins/cache/openai-primary-runtime/documents/26.1013.11914/skills/documents')
HERE=Path(__file__).resolve().parent
POPPLER=Path('C:/Users/PUVKID/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
os.environ['PATH']=str(POPPLER)+os.pathsep+os.environ.get('PATH','')
spec=importlib.util.spec_from_file_location('packaged_render_docx',SKILL/'render_docx.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
def native_word(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    pdf=Path(convert_tmp_dir)/(stem+'.pdf')
    p=subprocess.run(['pwsh.exe','-NoProfile','-File',str(HERE/'word_render.ps1'),'-InputDocx',doc_path,'-OutputPdf',str(pdf)],capture_output=True,text=True)
    log=p.stdout+'\n'+p.stderr
    if p.returncode or not pdf.is_file():return '',log
    return str(pdf),log
renderer.convert_to_pdf=native_word
renderer.main()
