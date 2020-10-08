"""
REST service to store, retrieve and summarize upon request
author: leonardo.echeverria@gmail.com
"""

from flask import Flask, request, abort
from dataclasses import dataclass
from summarize import summarize_text

@dataclass
class Document:
    doc_id: int
    text: str

class DocumentService:
    def __init__(self):
        self.db = dict()
        self.next_id = 0

    def retrieve(self, doc_id: int):
        return self.db.get(int(doc_id))

    def store(self, text: str):
        self.next_id += 1
        doc = Document(self.next_id, text)
        self.db[doc.doc_id] = doc
        return doc

    def summarize(self, doc_id:int):
        text = self.db.get(int(doc_id)).text
        if text is None:
            return None
        else:
            s_text = summarize_text(text)
            #s_text = 'this is a dummy summary'
            summary = Document(doc_id, s_text)
            return summary

app = Flask(__name__)

service = DocumentService()

@app.route('/', methods = ['POST'])
def store_document():
    text = request.form['text']
    doc = service.store(text)
    return doc.__dict__

@app.route('/', methods = ['GET'])
def retrieve_document():
    doc_id = request.args.get('doc_id')
    doc = service.retrieve(doc_id)
    if doc is not None:
        return doc.__dict__
    else:
        abort(404)

@app.route('/summary', methods = ['GET'])
def get_summary():
    doc_id = request.args.get('doc_id')
    summary = service.summarize(doc_id)
    if summary is not None:
        return summary.__dict__
    else:
        abort(404)

if __name__ == '__main__':
    app.run()

#dispatcher, how to know??? ...
# host/ define a donde va
# path is unique for everymethod ... get_summary and retrieve_document have the same path
# summary necesita otro path same doc_id
# extraer una parte del path como argumento
# http://host/path1/path2/endpoint?key1=val1&key2=val2
# whatever is in the path is stable
# get request.arg.get() is not standard
# eagerly: compute summary when the text is stored
# lazy: compute upon request
# what if you request a non-existing document
# use get(key) instead of [key] to return None