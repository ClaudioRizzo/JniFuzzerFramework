"""
database_tools.py
~~~~~~~~~~~~~~~~~

This modules provides methods to load data into the database.
It also exports all the necessary metadata to interact with the DB
"""
import json
import argparse
import apk_tags as at

from pymongo import MongoClient
from tqdm import tqdm

DB_NAME = 'TaintSaviour'
DB_HOST = 'localhost'
DB_PORT = 27017

# TODO (clod, tp) we need to avoid have hardcoded strings
# we should consider stardadize our tags into one big module


def load_flows_from_json(flows_json):
    assert type(flows_json) is list
    print('[info] loading flows to database')

    for result_dict in tqdm(flows_json):
        result = result_dict['result']
        apk_id = result['apk']

        for flow in result['flows']:
            sink = flow['sink']
            db_flow = Flow(sink, apk_id)
            for source in flow['sources']:
                db_flow.add_source(source)

            # Adding the flow to the db
            db_flows = mongo_db.flows
            flow_id = db_flows.insert_one(db_flow.to_mongo()).inserted_id

            # updating the apk
            db_apks = mongo_db.apks
            db_apks.find_one_and_update(
                {'_id': apk_id}, {"$push": {"flows": str(flow_id)}})


def _create_library(apk_id, library):

    isa = library.get('isa')
    db_library = Library(library['name'], library['sha256'])
    if isa is not None:
        db_library = Library(library['name'], library['sha256'], isa=isa)

    for symbol in library['symbols']:
        sym = symbol['symbol']
        db_symbol = Symbol(sym['name'], sym['count'])

        # inserting symbol in to the db
        db_symbols = mongo_db.symbols
        symbol_id = db_symbols.insert_one(
            db_symbol.to_mongo()).inserted_id

        # adding the just added symbol as a reference to the current library
        db_library.add_symbol(symbol_id)

    db_library.add_apk(apk_id)

    # adding the library into the database and returning its id
    db_libraries = mongo_db.libraries
    library_id = db_libraries.insert_one(db_library.to_mongo()).inserted_id

    return library_id


def _update_library(apk_id, library):
    db_libraries = mongo_db.libraries

    # note that I look for _id rather than sha256 as in mongo
    # the entry id is _id!
    db_libraries.find_one_and_update({'_id': library['_id']}, {
                                     "$push": {"apks": str(apk_id)}})

    return library['_id']


def _load_libraries(apk_id, libraries):
    '''Load libraries into the database and return a list of ids (sha256)
    when done
    '''
    library_ids = set()
    for library in libraries:
        lib = library['library']
        lib_sha256 = lib['sha256']

        db_libraries = mongo_db.libraries
        extracted_lib = db_libraries.find_one({'_id': lib_sha256})

        if extracted_lib is None:
            # we create a brand new library
            library_ids.add(_create_library(apk_id, lib))

        else:
            # we only need to update it
            library_ids.add(_update_library(apk_id, extracted_lib))

    return library_ids


def load_from_jnienv_stats(jnienv_stats):
    assert type(jnienv_stats) is dict
    print('[info] loading jnienv statistics to database')

    apks = jnienv_stats['results']

    for curr_apk in tqdm(apks):
        apk = curr_apk['apk']
        apk_id = apk['apk_id']
        db_apk = Apk(apk_id)

        library_ids = _load_libraries(apk_id, apk['libraries'])

        # adding library id to the apk
        for lib_id in library_ids:
            db_apk.add_library(lib_id)

        db_apks = mongo_db.apks
        db_apks.insert_one(db_apk.to_mongo())


def load_libraries_from_jnienv(jnienv_stats):
    '''Only insert libraries into the databes. It will update
    all the apk as well.'''

    assert type(jnienv_stats) is dict
    print('[info] loading libraries to database')
    
    apks = jnienv_stats['results']
    for apk_entry in tqdm(apks):
        apk = apk_entry['apk']
        if mongo_db.apks.find_one({'_id': apk['apk_id']}) is None:
            continue

        libraries_ids = _load_libraries(apk['apk_id'], apk['libraries'])
        
        for lib_id in libraries_ids:
            mongo_db.apks.find_one_and_update({'_id': apk['apk_id']}, {'$addToSet': {'libraries':lib_id}})


def load_standard_tags():
    for tag_color in at.tags:
        tag = Tag(tag_color)
        tag_id = mongo_db.tags.insert_one(tag.to_mongo()).inserted_id

        mongo_db.apks.update_many({}, {"$push": {
            "tags": {
                "tag_id": str(tag_id),
                "active": False,
                "color": tag.color}}})


class Symbol:
    def __init__(self, name, count=0):
        self._name = name
        self.count = count

    def to_mongo(self):
        return {'name': self._name, 'count': self.count}


class Flow:
    def __init__(self, sink, apk_id):
        self._apk_id = apk_id
        self._sink = sink
        self._sources = []

    def add_source(self, source):
        if source is not None:
            self._sources.append(source)

    def to_mongo(self):
        return {
            'apk_id': self._apk_id,
            'sink': self._sink,
            'sources': self._sources
        }


class Library:
    def __init__(self, name, sha256, isa='armeabi-v7a'):
        self._name = name
        self._symbols = set()
        self._apks = set()
        self.fail = False
        self._sha256 = sha256
        self._isa = isa

    def add_symbol(self, symbol):
        if symbol is not None:
            self._symbols.add(symbol)

    def add_apk(self, apk):
        if apk is not None:
            self._apks.add(apk)

    def to_mongo(self):
        return {
            '_id': self._sha256,
            'name': self._name,
            'symbols': list(self._symbols),
            'apks': list(self._apks),
            'fail': self.fail,
            'isa': self._isa
        }


class Tag:
    def __init__(self, color):
        self.color = color
        self._label = ''
        self._standard = True

    def to_mongo(self):
        return {'color': self.color,
                'label': self._label,
                'standard': self._standard}


class Apk:
    def __init__(self, sha256):
        self._id = sha256
        self._libraries = set()
        self._flows = set()
        self.tags = []

    def add_library(self, library):
        if library is not None:
            self._libraries.add(library)
        else:
            print('[warning] A none library has been found')

    def add_flow(self, flow):
        if flow is not None:
            self._flows.add(flow)

    def to_mongo(self):
        return {
            '_id': self._id,
            'libraries': list(self._libraries),
            'flows': list(self._flows),
            'tags': self.tags
        }


if __name__ == '__main__':
    client = MongoClient(DB_HOST, DB_PORT)
    mongo_db = client[DB_NAME]

    parser = argparse.ArgumentParser(
        description='TaintSaviour WebApp Database Tools')

    parser.add_argument('-j', '--load-jsons', nargs=2,
                        help="""Given jnienv_statistics.json and flowdroid_stats.json 
                        files (in this order) as input, a mongo DB 
                        TaintSaviour is generated""")

    parser.add_argument('-env', '--jni-env-stats',
                        help="""Load jnienv stats into the database from json file
                        Note that any entry (apk or library) already in the database
                        will be overridden.
                        """)
    
    parser.add_argument('-l', '--libraries',
                         help="""loads libraries from jnienv stats file""")

    args = parser.parse_args()

    if args.libraries:
        stats = args.libraries
        with open(stats, 'rt') as f:
            load_libraries_from_jnienv(json.load(f))

    elif args.load_jsons:
        jnienv_stats = args.load_jsons[0]
        flowdroid_stats = args.load_jsons[1]

        with open(jnienv_stats, 'rt') as f:
            load_from_jnienv_stats(json.load(f))

        with open(flowdroid_stats, 'rt') as f:
            load_flows_from_json(json.load(f))

        load_standard_tags()
