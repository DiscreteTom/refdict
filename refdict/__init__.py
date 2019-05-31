class refdict:
	def __init__(self, data, refPrefix = '@', separator = '.'):
		self.__prefix = refPrefix
		self.__data = data
		self.__separator = separator
		self.__partial = False
		self.__result = None

	def load(self, data):
		self.__data = data
		self.__partial = False
		return self

	def __getitem__(self, keys):
		# get raw result
		result = self.__data
		if self.__partial:
			result = self.__result
		try:
			return refdict.findItem(self.__data, keys, refPrefix = self.__prefix, seperator = self.__separator, root = result)
		except TypeError:
			raise TypeError('refdict.__getitem__ can just accept str, int or slice as keys')

	@classmethod
	def findItem(cls, data, keys, **kwargs):
		'''
		kwargs:
		- `refPrefix = '@'`
		- `separator = '.'`
		- `root = data`
		
		return `root[keys]` using `data` as reference dataset
		
		`keys` can be a str of linked keys, or an int, or a slice object
		'''

		prefix = '@' if 'refPrefix' not in kwargs else kwargs['refPrefix']
		sep = '.' if 'separator' not in kwargs else kwargs['separator']
		root = data if 'root' not in kwargs else kwargs['root']
		result = root

		# if keys is an int or a slice (result is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			return result[keys]
		# else, keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.findItem can just accept str, int or slice as keys')

		# now keys must be a str, process it to a list
		keys = keys.split(sep)
		# calculate result[keys[0]]
		while len(keys):
			# every time pop the first key
			key = keys.pop(0)
			# calculate the raw result, which means result may be a ref str
			if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
				# use `eval` to support slice operation
				result = eval('result[' + key + ']')
			else:
				# see result as a dict, use key as a string
				result = result[key]
			# if result is a reference string, redirect it to its target
			while isinstance(result, str) and result.startswith(prefix):
				# add target infront of keys
				keys = result[len(prefix):].split(sep) + keys
				# result is the data
				result = data
		return result

	def __setitem__(self, keys, value):
		result = self.__data
		if self.__partial:
			result = self.__result
		# if keys is a slice or an int (maybe result is str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			result[keys] = value
			return
		# else, keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__setitem__ can just accept int, str or slice as keys')

		keys = keys.split(self.__separator)
		# idea: self.__result[keys[:-1]][keys[-1]] = value
		# first, let result = self.__result[keys[:-1]]
		if len(keys) != 1:
			result = refdict.findItem(self.__data, self.__separator.join(keys[:-1]), refPrefix = self.__prefix, separator = self.__separator, root = result)
		# then, result = result[keys[-1]]
		# ignore whether the final result is a reference string
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `exec` to support slice assignment
			result = exec('result[' + keys[-1] + '] = value')
		else:
			# see result as a dict
			result[keys[-1]] = value
	
	def text(self, keys):
		'''
		get value, if the value of the last key is a ref string, return the ref string
		'''
		result = self.__data
		if self.__partial:
			result = self.__result
		# if keys is a slice or an int (maybe result is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			return result[keys]
		elif not isinstance(keys, str):
			raise TypeError('refdict.text can just accept int, str or slice as keys')
		keys = keys.split(self.__separator)
		# idea: return result[keys[:-1]][key[-1]]
		# first, let result = result[keys[:-1]]
		if len(keys) != 1:
			result = refdict.findItem(self.__data, self.__separator.join(keys[:-1]), refPrefix = self.__prefix, separator = self.__separator, root = result)
		# then, result = result[keys[-1]]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			result = eval('result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			result = result[keys[-1]]
		return result

	def __getattr__(self, funcName):
		if self._refdict__partial:
			return eval('self._refdict__result.' + funcName)
		return eval('self._refdict__data.' + funcName)

	def __str__(self):
		if self._refdict__partial:
			return str(self._refdict__result)
		return str(self.__data)

	def __contains__(self, keys):
		resultContainer = self._refdict__data
		if self._refdict__partial:
			resultContainer = self._refdict__result
		if not isinstance(keys, str):
			return keys in resultContainer
		keys = keys.split(self.__separator)
		if len(keys) == 1:
			return keys[0] in resultContainer
		try:
			resultContainer = self[self._refdict__separator.join(keys[:-1])]
		except:
			return False
		return keys[-1] in resultContainer


	def __delitem__(self, keys):
		# if keys is an int or a slice (maybe self.__data is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			del self.__data[keys]
		# or keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__delitem__ can just accept int, str or slice as keys')
		keys = keys.split(self.__separator)
		# idea: del self.__data[keys[:-1]][keys[-1]], based on self.__getitem__
		# first, let result = self.__data[keys[:-1]]
		result = self.__data
		if len(keys) > 1:
			result = self[self.__separator.join(keys[:-1])]
		# then, result = result[keys[-1]]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			exec('del result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			del result[keys[-1]]

	def __iter__(self):
		return iter(self.__data)

	def __repr__(self):
		return repr(self.__data)
