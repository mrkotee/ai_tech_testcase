from elasticsearch import Elasticsearch


class ElasticConnection:

    def __init__(self, url):
        self.elastic_obj = Elasticsearch(url)

    def ping(self):
        return self.elastic_obj.ping()

    def create_index(self, index):
        if self.elastic_obj.indices.exists(index):
            return True

        self.elastic_obj.indices.create(index=index)

    def is_index_exist(self, index):
        return self.elastic_obj.indices.exists(index)

    def add_item(self, index: str, item: dict):
        self.elastic_obj.index(index=index, document=item)

    def search_by_text(self, index, text, query_size=20):
        query_body = {
                "match": {'text': text}
            }
        result = self.elastic_obj.search(index=index, query=query_body, size=20)
        return {res["_id"]: res["_source"] for res in result['hits']['hits']}

    def search_by_base_id(self, index, item_base_id):
        query_body = {
            "match": {'base_id': item_base_id}
        }
        result = self.elastic_obj.search(index=index, query=query_body, size=1)
        return {res["_id"]: res["_source"] for res in result['hits']['hits']}

    def get_all_by_index(self, index, expected_size: int):
        return self.elastic_obj.search(index=index, size=expected_size, query={"match_all": {}})['hits']['hits']

    def delete_by_id(self, index, item_id):
        res = self.elastic_obj.delete(index=index, id=item_id)
        if res["result"] == 'deleted':
            return True
        return False
