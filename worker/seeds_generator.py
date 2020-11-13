"""
seeds_generator.py
~~~~~~~~~~~~~~~~~~~

This module is used as an utility to generate AFL seeds
depending on the signature received.

Since many parameters are expected, we need a separator character to be able to
split AFL input into different parameters: by default we use `\x07`.
"""

from jni_extractor.method_abstraction import SootMethod
import random
import itertools
import string


def _generate_integer_parameter_seed():
    # (positive, negative, zero)
    positive = random.randint(1, 2048)
    negative = -1 * random.randint(1, 2048)
    return [str(positive), str(negative), str(0)]

def _randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def generate_integer_seed_for_one():
    '''Generates seeds for fuzzing an integer parameter'''
    return _generate_integer_parameter_seed()

def generate_string_seed_for_one():
    return [_randomString(1), _randomString(random.randint(256, 1024)), _randomString(1024)]
    

def generate_string_seeds(signature):
    sm = SootMethod(signature)
    param_types = sm.get_parameter_types()

    seed = [_randomString(random.randint(256, 1024)) for _ in param_types]
    return ["\x07".join(seed)]

def generate_integer_seeds(signature):
    """Generates a set of seeds. Each seed
    is supposed to be included as a file for AFL.

    **NOTE** that this method assumes that the signature
    only have int types. If a non int type is found,
    None is returned.

    Param:
        (str) signature: fuzzable method signature
    Return:
        (list) of seeds to include in the analysis
    """
    primitives = {'int', 'float', 'long', 'double'}
    sm = SootMethod(signature)
    param_types = sm.get_parameter_types()

    #for param_type in param_types:
        #if param_type not in primitives:
        #    return None

    # seeds = itertools.product(_generate_integer_parameter_seed(),
    #                          repeat=len(param_types))
    seed = [str(random.randint(-2048, 2048)) for _ in param_types]

    return ["\x07".join(seed)]
    #return list(map(lambda x: "\x07".join(x), seeds))

def generate_seeds(signature):
    sm = SootMethod(signature)
    param_types = set(sm.get_parameter_types())

    primitives = {'int', 'float', 'long', 'double'}
    complex_type = {'java.lang.String'}
    
    if param_types.issubset(primitives):
        return generate_integer_seeds(signature) + generate_integer_seed_for_one()
    elif param_types.issubset(complex_type):
        return generate_string_seeds(signature) + generate_string_seed_for_one()
    else:
        return None
    # TODO(clod) keep implementing
    