# -*- coding: utf8 -*-
import json

from permission_admin.models import Dataset


class Datasets:
    """ Datasets class
    """
    def __init__(self):
        self.datasets = self._build_datasets_map()
        self.mapping_id = None

    @staticmethod
    def _build_datasets_map():
        datasets = {}
        for dataset in Dataset.objects.all():
            pk = dataset.pk
            index = dataset.index
            mapping = dataset.mapping
            datasets[pk] = {'index': index, 'mapping': mapping}
        return datasets

    def activate_dataset(self, session):
        """ Activate dataset for a given session. If the session does not contain
            information about the dataset, initiates with the first valid dataset
            Returns: the session object containing the active dataset mapping_id
        """
        if len(self.datasets.keys()) > 0:
            if 'dataset' not in session:
                session['dataset'] = list(self.datasets.keys())[0]
            self.mapping_id = int(session['dataset'])
        return self

    def is_active(self):
        return self.mapping_id is not None

    def get_index(self):
        """ Returns: the active dataset index, None otherwise
        """
        index = None
        if self.is_active():
            index = self.datasets[self.mapping_id]['index']
        return index

    def get_mapping(self):
        """ Returns: the active dataset mapping, None otherwise
        """
        mapping = None
        if self.is_active():
            mapping = self.datasets[self.mapping_id]['mapping']
        return mapping

    def get_datasets(self):
        """ Returns: map of all dataset objects
        """
        return self.datasets

    def build_manager(self, manager_class):
        """ Builds manager_class as:
            ManagerClass(index, mapping, date_range)
        """
        index = self.get_index()
        mapping = self.get_mapping()
        return manager_class(index, mapping)
