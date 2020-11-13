
class JNITypeFactory:
	instance=None
	
	def __new__(cls):
		if JNITypeFactory.instance is None:
			JNITypeFactory.instance = JNITypeFactory.__JNITypeFactory()
		return JNITypeFactory.instance

	class __JNITypeFactory:
		#def __init__(self)
		def __get_primitive(self, java_type):
			if java_type == 'boolean' or java_type == 'Z':
				return 'jboolean'
			elif java_type == 'byte' or java_type == 'B':
				return 'jbyte'
			elif java_type == 'char' or java_type == 'C':
				return 'jchar'
			elif java_type == 'short' or java_type == 'S':
                            return 'jshort'
			elif java_type == 'int' or java_type == 'I':
				return 'jint'
			elif java_type == 'long' or java_type == 'J':
				return 'jlong'
			elif java_type == 'float' or java_type == 'F':
				return 'jfloat'
			elif java_type == 'double' or java_type == 'D':
				return 'jdouble'
			elif java_type == 'void' or java_type == 'V':
				return 'void'
			else: 
				return None
		
		# TODO:: Need to implement support to jobjects and arrays
		def __get_reference(self, java_type):
			if java_type == 'java.lang.Class' or java_type == 'java/lang/Class':
				return 'jclass'
			elif java_type == 'java.lang.String' or java_type == 'java/lang/String':
				return 'jstring'
			elif java_type == 'java.lang.Throwable' or java_type == 'java/lang/Throwable':
				return 'jthrowable'
			else: 
				return None 

		def getType(self, java_type):
			jni_type = self.__get_primitive(java_type)

			if jni_type is None:
				jni_type = self.__get_reference(java_type)

			if jni_type is None:
				raise NotImplementedError('{} type not supported'.format(java_type))
			else:
				return jni_type
