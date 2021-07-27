#!/usr/bin/env python
# coding: utf-8
"""NER project (reproduced) from RSE Summer School"""
from bs4 import BeautifulSoup
import en_core_web_sm
import spacy
import json
from spacy import displacy
from pathlib import Path
import PySimpleGUI as sg

def _write_file(filepath, content):
    """
    Write content to specified file.

    Parameters
    ----------
    filepath : str or Path
        The file to write to
    content : str
        The content to write to file

        """
    output_file = Path(filepath).resolve()
    output_file.open("w", encoding="utf-8").write(content)


def extract_text():
    """
    Extract text from an XML file transcription.

    Parameters
    ----------
    filepath : str or Path
        The source XML file

        """
    input_file = Path(source).resolve()

    with open(input_file, encoding="utf-8") as file:
        letter = BeautifulSoup(file, "lxml-xml")
    transcription = letter.find(type="transcription").text
    transcription = transcription.replace("& ", "and ")
    return transcription

def ner(text):
    """Recognise named entities from a text.
    Parameters
    ----------
    text : str
        The text in which to recognise named entities

    Returns
    -------
    document
        a spaCy doc including named entities

    """
    nlp = en_core_web_sm.load()
    document = nlp(text)
    for entity in document.ents:
        print(f"{entity.text}: {entity.label_}")
    return document

def write_json(document):
        """Recognise named entities from a text.
        Parameters
        ----------
        document : spaCy doc
            The spaCy doc including named entities
        json dest : str or Path
            The destination JSON file to write to
        """
    doc_dict = document.to_json()

    ents_dict = {key: value for (key, value) in doc_dict.items() if key == "ents"}

    ents_json = json.dumps(ents_dict)

    _write_file(json_dest,ents_json)

def write_html_viz(document):
    """Write a displaCy named entity visualisation to HTML file.

    Parameters
    ----------
    document : spaCy doc
        The spaCy doc including named entities
    json dest : str or Path
        The destination HTML file to write to
    """
    document.user_data[
        "title"
    ] = "Letter from William Christy, Jr., to John Henslow, 26 February 1831"

    html = displacy.render(document, style="ent", jupyter=False, page=True)
    output_file.open("w", encoding="utf-8").write(html)

def main():
    sg.theme("LightGreen")
    layout = [
# Explanatory text
        [sg.Text("Generate named entity tags for a TEI-XML transcription. Entities will print to the output window.")],
# Separator
        [sg.HorizontalSeparator(pad=(2, 10))],
# Source file browser
        [sg.Text("Source XML file (required):")],
        [sg.Input(size=(75, 1), enable_events=True,key="-SOURCE-"),sg.FileBrowse(target="-SOURCE-", key="-SRC BROWSE-"),],
# Separator
        [sg.HorizontalSeparator(pad=(2, 10))],
# Explanatory text
        [sg.Text("Optionally, you can also output tags as JSON and/or as a visualisation in HTML.")],
# JSON folder browser
        [sg.Text("Output JSON folder (optional):")],
        [sg.Input(size=(75, 1), enable_events=True, key="-JSON DEST-"),sg.FolderBrowse(target="-JSON DEST-", key="-JSON BROWSE-"),],
# HTML folder browser
        [sg.Text("Output HTML visualisation folder (optional):")],
        [sg.Input(size=(75, 1), enable_events=True, key="-HTML DEST-"),sg.FolderBrowse(target="-HTML DEST-", key="-HTML BROWSE-"),],
# Separator
        [sg.HorizontalSeparator(pad=(2, 10))],
        # NER output
        [sg.Text('Output:', key='-OUTPUT TEXT-')],
        [sg.Output(size=(90, 10), key='-OUTPUT-')],
# Buttons
        [sg.Submit("Run NER", key="-SUBMIT-"),
        sg.CloseButton("Exit"),],
    ]
    window = sg.Window("Named Entity Recognition", layout)
    # text = extract_text()
    # document = ner(text)
    # write_json(document)
    # write_html_viz(document)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == '-SUBMIT-':

            source = values["-SOURCE-"]

            if source:
                json_dest = values["-JSON DEST-"]
                html_dest = values["-HTML DEST-"]

                text = extract_text(source)
                document = ner(text)

                source_name = Path(source).stem

                if json_dest:

                    json_file = (Path(json_dest).joinpath(source_name).with_suffix(".json"))
                    write_json(document, json_file)

                if html_dest:

                    html_file = (Path(html_dest).joinpath(source_name).with_suffix(".html"))
                    write_html_viz(document, html_file)

                else:
                    sg.popup(
                        f"Source XML file is required. Please try again!",
                        title="Oops!",
                        non_blocking=False,
                        keep_on_top=True,
                    )
                    continue

    window.close()

if __name__ == "__main__":
    main()
