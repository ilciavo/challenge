from flask import Flask, request, abort
from dataclasses import dataclass
import json

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

    def summarize(self, sum_id:int):
        text = self.db[sum_id].text
        #s_text = summarize(text)
        s_text = 'this is a dummy summary'
        summary = Document(sum_id, s_text)
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

@app.route('/', methods = ['GET'])
def get_summary():
    sum_id = request.args.get('sum_id')
    summary = service.summarize(sum_id)
    if summary is not None:
        return summary.__dict__
    else:
        abort(404)

if __name__ == '__main__':
    app.run()