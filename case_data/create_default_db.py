
import csv
from datetime import datetime as dt
from database.models import Document, Rubric
from database.elastic import ElasticConnection


def create_db(csv_filepath, alchemy_session):
    """fill database from csv file"""
    def go_through(documents: list, alchemy_session, base_rubrics: dict):
        for i, row in enumerate(documents):
            text = row['text']
            created_date = dt.strptime(row["created_date"], "%Y-%m-%d %H:%M:%S")
            rubrics = row['rubrics'][2:-2].split("', '")

            # print(f"text:{text[:40]}\ndate:{created_date}, rub:{rubrics}\n")

            document = Document(text=text, created_date=created_date)
            alchemy_session.add(document)
            for rubric in rubrics:
                base_rubric = base_rubrics.get(rubric)
                if not base_rubric:
                    base_rubric = Rubric(name=rubric)
                    base_rubrics[rubric] = base_rubric
                    alchemy_session.add(base_rubric)
                document.rubrics.append(base_rubric)
            alchemy_session.commit()

    try:
        file = open(csv_filepath)
        reader = csv.DictReader(file)
        documents = list(reader)
    except UnicodeDecodeError:
        file = open(csv_filepath, encoding="utf_8_sig")
        reader = csv.DictReader(file)
        documents = list(reader)

    # threads = []
    doc_len = len(documents)
    prev = 0
    base_rubrics = {rubric.name: rubric for rubric in Rubric.query.all()}
    for i in range(100, doc_len, 100):
        doc_slice = slice(prev, i)
        prev = i
        go_through(documents[doc_slice], alchemy_session, base_rubrics)
        alchemy_session.commit()
        # thread = Thread(target=go_through, args=(documents[doc_slice], alchemy_session, base_rubrics))
        # thread.start()
        # threads.append(thread)
    else:
        doc_slice = slice(prev, doc_len)
        go_through(documents[doc_slice], alchemy_session, base_rubrics)
        alchemy_session.commit()
        # thread = Thread(target=go_through, args=(documents[doc_slice], alchemy_session, base_rubrics))
        # thread.start()
        # threads.append(thread)

    file.close()
    return doc_len, len(base_rubrics)


def fill_elastic(index, elastic_obj: ElasticConnection):
    elastic_obj.create_index(index)
    documents = Document.query.all()

    for document in documents:
        doc_dict = {"text": document.text,
                    "base_id": document.id}
        elastic_obj.add_item(index, doc_dict)
