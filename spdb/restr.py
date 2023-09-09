import re


class REstr:...

class REstr:
	def __init__(self, string: str|REstr=''):
		if type(string) == REstr:
			self.string: str = string.string
		elif type(string) == str:
			self.string: str = string
		else:
			self.convertFrom(string)


	def replace(self, find: str, to: str):
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		self.string = re.sub(find.string, to.string, self.string)
		return self


	def toReplaced(self, find: str, to: str):
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		return REstr.fromStr(re.sub(find.string, to.string, self.string))


	def clean(self, find: str):
		find: REstr = REstr.strOrREstr(find)
		self.replace(find, '')
		return self


	def toCleaned(self, find: str):
		find: REstr = REstr.strOrREstr(find)
		return self.toReplaced(find, '')


	def isReplacing(self, find: str, to: str='') -> bool:
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		return self.string != self.toReplaced(find, to)


	def isMatches(self, find: str) -> bool:
		find: REstr = REstr.strOrREstr(find)
		return self.toReplaced(find, '').isEmpty()


	def matches(self, find: str) -> int:
		find: REstr = REstr.strOrREstr(find)
		return len(self.match(find))


	def match(self, find: str) -> re.Match:
		find: REstr = REstr.strOrREstr(find)
		return re.match(find.string, self.string)


	def setFromStr(self, string: str) -> None:
		self.string = string


	def len(self) -> int:
		return len(self.string)


	def isEmpty(self) -> bool:
		return self.string == ''


	def at(self, index):
		if type(index) == int:
			return REstr.fromStr(self.string[index])
		elif type(index) == tuple:
			if len(index) == 1:
				return REstr.fromStr(self.string[index[0]])
			elif len(index) == 2:
				return REstr.fromStr(self.string[index[0]:index[1]])
			elif len(index) == 3:
				return REstr.fromStr(self.string[index[0]:index[1]:index[2]])
		return REstr()


	def join(self, lst: list):
		return REstr.fromStr(self.string.join(lst))


	def join_to_begins(self, lst: list):
		for l in lst:
			yield self.string + REstr.strOrREstr(l).string


	def join_to_ends(self, lst: list):
		for l in lst:
			yield REstr.strOrREstr(l).string + self.string


	def join_boths(self, lst: list):
		for l in lst:
			yield self.string + self.REstr.strOrREstr(l).string + self.string


	def split(self, D=[' ','\n','\r','\t']):
		return re.split('|'.join(map(re.escape, D)))


	def splits(string: str, delimeters: list[str]=[' ', '\n'], quotes: list[str]=[]):
		result = [REstr()]
		current_quote = ''
		for char in str(string):
			if char in quotes:
				if current_quote == '':
					current_quote = char
					continue
				elif current_quote == char:
					current_quote = ''
					continue
			if current_quote == '':
				if char in delimeters:
					result.append(REstr())
				else:
					result[-1].string += char
			else:
				result[-1].string += char
		return result


	def convertFrom(self, var):
		return REstr.fromStr(str(var))


	def convertTo(self, Class):
		return Class(self.string)


	def load(self, path: str):
		self.string = REstr.read(path).toStr()
		return self


	def save(self, path: str) -> bool:
		return REstr.write(path, self)


	def __str__(self):
		return self.string


	def __int__(self):
		return int(self.string)


	def __float(self):
		return float(self.string)

	def __bool__(self):
		return bool(self.string)

	def __add__(self, other):
		return self.string + str(other)

	def __iadd__(self, other):
		self.string += str(other)
		return self.string

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return self.string * int(other)
		return self.string * len(str(other))

	def __imul__(self, other):
		if type(other) == int or type(other) == float:
			self.string *= int(other)
		else:
			self.string *= len(str(other))
		return self.string


	def __set__(self, instance, value):
		self.string = str(value)


	def __len__(self):
		return len(self.string)


	@staticmethod
	def strOrREstr(string):
		if type(string) == str:
			return REstr.fromStr(string)
		elif type(string) == REstr:
			return string
		return REstr()


	@staticmethod
	def read(path: str):
		path = strOrREstr(path)
		try:
			file = open(path, 'r')
			string = file.read()
			file.close()
		except Exception:
			return False
		return REstr.fromStr(string)


	@staticmethod
	def write(path: str, string: str):
		path = REstr.strOrREstr(path)
		string = REstr.strOrREstr(string)
		try:
			file = open(path, 'w')
			file.write(string.string)
			file.close()
		except Exception:
			return False
		return True
