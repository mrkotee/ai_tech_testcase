from threading import Thread
import csv
from datetime import datetime as dt
from models import Document, Rubric, db

FILENAME = "posts.csv"


def create_db(alchemy_session):
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
                    alchemy_session.commit()
                document.rubrics.append(base_rubric)

    try:
        file = open(FILENAME)
        reader = csv.DictReader(file)
        documents = list(reader)
        # go_through(reader)
    except UnicodeDecodeError:
        file = open(FILENAME, encoding="utf_8_sig")
        reader = csv.DictReader(file)
        documents = list(reader)
        # go_through(reader)

    # threads = []
    doc_len = len(documents)
    prev = 0
    base_rubrics = {rubric.name: rubric for rubric in Rubric.query.all()}
    for i in range(100, doc_len, 100):
        doc_slice = slice(prev, i)
        print(doc_slice)
        prev = i
        go_through(documents[doc_slice], alchemy_session, base_rubrics)
        alchemy_session.commit()
        # thread = Thread(target=go_through, args=(documents[doc_slice], alchemy_session, base_rubrics))
        # thread.start()
        # threads.append(thread)
    else:
        doc_slice = slice(prev, i)
        print(doc_slice)
        go_through(documents[doc_slice], alchemy_session, base_rubrics)
        alchemy_session.commit()
        # thread = Thread(target=go_through, args=(documents[doc_slice], alchemy_session, base_rubrics))
        # thread.start()
        # threads.append(thread)

    file.close()


if __name__ == '__main__':
    session = db.session
    create_db(session)

    # import cProfile
    # import pstats
    #
    # pr = cProfile.Profile()
    # pr.enable()
    # create_db(session)
    # pr.disable()
    #
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
