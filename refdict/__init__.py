class refdict:
	'''
	`refdict(data, refPrefix='@', separator='.')`
	'''
	def __init__(self, data, refPrefix = '@', separator = '.'):
		self.__prefix = refPrefix
		self.__data = data
		self.__separator = separator
		self.__resultPath = ''

	def load(self, data):
		'''
		load `data` to `self`, return `self`
		'''
		self.__data = data
		self.__resultPath = ''
		return self

	def __getitem__(self, keys):
		# get partial result
		result = self.__data
		if len(self.__resultPath):
			result = refdict.findItem(result, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
		# get result
		return refdict.findItem(self.__data, keys, refPrefix = self.__prefix, seperator = self.__separator, root = result)

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
				# add target in front of keys
				keys = result[len(prefix):].split(sep) + keys
				# result is the data
				result = data
		return result

	def __setitem__(self, keys, value):
		result = self.__data
		if len(self.__resultPath):
			result = refdict.findItem(result, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
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
			try:
				result = refdict.findItem(self.__data, self.__separator.join(keys[:-1]), refPrefix = self.__prefix, separator = self.__separator, root = result)
			except KeyError:
				result = self[self.__separator.join(keys[:-1])] = {}
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
		if len(self.__resultPath):
			result = refdict.findItem(result, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
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
		if len(self.__resultPath):
			result = refdict.findItem(result, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
			return eval('result.' + funcName)
		return eval('self._refdict__data.' + funcName) # DO NOT change `_refdict__data` to `__data`

	def __str__(self):
		result = 'refdict(' + str(self.__data) + ')'
		if len(self.__resultPath):
			result += "('" + self.__resultPath + "')"
		return result

	def __contains__(self, keys):
		resultContainer = self.__data
		if len(self.__resultPath):
			resultContainer = refdict.findItem(resultContainer, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
		if not isinstance(keys, str):
			return keys in resultContainer
		keys = keys.split(self.__separator)
		if len(keys) == 1:
			return keys[0] in resultContainer
		try:
			resultContainer = self[self.__separator.join(keys[:-1])]
		except:
			return False
		return keys[-1] in resultContainer

	def __delitem__(self, keys):
		result = self.__data
		if len(self.__resultPath):
			result = refdict.findItem(result, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator)
		# if keys is an int or a slice (maybe result is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			del result[keys]
		# or keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__delitem__ can just accept int, str or slice as keys')
		keys = keys.split(self.__separator)
		# idea: del result[keys[:-1]][keys[-1]]
		# first, let result = result[keys[:-1]]
		if len(keys) != 1:
			result = refdict.findItem(self.__data, self.__separator.join(keys[:-1]), refPrefix = self.__prefix, separator = self.__separator, root = result)
		# then, del result[keys[-1]]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			exec('del result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			del result[keys[-1]]

	def __iter__(self):
		if len(self.__resultPath):
			return iter(refdict.findItem(self.__data, self.__resultPath, refPrefix = self.__prefix, separator=self.__separator))
		return iter(self.__data)

	def __repr__(self):
		result = 'refdict(' + repr(self.__data) + ')'
		if len(self.__resultPath):
			result += "('" + self.__resultPath + "')"
		return result

	def __call__(self, keys):
		result = refdict(self.__data, self.__prefix, self.__separator)
		result.__resultPath = self.__resultPath
		if len(result.__resultPath):
			result.__resultPath += '.'
		result.__resultPath += str(keys)
		return result

	def get(self, keys, default = None):
		'''
		similar to `dict.get()`
		'''
		if keys in self:
			return self[keys]
		else:
			return default