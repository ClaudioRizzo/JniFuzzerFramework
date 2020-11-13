"""Method abstraction module"""

import re

from jni_extractor.exceptions.extractor_exceptions import (NoneParameterError,
                                                           AndroSignatureError,
                                                           ANDRO_SIG,
                                                           ABSTRAC_METHOD,
                                                           NONE_PARAM,
                                                           SootSignatureError,
                                                           SOOT_SIG)


class MethodIface:
    """Method interface to be extended"""

    def __init__(self, signature, native):
        if signature is None:
            raise NoneParameterError(NONE_PARAM.format('signature'))
        self.signature = signature
        self.native = native

    def to_jni(self):
        """Return the jni signature of the method."""
        raise NotImplementedError(ABSTRAC_METHOD)


class SootMethod(MethodIface):
    """Method representation of the soot signature"""
    # <a.b.c: type f(type1, type2)>

    def __init__(self, signature, native=True):
        super().__init__(signature, native)
        self.__resolve_signature(signature)

    def __resolve_signature(self, sig_str):
        """Resolving a signature"""
        # removing angular parentesis from signature:
        # <a.b.c: type f(type1,type2)>  --> a.b.c: type f(type1, type2)

        stripped_sig = sig_str[1:len(sig_str)-1]

        method_class_match = re.search(r'^(.*?):', stripped_sig)
        ret_type_match = re.search(r' (.*?) ', stripped_sig)

        param_types_match = re.search(r'\((.*?)\)', stripped_sig)
        name_match = re.search(r' (.*?)\(', stripped_sig)

        if (method_class_match is None or ret_type_match is None or
                param_types_match is None or name_match is None):

            raise SootSignatureError(
                SOOT_SIG.format(sig_str) +
                "\nclass: {}\nname: {}\nparams: {}".format(method_class_match,
                                                           name_match,
                                                           ret_type_match))

        self.__method_class = method_class_match.group(1)
        self.__ret_type = ret_type_match.group(1)
        self.__parameters = param_types_match.group(1).split(',')
        self.__method_name = name_match.group(1).split(' ')[-1]

    def get_parameter_types(self):
        """Return a list of strings of parameter types"""
        return self.__parameters

    def get_return_type(self):
        """Return a string of the return type"""
        return self.__ret_type

    def get_name(self):
        """Return the method name"""
        return self.__method_name

    def get_class(self):
        """Return the class of the metod"""
        return self.__method_class

    def to_jni(self):
        print("STUB")


'''
This class represets method extracted using androguards
'''


class AndroMethod(MethodIface):

    """
        @Param native: True(Default) if this method is native.
        @Param signature: the androguard signature of the method.

        The signature is considered as: (class, name, ([LparamType;]*)LretType)
        Notice that in case of primitive types, there is
        no L in the param and ret types, but just the initial.
        Examples of signatures:
        ('uk/ac/rhul/clod/hellofrida/MainActivity',
         'getField',
         '(Luk/ac/rhul/clod/hellofrida/MyWrapper;Ljava/lang/String;)
          Ljava/lang/String;')
        ('uk/ac/rhul/clod/hellofrida/MainActivity', 'pow', '(DD)D')
    """

    def __init__(self, signature, native=True):
        super().__init__(signature, native)
        self.__method_class = self.signature[0]
        self.__method_name = self.signature[1]
        self.__ret__and_param_types = self.signature[2]
        self.__parameters = None
        self.__ret_type = None
        self.__check_signature_none_or_empty()

        self.__extract_types()

    def get_parameter_types(self):
        """Return a list of strings of parameter types"""
        return self.__parameters

    def get_return_type(self):
        """Return a string of the return type"""
        return self.__ret_type

    def get_name(self):
        """Return the method name"""
        return self.__method_name

    def get_class(self):
        """Return the class of the metod"""
        return self.__method_class

    def __check_signature_none_or_empty(self):
        if self.__method_class is None or self.__method_class == '':
            raise AndroSignatureError(
                ANDRO_SIG.format(" ".join(self.signature)))

        if self.__method_name is None or self.__method_name == '':
            raise AndroSignatureError(
                ANDRO_SIG.format(" ".join(self.signature)))

        if self.__ret__and_param_types is None:
            raise AndroSignatureError(
                ANDRO_SIG.format(" ".join(self.signature)))

    def __extract_types(self):
        params_match = re.search(r'\((.*?)\)', self.__ret__and_param_types)
        ret_type_match = re.search(r'\)(.*$)', self.__ret__and_param_types)

        if params_match is None or ret_type_match is None:
            raise AndroSignatureError(
                ANDRO_SIG.format(" ".join(self.signature)))
        else:
            self.__parameters = self.__resolve_types(
                params_match.group(1), 0, '', list())

            self.__ret_type = self.__resolve_types(
                ret_type_match.group(1), 0, '', list())[0]

    def __resolve_types(self, to_resolve, index, param, types_list):
        """ Given a string representing a list of types, as they are returned
        from androguars,this method convertes them in a python list of types,
        stripping out keywords when necessar.
        For example: I[[IILjava/lang/String;[Ljava/lang/Object; becomes
        [ 'I', '[[I', 'I', 'java/lang/String', '[java/lang/Object' ]"""

        if len(to_resolve) == index:
            return types_list

        literal = to_resolve[index]

        if literal == '[':
            # We need to consume
            param += literal
            index += 1
            return self.__resolve_types(to_resolve, index, param, types_list)
        if literal == 'L':
            # We need to consume a complex type
            (index, param) = self.__consume_complex_type(to_resolve,
                                                         index+1,
                                                         param)
            types_list.append(param)
            param = ''
            return self.__resolve_types(to_resolve, index, param, types_list)

        param += literal
        types_list.append(param)
        param = ''
        index += 1
        return self.__resolve_types(to_resolve, index, param, types_list)

    def __consume_complex_type(self, current_str, start, param):
        for i in range(start, len(current_str)):
            to_consume = current_str[i]
            if to_consume == ';':
                # we are done consuming the complex type
                return (i+1, param)
            param += to_consume

        # We raise and exception because we always expect
        # a ; to compleete a complex type
        raise AndroSignatureError(
            ANDRO_SIG.format(" ".join(self.signature)))

    def to_jni(self):
        # TODO (clod): implements
        print("STUB: TODO")
