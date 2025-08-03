from docxtpl import DocxTemplate

# Ladda din Word-mall
doc = DocxTemplate("kolumns.docx")

# Kontextdata: varje rad har en lista med kolumner
context = {
    "tbl_contents": [
        {"cols": ["integration tests", "rpv2", "cv90"]},
        {"cols": ["test_one", "passed", "passed"]},
        {"cols": ["test_two", "failed", "passed"]},
    ]
}

# Rendera mallen med data
doc.render(context)

# Spara resultatet
doc.save("output.docx")
