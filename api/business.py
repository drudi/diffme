import redis, json, pickle, difflib
from api.exceptions import *
"""
Business logic for computing the diffs
"""

class RawData(object):
    _db_addr = '127.0.0.1'
    _db_port = 6379
    _db_conn = None

    def __init__(self):
        self._db_conn = redis.StrictRedis(
                host=self._db_addr,
                port=self._db_port,
                db=0
                )

    def write(self, key, data):
        self._db_conn.set(key, data)

    def read(self, key):
        return self._db_conn.get(key)

class Base():
    def put(self, data):
        """
        Receives decoded data and writes it to storage
        """
        self.dataImpl.write(self.key, data)

    def get(self):
        """
        Retrieves data from storage as a json encoded string
        """
        data = self.dataImpl.read(self.key)
        return data


class Right(Base):
    def __init__(self, dataImpl):
        self.dataImpl = dataImpl
        self.key = 'right'


class Left(Base):
    def __init__(self, dataImpl):
        self.dataImpl = dataImpl
        self.key = 'left'

class Diff():
    def __init__(self):
        self.right = Right(RawData())
        self.left  = Left(RawData())

    def getDiff(self):
        """
        Retrieve previusly stored data from left and right and
        returns a python object describing the differences (if any)
        """

        try:
            right_data = self.right.get()
            right_data = pickle.loads(right_data)
        except TypeError:
            raise NotFoundException('No data on right endpoint.')

        try:
            left_data = self.left.get()
            left_data = pickle.loads(left_data)
        except TypeError:
            raise NotFoundException('No data on left endpoint.')

        diff = {'diffs': []}

        if right_data == left_data:
            diff['equal'] = True
            diff['same_size'] = True

        elif len(str(right_data)) != len(str(left_data)):
            diff['equal'] = False
            diff['same_size'] = False

        else:
            diff['equal'] = False
            diff['same_size'] = True

            # Compute diffs
            differ = difflib.Differ()
            diffs = list(differ.compare(str(left_data), str(right_data)))

            offset = None
            lenght = 0

            for i in enumerate(diffs):

                # Equal
                if i[1][0] == ' ':
                    if offset is not None:
                        diff['diffs'].append([offset, lenght])
                        offset = None
                        lenght = 0

                # Found a diff
                elif i[1][0] == '-':
                    lenght += 1
                    if offset is None:
                        offset = i[0]

        return diff


