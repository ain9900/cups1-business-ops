# Scripts

| Script | What it does | Run |
|---|---|---|
| `build_sourcing_model.py` | Rebuilds `deliverables/phase2/Cup1_Phase2_Sourcing_Model.xlsx` (supplier comparison, landed cost model, tariffs, RFQ tracker). Edit the inputs in the script, or edit the yellow cells in Excel directly | `pip install openpyxl` then `python scripts/build_sourcing_model.py` (open in Excel to recalculate) |
| `style_docx.py` | Applies Cup1 styling (Arial, teal headings, bordered tables) to a Word file made by pandoc | `pandoc docs/phases/phase3-brand-strategy.md -o raw.docx --resource-path=docs/phases` then `python scripts/style_docx.py raw.docx out.docx` |
| `homepage_blueprint.html` | Source of `brand/homepage-blueprint.png`; open it in a browser to view or edit | Open in any browser |

To make a PDF from a Word file: open it in Word or LibreOffice and export as PDF (`soffice --headless --convert-to pdf file.docx`).
