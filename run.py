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

@dataclass
class Summary:
    document_id: int
    summary: str

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
            summary = Summary(doc_id, s_text)
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