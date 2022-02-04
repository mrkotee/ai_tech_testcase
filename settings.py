import os

main_dir = os.getcwd()

db_path = os.path.join(main_dir, 'database', 'db.sqlite')

default_data_filepath = os.path.join(main_dir, 'case_data', 'posts.csv')

elastic_host = "localhost"
elastic_port = 9200
elastic_index = "documents"
