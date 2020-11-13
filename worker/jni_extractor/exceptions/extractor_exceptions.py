class KeyNotFound(Exception):
	def __init__(self, message):
		self.message = message

class NoMethodsGiven(Exception):
	def __init__(self, message):
		self.message = message


class FileNotFound(Exception):

	def __init__(self, message):
		self.message = message

class StrategyNotSupported(Exception):
	def __init__(self, message):
		self.message = message

class NoFunctionsProvided(Exception):
	def __init__(self, message):
		self.message = message

class NoneParameterError(Exception):
	def __init__(self, message):
		self.message = message

class AndroSignatureError(Exception):
	def __init__(self, message):
		self.message = message

class SootSignatureError(Exception):
	def __init__(self, message):
		self.message = message

class ToolNotFoundError(Exception):
	def __init__(self, message):
		self.message = message


class InvalidFileError(Exception):
	def __init__(self, message):
		self.message = message

# Messages
ABSTRAC_METHOD = 'This method is abstract like and needs to be implemented by subclasses to be used'
NONE_PARAM = 'parameter \'{}\' cannot be None'
ANDRO_SIG = 'The signature \'{}\' extracted does not respect the expected Androguard pattern'
SOOT_SIG = 'The signature \'{}\' extracted does not respect the expected Soot pattern'
TOOL_NOT_FOUND = 'Could not find \'{}\' on this computer, please install it and try again'
FILE_NOT_FOUND = 'Could not find \'{}\' on this machine, maybe wrong path?'
INVALID_FILE = 'The file provided is not of the correct type. File must be .\'{}\' like.'