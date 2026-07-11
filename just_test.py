import fitz

doc = fitz.open("WB_BANGLA_ACADEMY_WORD_LIST-3-4.pdf")

page = doc[1]

pix = page.get_pixmap(dpi=600)

pix.save("first_page2.png")