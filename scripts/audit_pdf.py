"""Confere páginas, texto, links e retângulos de anotação do guia."""
import argparse
import json
from pathlib import Path
from pypdf import PdfReader

def audit(path):
    doc=PdfReader(path);links=[];counts=[]
    if len(doc.pages)!=16:raise ValueError('O guia deve ter 16 páginas.')
    for index,page in enumerate(doc.pages,1):
        text=page.extract_text() or ''
        if len(text)<80:raise ValueError(f'Página {index} sem texto suficiente.')
        if chr(65533) in text:raise ValueError(f'Caractere de substituição na página {index}.')
        count=0
        for ref in page.get('/Annots',[]):
            ann=ref.get_object()
            if ann.get('/Subtype')!='/Link':continue
            rect=[float(x) for x in ann['/Rect']]
            left,bottom,right,top=rect
            if not (0<=left<right<=float(page.mediabox.width) and 0<=bottom<top<=float(page.mediabox.height)):
                raise ValueError(f'Área de link fora da página {index}.')
            action=ann.get('/A',{})
            uri=action.get('/URI')
            if uri and not uri.startswith('https://'):raise ValueError('Link externo inseguro ou incompleto.')
            if not uri and '/Dest' not in ann and action.get('/S')!='/GoTo':raise ValueError('Botão sem destino.')
            links.append({'page':index,'rect':rect,'url':uri or 'destino interno'});count+=1
        if count==0:raise ValueError(f'Página {index} sem botão navegável.')
        counts.append(count)
    return {'pages':len(doc.pages),'links':len(links),'links_per_page':counts,'unique_external_urls':sorted({x['url'] for x in links if x['url'].startswith('https://')}),'annotations':links,'passed':True}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf');p.add_argument('--output');a=p.parse_args()
    result=audit(a.pdf)
    if a.output:Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='annotations'},ensure_ascii=False,indent=2))
