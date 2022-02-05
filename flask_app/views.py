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
        return None
    e_response = e_connection.search_by_text(elastic_index, text)
    base_ids = [e_item["base_id"] for e_item in e_response.values()]
    base_documents = Document.query.filter(Document.id.in_(base_ids)).order_by(Document.created_date).all()
    response = [{"id": doc.id,
                 "text": doc.text,
                 "rubrics": [rub.name for rub in doc.rubrics],
                 "created_date": doc.created_date.strftime("%Y-%m-%d %H:%M:%S")} for doc in base_documents]

    return {"response": response}


@app.delete("/document/<item_id>")
def delete_doc_by_id(item_id):
    base_item = Document.query.get(item_id)
    e_item = e_connection.search_by_base_id(elastic_index, item_id)

    base_item.delete()
    e_connection.delete_by_id(elastic_index, e_item.popitem()[0])

    response = 200
    return {"response": response}

