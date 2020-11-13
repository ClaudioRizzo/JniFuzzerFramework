# -*- coding: utf-8 -*-

"""
tsbackend.models.apks
~~~~~~~~~~~~~~~~~~~~~

This module contains helper functions for manipulating database records
primarily to support the routes defined in `tsbackend.views.apks`.

"""
from datetime import datetime

from bson import ObjectId
from flask import current_app


def find_library(lib_id) -> dict:
    """Retrieve a library document from the database.

    Args:
        lib_id (str): The id of the library to retrieve.

    Returns:
        dict: A dictionary corresponding to the requested library.
    """
    library = current_app.db.libraries.find_one({'_id': lib_id})
    library['symbols'] = [find_symbol(x) for x in library['symbols']]
    library['_id'] = str(library['_id'])
    return library


def find_flow(flow_id) -> dict:
    """Retrieve a flow document from the database.

    Args:
        flow_id (str): The id of the flow to retrieve.

    Returns:
        dict: A dictionary corresponding to the requested flow.
    """
    if isinstance(flow_id, str):
        flow_id = ObjectId(flow_id)
    flow = current_app.db.flows.find_one({'_id': flow_id})

    flow['_id'] = str(flow['_id'])

    if flow.get('path') is not None:
        flow['path'] = [find_method_path_by_id(x) for x in flow.get('path')]
    return flow


def find_symbol(sym_id) -> dict:
    """Retrieve a symbol document from the database.

    Args:
        sym_id (str): The id of the symbol to retrieve.

    Returns:
        dict: A dictionary corresponding to the requested symbol.
    """
    symbol = current_app.db.symbols.find_one({'_id': sym_id})
    symbol['_id'] = str(symbol['_id'])
    return symbol


def find_note(note_id) -> dict:
    """Retrieve a note document from the database.

    Args:
        note_id (str): The id of the note to retrieve.

    Returns:
        dict: A dictionary corresponding to the requested note.
    """
    note = current_app.db.notes.find_one({'_id': ObjectId(note_id)})
    note['_id'] = str(note['_id'])
    return note


def find_apks_starts_with(partial_id) -> list:
    """Retrieve a list of apk ids from the database, whose
    ids start with partial_id.

    Args:
        partial_id (str): Part of the apk id

    Returns:
        list: A list of apk id matchin the query
    """
    apks = current_app.db.apks.find({'_id': {'$regex': '^{}'
                                             .format(partial_id)}},
                                    {'flows': 0,
                                     'libraries': 0, 'notes': 0})

    apk_ids = [apk['_id'] for apk in apks]
    return apk_ids


def get_standard_tags() -> list:
    """Retrieve this project standard tags

    Returns:
        list: list of standard tags
    """
    return [tag for tag in current_app.db.tags.find({'standard': True},
                                                    {'_id': 0})]


def find_libraries(libraries_list):
    if libraries_list is None:
        return []

    libraries = []
    for library in libraries_list:
        library['apks'] = find_apks_by_library(library.get('_id'))
        libraries.append(library)
    return libraries


def find_apks_by_library(library_id):
    if library_id is None:
        return ""
    apk_ids = current_app.db.libraries.find_one({'_id': library_id},
                                                {'_id': 0, 'apks': 1})['apks']


    return [apk for apk in current_app.db.apks.find({'_id': {'$in': apk_ids}})]


def find_apk_list(apks_list) -> list:
    """Returns a list of apk ids, it returns a list of apks instances"""
    if apks_list is None:
        return []
    return [find_apk(apk_id) for apk_id in apks_list]


def find_apk(apk_id) -> dict:
    """Retrieve an apk document from the database.

    This function also resolves all sub-documents of the apk,
    fetching all necessary libraries, flows, and notes by their
    ids also.

    Args:
        apk_id (str): The id of the apk to retrieve.

    Returns:
        dict: A dictionary corresponding to the requested apk. None if no apk is found
    """
    apk = current_app.db.apks.find_one({'_id': apk_id})

    if apk is None:
        return None

    if 'notes' not in apk:
        apk['notes'] = []

    libs = [find_library(x) for x in apk['libraries']]
    # Sort libraries by most symbols first (most interesting)
    libs = sorted(libs, key=lambda x: len(x['symbols']), reverse=True)
    apk['libraries'] = libs
    apk['flows'] = [find_flow(x) for x in apk['flows']]
    apk['notes'] = [find_note(x) for x in apk['notes']]
    
    manifest_bytes = apk.get('manifest')
    apk['manifest'] = manifest_bytes.decode('utf-8') if manifest_bytes is not None else ""
    apk['_id'] = str(apk['_id'])

    return apk


def find_flows_by_apk(apk_id) -> list:
    """Retrieve all flow documents related to a given apk.

    Args:
        apk_id (str): The id of the apk of interest.

    Returns:
        list: A list containing the related flows.
    """
    apk = find_apk(apk_id)
    if apk is None:
        return None
    return [find_library(x) for x in apk['flows']]


def find_libs_by_apk(apk_id) -> list:
    """Retrieve all library documents related to a given apk.

    Args:
        apk_id (str): The id of the apk of interest.

    Returns:
        list: A list containing the related libraries.
    """
    apk = find_apk(apk_id)
    if apk is None:
        return None
    libs = [find_library(x) for x in apk['libraries']]
    # Sort libraries by most symbols first (most interesting)
    return sorted(libs, key=lambda x: len(x['symbols']), reverse=True)


def find_notes_by_apk(apk_id) -> list:
    """Retrieve all note documents related to a given apk.

    Args:
        apk_id (str): The id of the notes of interest.

    Returns:
        list: A list containing the related notes.
    """
    apk = find_apk(apk_id)
    if apk is None:
        return None
    notes = [find_note(x) for x in apk['notes']]
    # Sort notes chronologically (the datetime format should allow it)
    return sorted(notes, key=lambda x: len(x['time']))
    # return list(current_app.db.notes.find({"_id": {"$in": apk['notes']}}))


def delete_note(note_id):
    """Remove a note from the database.

    Args:
        note_id (str): The id of the note to delete.

    """
    note = current_app.db.notes.find_one_and_delete({'_id': ObjectId(note_id)})
    current_app.db.apks.find_one_and_update(
        {'_id': note['apk_id']}, {"$pull": {'notes': ObjectId(note_id)}})


def add_note(title, text, apk_id=None) -> dict:
    """Adds a note to the database related to a given apk.

    Args:
        title (str): The title of the note.
        text (str): The text making up the body of the note.
        apk_id (str): The apk to add the note to.

    Returns:
        dict: Returns the note along with updated id and timestamp.
    """
    note = {
        'apk_id': apk_id,
        'title': title,
        'text': text,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    note_id = current_app.db.notes.insert_one(note).inserted_id

    if apk_id:
        current_app.db.apks.find_one_and_update(
            {'_id': apk_id}, {"$push": {"notes": note_id}})

    note['note_id'] = str(note_id)
    return note


def set_tag(apk_id, tag, active):
    """Sets a tag as active or inactive on a given apk.

    Args:
        apk_id (str): The apk to add the tag to.
        tag (str): The tag to add.
        active (bool): Whether the tag is active or not.

    """
    current_app.db.apks.find_one_and_update(
        {'_id': apk_id, "tags.tag_id": tag},
        {"$set": {"tags.$.active": active}})


def list_apks_with_flows() -> list:
    """Find all apk ids of apks related to flows.

    Returns:
        list: The list of all apk ids of apks with flows.
    """
    results = current_app.db.apks.find(
        {"flows": {'$exists': True, '$ne': []}})
    return [str(x['_id']) for x in results]


def list_apk_summaries_with_flows() -> list:
    """Generate apk summaries for all apks related to flows.

    Returns:
        list: The list of apk summaries for apks with flows.
    """
    results = current_app.db.apks.find(
        {"flows": {'$exists': True, '$ne': []}})
    summaries = [
        {'_id': str(x['_id']),
         'tags': x['tags'],
         'n_flows': len(x['flows']),
         'n_libs': len(x['libraries']),
         'n_notes': (0 if 'notes' not in x else len(x['notes']))}
        for x in results]
    summaries = sorted(summaries, key=lambda x: x['n_flows'], reverse=True)
    return summaries


def find_method_path_by_id(_id):
    path_method = current_app.db.path_method.find_one({'_id': ObjectId(_id)})
    path_method['_id'] = str(path_method['_id'])
    return path_method