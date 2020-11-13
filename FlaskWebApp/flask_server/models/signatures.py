'''
tsbackend.models.signatures
~~~~~~~~~~~~~~~~~~~~~~

This module contains helper function to extract signatures from
the database.
'''
from flask import current_app
from bson.objectid import ObjectId


def get_fuzzable_signatures_deprecated():
    '''
    Extract a list of fuzzable signature from the Database.
    A fuzzable signature is a signature we found as a sink in our
    analysis.

    Returns:
        A dictionary of the form:
        {
            'apk_id': [sig1...sign]
            ...
        }
    '''
    signatures = {}
    flows = current_app.db.flows.find({},
                                      {'sink': 1,
                                       'apk_id': 1,
                                       '_id': 0,
                                       })

    for flow in flows:
        apk_id = flow['apk_id']
        sink = flow['sink']

        sig_list = signatures.get(apk_id)
        if sig_list is None:
            sig_list = []
            signatures[apk_id] = sig_list

        sig_list.append(sink)
    return signatures

def get_fuzzable_signatures():
    '''
    Extract a list of fuzzable signature from the database per apk id.
    A fuzzable signature is a jni method found in a flow path.
    
    Returns:
        A dictionary of the form:
        {
            'apk_id': [sig1...sign]}
            ...
        }
    '''
    signatures = {}
    native_paths = current_app.db.path_method.find({"is_native_node": True})
   
    for nativive_node in native_paths:
        
        flow_id = nativive_node['flow_id']
        
        flow = current_app.db.flows.find_one({'_id': ObjectId(flow_id)}, {'apk_id': 1, 'sink': 1, '_id': 0})
        
        apk_id = flow.get('apk_id')
        
        sink = flow.get('sink')
        print(sink)
        
        sig_list = signatures.get(apk_id)
        if sig_list is None:
            sig_list = []
            signatures[apk_id] = sig_list
        if sink != nativive_node.get('called_signature'):
            sig_list.append(nativive_node.get('called_signature'))

   
    
    return signatures

def get_isas(apk_id):
    apk = current_app.db.apks.find_one({'_id': apk_id})
    if apk is None:
        return {'error': True}
    
    libraries = apk.get('libraries')
    isas = set()
    
    for lib_id in libraries:
        lib = current_app.db.libraries.find_one({'_id': lib_id})
        isas.add(lib['isa'])
    
    return list(isas)
    
def get_test_signatures():
    signatures = next(current_app.db.test.find({}))['signatures']
    return signatures

