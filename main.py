import os
import sys
import time
from settings import db_path, default_data_filepath
from settings import elastic_index, elastic_host, elastic_port
from database import models
from database import elastic
from flask_app.views import app

if not os.path.exists(db_path):  # create sqlite db file
    print('creating default database...')
    models.db.create_all()
    from case_data.create_default_db import create_db
    doc_len, rub_len = create_db(default_data_filepath, models.db.session)
    print(f"created database with {doc_len} documents, {rub_len} rubrics")
else:
    doc_len = len(models.Document.query.all())

e_connection = elastic.ElasticConnection(elastic_host, elastic_port)
for _ in range(30):
    if e_connection.ping():
        break
    time.sleep(1)
if e_connection.ping():
    print("ElasticSearch connected")
else:
    print("Can't connect to ElasticSearch.\nStart ElasticSearch and try again")
    sys.exit(1)

if not e_connection.is_index_exist(elastic_index):
    print(f"Creating Elastic index: {elastic_index}")
    e_connection.create_index(elastic_index)

if doc_len > len(e_connection.get_all_by_index(elastic_index, doc_len)):
    print("Filling Elastic from database...")
    from case_data.create_default_db import fill_elastic
    fill_elastic(elastic_index, e_connection)


print("Starting Flask app")
app.run(debug=True)
