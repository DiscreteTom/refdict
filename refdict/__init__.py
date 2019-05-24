class refdict:
	def __init__(self, data, refPrefix = '@', divider = '.'):
		self.__prefix = refPrefix
		self.__data = data
		self.__divider = divider

	def load(self, data):
		self.__data = data
		return self

	def __getitem__(self, keys: str):
		# default result is the whole dict
		result = self.__data
		keys = keys.split(self.__divider)
		while len(keys):
			# every time pop the first key
			key = keys.pop(0)
			# get the original result
			if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
				# use `eval` to support slice operation
				result = eval('result[' + key + ']')
			else:
				# see result as a dict, use key as a string
				result = result[key]
			# if result is a reference string, redirect it to its target
			while isinstance(result, str) and result.startswith(self.__prefix):
				# add target infront of keys
				# because target can have many parts divided by self.__divider
				keys = result[len(self.__prefix):].split(self.__divider) + keys
				# result is the top-level object again
				result = self.__data
		return result

	def __setitem__(self, keys: str, value):
		result = None
		keys = keys.split(self.__divider)
		# idea: self.__data[keys[:-1]][keys[-1]] = value, based on self.__getitem__
		if len(keys) == 1:
			result = self.__data
		else:
			result = self[self.__divider.join(keys[:-1])]
		# if result is a reference string, redirect it to its target
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `exec` to support slice assignment
			result = exec('result[' + keys[-1] + '] = value')
		else:
			result[keys[-1]] = value
	
	def text(self, keys: str):
		'''
		get value, if the value the last key is a ref string, return the ref string
		'''
		keys = keys.split(self.__divider)
		# idea: return self.__data[keys[:-1]][key[-1]], based on self.__getitem__
		if len(keys) == 1:
			result = self.__data
		else:
			result = self[self.__divider.join(keys[:-1])]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			result = eval('result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			result = result[keys[-1]]
		return result

