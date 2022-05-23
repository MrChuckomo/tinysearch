"""
File         : processor.py
Description  : 
Author       : Alexander Kettler
Creation Date: 23-May-2022
"""

import os
import uuid

from enum import Enum
from dataclasses import Field, field
from dataclasses import dataclass
from tinydb import TinyDB


# ---------------------------------------------------------------------------------------------------------------------

class DataType(Enum):
    UNKNWON = 'unknown'
    STRING = 'string'
    INT = 'int'

@dataclass
class DataField():
    value: str
    name: str
    _data_type: DataType = field(init=False, default=DataType.UNKNWON)

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            self._data_type = DataType.STRING
        elif type(self.value) == int:
            self._data_type = DataType.INT
        else:
            self._data_type = DataType.UNKNWON

@dataclass
class DataRow():
    fields: list[DataField] = field(default_factory=list)
    _id: str = field(init=False, default_factory=uuid.uuid4)

@dataclass
class DataTable():
    name: str
    rows: list[DataRow] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = self.name.lower()

@dataclass
class Store():
    """Store and Lookup saved side by side"""
    data: DataTable
    data_db: str = field(init=False, default=None)
    lookup_db: str = field(init=False, default=None)
    workdir: str = os.path.abspath('./store')

    def __post_init__(self) -> None:
        if not self.exists:
            self._create()
        self.data_db = TinyDB(os.path.abspath(f'{self.workdir}{os.sep}ds-0000001-{self.data.name}.db.json'))
        self.lookup_db = TinyDB(os.path.abspath(f'{self.workdir}{os.sep}ls-{self.data.name}.db.json'))

    @property
    def exists(self) -> None:
        return True if os.path.exists(os.path.abspath(self.workdir)) else False

    def scan(self) -> None:
        """Scan for existing data stores"""
        pass

    def save_data(self) -> None:
        for row in self.data.rows:
            doc = {'_id': str(row._id)}
            for field in row.fields:
                doc[field.name] = field.value
            self.data_db.insert(doc)

    def save_lookup(self) -> None:
        """lookup table structure

        word:str | items:list
        """
        pass

    def _create(self) -> None:
        os.mkdir(os.path.abspath(self.workdir))

@dataclass
class LanguageProcessor():
    sentence: str

    def _sanatize(self):
        pass

def insert(data: dict, table_name: str) -> bool:
    fields = [DataField(name=key, value=data[key]) for key in data.keys()]
    row = DataRow(fields)
    dt = DataTable(name=table_name, rows=[row])

    print(dt)

    store = Store(data=dt)

    print(store)
    store.save_data()



if __name__ == '__main__':
    insert(
        table_name='test',
        data={
            'content': 'some search string',
            'value': 1234
        }
    )
    insert(
        table_name='test',
        data={
            'content': 'another string of text',
            'value': 5678
        }
    )
