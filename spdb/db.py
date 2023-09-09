from spdb import db_utils
from spdb.loggers import BaseLogger
from spdb.loggers import LogText
import sqlite3
import json
import sys


class Database:
	def __init__(self, path: str, logger: BaseLogger=BaseLogger(), database_type='sqlite3', encoding='UTF-8'):
		if database_type not in ['sqlite3']:
			raise NotImplementedError(f'Database {database_type} is not supported. Available types: sqlite3')
		self.path = path
		self.logger = logger
		self.execute(f'PRAGMA encoding="{encoding}"')


	def create_tables(self, tables_names: list):
		for table_name in tables_names:
			if type(table_name) == tuple:
				columns = ''
				for column in table_name[1]:
					if column[0] != 'data':
						columns += f'{column[0]} {column[1]},'
				self.logger.log(LogText('DEBUG', f'spdb.Database.create_tables >>> {table_name[0]}:'+columns))
				self.execute(f'create table if not exists {table_name[0]}({columns}data text)')
			else:
				self.create_tables([(table_name, [('id', 'text')])])


	def execute(self, code: str) -> str:
		self.logger.log(LogText('DEBUG', 'spdb.Database.execute >>> code:'+code))
		database = sqlite3.connect(self.path, isolation_level=None)
		cursor = database.cursor()
		cursor.execute(code)
		result = cursor.fetchall()
		database.commit()
		database.close()
		self.logger.log(LogText('DEBUG', 'spdb.Database.execute >>> result:'+str(result)))
		return result


	def get_columns(self, table_name):
		for column in self.execute(f'pragma table_info({table_name})'):
			if column[1] != 'data':
				yield column[1]


	@staticmethod
	def merge_columns_and_data_ids(columns: list[str], data_ids: list[str]):
		result = []
		if type(data_ids) != list:
			data_ids = [data_ids]
		if len(columns) != len(data_ids):
			columns_hint = '(0)' if len(columns) == 0 else f'(<{len(columns)}> {", ".join(columns)})'
			data_ids_hint = '(0)' if len(columns) == 0 else f'(<{len(data_ids)}> {", ".join(data_ids)})'
			raise KeyError(f'The number of columns{columns_hint} does not match the number of IDs{data_ids_hint}')
		for i, column in enumerate(columns):
			result.append(f'{column}=\'{data_ids[i]}\'')
		return ' and '.join(result)



	@staticmethod
	def object_to_dict(object) -> dict:
		if object is None:
			return {}
		return object.__dict__


	@staticmethod
	def object_to_json(object) -> dict:
		return Database.dict_to_json(Database.object_to_dict(object))


	@staticmethod
	def dict_to_json(Dict) -> dict:
		D = {}
		for key in list(Dict):
			if type(Dict[key]) in [bool, int, float, str]:
				D[key] = Dict[key]
			elif type(Dict[key]) == dict:
				D[key] = Database.dict_to_json(Dict[key])
			elif type(Dict[key]) == list:
				D[key] = []
				for e in Dict[key]:
					D[key].append(Database.dict_to_json({'o': e})['o'])
			else:
				D[key] = Database.object_to_json(Dict[key])
		return D


	@staticmethod
	def dict_to_object(Class, Dict: dict):
		try:
			return Class(**Dict)
		except TypeError:
			return None


	@staticmethod
	def json_to_object(Class, JSON: dict):
		try:
			return Class.fromJSON(JSON)
		except NameError:
			return Database.dict_to_object(Class, JSON)
		except KeyError:
			return Database.dict_to_object(Class, JSON)


	def read_json(self, name: str, data_id: str | list[str]) -> dict:
		if type(data_id) != list:
			data_id = [data_id]

		for i in range(len(data_id)):
			data_id[i] = str(data_id[i])

		objects = self.execute(f'select data from {name} where {Database.merge_columns_and_data_ids(list(self.get_columns(name)),data_id)}')
		if len(objects) == 0:
			return {}
		return json.loads(objects[0][0].replace('SNGL_QT', '\'').replace('DBL_QT', '"'))


	def read_object(self, Class, name: str, object_id: str | list[str]):
		return Database.json_to_object(Class, self.read_json(name, object_id))


	def write_json(self, name: str, data_id: str | list[str], JSON: dict):
		if type(data_id) != list:
			data_id = [data_id]

		for i in range(len(data_id)):
			data_id[i] = str(data_id[i])

		data = json.dumps(JSON)
		columns = list(self.get_columns(name))
		objects = self.execute(f'select data from {name} where {Database.merge_columns_and_data_ids(columns,data_id)}')
		if len(objects) == 0:
			self.execute(f'insert into {name}({",".join(columns)}, data) values({",".join(list(db_utils.add_quotes_to_list(data_id)))}, \'{data}\')')
		else:
			self.execute(f'update {name} set data = \'{data}\' where {Database.merge_columns_and_data_ids(columns,data_id)}')


	def write_object(self, name: str, object_id: str | list[str], object: any):
		self.write_json(name, object_id, Database.object_to_json(object))


	def delete_dict(self, name: str, dict_id: str | list[str]):
		if type(dict_id) != list:
			dict_id = [dict_id]

		for i in range(len(dict_id)):
			dict_id[i] = str(dict_id[i])
		self.execute(f'delete from {name} where {Database.merge_columns_and_data_ids(list(self.get_columns(name)),dict_id)}')


	def delete_json(self, name: str, json_id: str | list[str]):
		self.delete_dict(name, json_id)


	def delete_object(self, name: str, object_id: str | list[str]):
		self.delete_dict(name, object_id)
