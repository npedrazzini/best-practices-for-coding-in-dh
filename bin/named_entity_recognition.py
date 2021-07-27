#!/usr/bin/env python
# coding: utf-8
"""NER project (reproduced) from RSE Summer School"""
from bs4 import BeautifulSoup
import en_core_web_sm
import spacy
import json
from spacy import displacy
from pathlib import Path

def extract_text():
    """Extracts transcription"""
    with open("/Users/nilo/RSE-summerschool/best-practices-for-coding-in-dh/data/henslow/letters_152.xml", encoding="utf-8") as file:
        letter = BeautifulSoup(file, "lxml-xml")
    transcription = letter.find(type="transcription").text
    transcription = transcription.replace("& ", "and ")
    return transcription

def ner(text):
    """Extracts NER from transcription"""
    nlp = en_core_web_sm.load()
    document = nlp(text)
    for entity in document.ents:
        print(f"{entity.text}: {entity.label_}")
    return document

def write_json(document):
    """Write json"""
    doc_dict = document.to_json()
    ents_dict = {key: value for (key, value) in doc_dict.items() if key == "ents"}
    json.dumps(ents_dict)

def write_html_viz(document):
    """Write HTML"""
    output_file = Path("/Users/nilo/RSE-summerschool/best-practices-for-coding-in-dh/results/ent_viz.html")
    document.user_data[
        "title"
    ] = "Letter from William Christy, Jr., to John Henslow, 26 February 1831"

    html = displacy.render(document, style="ent", jupyter=False, page=True)
    output_file.open("w", encoding="utf-8").write(html)

def main():
    text = extract_text()
    document = ner(text)
    write_json(document)
    write_html_viz(document)

if __name__ == "__main__":
    main()
