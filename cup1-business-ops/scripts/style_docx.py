import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document(sys.argv[1])
for s in d.styles:
    try:
        if s.font is not None:
            s.font.name='Arial'
            rpr=s.element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
            if rf is None: rf=OxmlElement('w:rFonts'); rpr.append(rf)
            for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),'Arial')
    except Exception: pass
d.styles['Normal'].font.size=Pt(10)
for n,sz in (('Title',22),('Subtitle',12),('Heading 1',15),('Heading 2',12)):
    try:
        st=d.styles[n]; st.font.size=Pt(sz); st.font.color.rgb=RGBColor(0x1F,0x4E,0x5A); st.font.bold = n!='Subtitle'
    except KeyError: pass
for sec in d.sections:
    sec.left_margin=sec.right_margin=Cm(2); sec.top_margin=sec.bottom_margin=Cm(2)
for t in d.tables:
    tblPr=t._tbl.tblPr; b=OxmlElement('w:tblBorders')
    for e in ('top','left','bottom','right','insideH','insideV'):
        el=OxmlElement(f'w:{e}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:color'),'AAAAAA'); b.append(el)
    tblPr.append(b)
    for i,row in enumerate(t.rows):
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size=Pt(8.5)
                    if i==0: r.font.bold=True; r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)
            if i==0:
                sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'1F4E5A'); c._tc.get_or_add_tcPr().append(sh)
d.save(sys.argv[2])
