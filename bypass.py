import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import nltk
from nltk.corpus import wordnet
import random

# Download necessary nltk data
nltk.download('punkt')
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")


def get_synonyms(word):
    """Fetch synonyms for a word from WordNet."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            syn_name = lemma.name().replace("_", " ").replace("-", " ")
            synonyms.add(syn_name)
    synonyms.discard(word)  # Remove the original word
    return list(synonyms)


def replace_words(text, replacement_rate):
    """Replace words with their synonyms based on a replacement rate."""
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    replaced_words = []

    for word, tag in tagged:
        if tag.startswith(("NN", "VB", "JJ", "RB")) and random.random() < replacement_rate:
            synonyms = get_synonyms(word)
            if synonyms:
                new_word = random.choice(synonyms)
                replaced_words.append(new_word)
            else:
                replaced_words.append(word)
        else:
            replaced_words.append(word)

    return " ".join(replaced_words)


def process_text():
    """Process input text and display the paraphrased version."""
    input_text = input_text_area.get("1.0", tk.END).strip()
    replacement_rate = slider.get() / 100  # Convert percentage to decimal
    processed_text = replace_words(input_text, replacement_rate)
    output_text_area.delete("1.0", tk.END)
    output_text_area.insert(tk.END, processed_text)


# Tkinter GUI setup
root = tk.Tk()
root.title("Text Paraphraser")

# Input text area
tk.Label(root, text="Input Text:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
input_text_area.grid(row=1, column=0, padx=10, pady=5)

# Output text area
tk.Label(root, text="Paraphrased Text:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
output_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
output_text_area.grid(row=3, column=0, padx=10, pady=5)

# Replacement rate slider
tk.Label(root, text="Replacement Rate (%):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=300)
slider.set(30)  # Default replacement rate is 30%
slider.grid(row=5, column=0, padx=10, pady=5)

# Submit button
submit_button = tk.Button(root, text="Paraphrase", command=process_text)
submit_button.grid(row=6, column=0, padx=10, pady=10)

root.mainloop()

