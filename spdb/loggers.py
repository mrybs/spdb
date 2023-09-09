from datetime import datetime

log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class LogText:
	def __init__(self, log_type: str, text: str, time: str=None):
		if time is None:
			time = str(datetime.now())
		self.type = log_type
		self.time = time
		self.text = text


	def __str__(self):
		return f'{self.type} at {self.time}: {self.text}'


class BaseLogger:
	def __init__(self, min_log_level: str='WARNING'):
		if not min_log_level in log_levels:
			min_log_level = 'WARNING'
		self.min_log_level = min_log_level


	def can_log(self, log_level: str) -> bool:
		if not log_level in log_levels:
			return False
		return log_levels.index(log_level) >= log_levels.index(self.min_log_level)


	def log(self, text: LogText):
		if self.can_log(text.type):
			...  # log


class PrintLogger(BaseLogger):
	def log(self, text: LogText):
		if self.can_log(text.type):
			print(text)


class FileLogger(BaseLogger):
	def __init__(self, path: str='log.txt', min_log_level: str='WARNING', isPrint=False):
		super().__init__(min_log_level=min_log_level)
		self.path = path
		self.print = isPrint


	def log(self, text: LogText):
		if self.can_log(text.type):
			with open(self.path, 'a') as file:
				file.write(str(text)+'\n')
			if self.print:
				print(text)
