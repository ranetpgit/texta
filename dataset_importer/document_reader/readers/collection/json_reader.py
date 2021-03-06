from collection_reader import CollectionReader
import json


class JSONReader(CollectionReader):

    @staticmethod
    def get_features(**kwargs):
        directory = kwargs['directory']

        for file_path in JSONReader.get_file_list(directory, 'json'):
            with open(file_path, encoding='utf8') as json_file:
                for line_idx, line in enumerate(json_file):
                    features = json.loads(line.strip())
                    features['_texta_id'] = '{0}_{1}'.format(file_path, line_idx)
                    yield features

    @staticmethod
    def count_total_documents(**kwargs):
        directory = kwargs['directory']

        total_documents = 0

        for file_path in JSONReader.get_file_list(directory, 'json'):
            with open(file_path, encoding='utf8') as json_file:
                total_documents += sum(1 for row in json_file)

        return total_documents
