import ast
import numpy as np
import json
import sklearn.feature_selection as fs
import sys
import tqdm
import re

INF = sys.maxsize
expression = re.compile("\[d, (\d+\.\d+,)+, \d+\.\d+\]")


def generate_taint_model(signature, io_path):
    '''Extract io.txt file and generates a model
    that can be used by flowdroid to propagate the taint

    **NOTE** This method should be called only after AnalysisCompleted
    has been triggered!!!

    Param:
        AndroidEmulator emu: android emulator instance where io.txt file 
                             has been produced.
        str io_path: Path to `io.txt`. The file should be at the same location specified for
        `extract_afl_analysis_result`.  
    '''
    f = open(io_path, 'r')

    X = None  # parameters matrix
    Y = None  # return values: starting empty
    processed = set()
    for entry in tqdm.tqdm(f.readlines()):
        if "nan" in entry or "inf" in entry or "]" not in entry:
            continue
        #entry = entry.replace("inf", str(INF))
        afl_entry = ast.literal_eval(entry.strip())
        # afl_entry = list(map(str, afl_entry))

        # we do not want duplicates
        afl_tuple = tuple(afl_entry)
        skip = False
        for x in afl_tuple:
            if x > 9223372036854775807 or x < -9223372036854775808:
                # pass
                skip = True
        afl_tuple = tuple(map(str, afl_tuple))
        
        if skip:
            continue

        if afl_tuple in processed:
            continue
        else:
            # print(afl_tuple)
            processed.add(afl_tuple)

        #  afl_entry[0] is the index of the fuzzed param and afl_entry[-1] is the ret value
        x = np.array(afl_entry[1:len(afl_entry)-1])
        y = afl_entry[-1]

        if X is None and Y is None:
            # this is the first entry and iteration
            X = np.array(x)
            Y = np.array(y)

        else:

            X = np.vstack((X, x))
            Y = np.append(Y, y)
    
    print(X)
    print(Y)
    f.close()

    def sigmoid(x):
        import math
        return 1 / (1 + math.exp(-x))

    print("computing....")
    #result = fs.mutual_info_classif(X, Y)
    #print(result)
    result = fs.mutual_info_regression(X, Y)
    print(result)
    sigmoid_result = [round(sigmoid(x), 2) for x in result]
    print(result)
    class_result = fs.mutual_info_classif(X, Y)
    input_map = {}
    #for i in range(len(result)):
    #    mutual_info_at_i = result[i]
    #    input_map[i] = bool(mutual_info_at_i > 0.1)

    #with open('model.json', 'w') as out:
        #json.dump({signature: input_map}, out)

    #fs.mutual_info_regression(X, Y)
    return (result, class_result, len(processed))


def get_mutual_info(io_path):
    f = open(io_path, 'r')
    
    X = []
    Y = []
    observation = set()
    for entry in tqdm.tqdm(f.readlines()):
        try:
            afl_entry = ast.literal_eval(entry.strip())
        except:
            continue
        
        
        import sys
        skip = False
        for x in afl_entry:
            if x > sys.maxsize or x < -9223372036854775808:
                # pass
                skip = True
        
        if skip:
            continue
        
        afl_tuple = tuple(afl_entry)
        if afl_tuple in observation:
            continue
        
        observation.add(afl_tuple)
        
        afl_entry = list(map(str, afl_entry))

        params = afl_entry[1:-1]
        ret_value = afl_entry[-1]

        
        

        X.append(params)
        Y.append(ret_value)
    

    try:
        class_result = fs.mutual_info_classif(X, Y)
        regression = fs.mutual_info_regression(X,Y)
    except:
        class_result = np.array(-1)
        regression = np.array(-1)

    return (regression, class_result, len(observation))

        

def unzip(path_to_zip_file, directory_to_extract_to):
    import zipfile
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()


def extract_and_analyse():
    worksapces = '/home/clod/Downloads/'
    import os

    results = {}

    i = 0 
    for workspace in os.listdir(worksapces):
        if workspace.endswith('.zip'):
            workspace_folder = os.path.join(worksapces, "workspace{}".format(i))
            unzip(os.path.join(worksapces, workspace), workspace_folder)
            
            with open(workspace_folder+"/signatures.txt", 'r') as f:
                signature = f.read().strip()
            
            res, class_res, n = get_mutual_info(os.path.join(workspace_folder, 'io.txt'))
            
            results[signature] = {'regression': res.tolist(), 'classification': class_res.tolist(), '#entry': n}
            

            i += 1
    return results
import pprint
import json
result = extract_and_analyse()
pprint.pprint(result)

with open(sys.argv[1], 'w') as f:
    json.dump(result, f, indent=3)

#generate_taint_model("<uk.ac.rhul.clod.samplejniapp.MainActivity: double pow(double,double)>",
#                     "/home/clod/Downloads/workspace2/io.txt")
