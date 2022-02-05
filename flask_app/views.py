import flask
from database.models import Document, Rubric, db
from database.elastic import ElasticConnection
from settings import elastic_index, elastic_url
from .app import app

session = db.session

e_connection = ElasticConnection(elastic_url)


@app.get("/document/search")
def search_doc():
    text = flask.request.args.get('text')
    if not text:
        return "empty request", 400
    e_response = e_connection.search_by_text(elastic_index, text)
    if not e_response:
        return "document not found", 400
    base_ids = [e_item["base_id"] for e_item in e_response.values()]
    base_documents = Document.query.filter(Document.id.in_(base_ids)).order_by(Document.created_date).all()
    response = [{"id": doc.id,
                 "text": doc.text,
                 "rubrics": [rub.name for rub in doc.rubrics],
                 "created_date": doc.created_date.strftime("%Y-%m-%d %H:%M:%S")} for doc in base_documents]

    return {"items": response}


@app.delete("/document/<item_id>")
def delete_doc_by_id(item_id):
    if not item_id.isdigit():
        return "id must be an integer", 400
    base_item = Document.query.get(item_id)
    e_item = e_connection.search_by_base_id(elastic_index, item_id)
    if not base_item:
        return "document not found", 400

    response = {"deleted_document": {"id": base_item.id,
                 "text": base_item.text,
                 "rubrics": [rub.name for rub in base_item.rubrics],
                 "created_date": base_item.created_date.strftime("%Y-%m-%d %H:%M:%S")}}

    base_item.delete()
    e_connection.delete_by_id(elastic_index, e_item.popitem()[0])

    return {"response": response}

