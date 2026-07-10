INPUT_FILE = "E:\\ocr\\all_bangla_words.txt"
OUTPUT_FILE = "E:\\ocr\\all_unique_bangla_words.txt"



words = set()

with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    for line in infile:
        # Remove leading/trailing spaces and normalize multiple spaces
        word = " ".join(line.split())

        if word:
            words.add(word)

# Sort alphabetically
sorted_words = sorted(words)

with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for word in sorted_words:
        outfile.write(word + "\n")

print(f"Total unique words: {len(sorted_words)}")
print(f"Saved to: {OUTPUT_FILE}")