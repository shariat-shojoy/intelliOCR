import fitz

doc = fitz.open("WB_BANGLA_ACADEMY_WORD_LIST.pdf")

page = doc[0]

print("========== get_text() ==========")
print(page.get_text()[:2000])

print("\n========== get_text('words') ==========")
words = page.get_text("words")
print("Number of words:", len(words))

if words:
    print(words[:20])

doc.close()