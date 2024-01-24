import logging


class NoDuplicatesFilter(logging.Filter):   
    def filter(self, record):
        # Adiciona um atributo para o registro para verificar duplicatas
        if not hasattr(self, 'unique_records'):
            self.unique_records = set()
        record_key = (record.msg, record.levelname)
        if record_key not in self.unique_records:
            self.unique_records.add(record_key)
            return True
        return False