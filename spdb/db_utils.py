def add_quotes_to_list(lst: list[str]):
		for l in lst:
			yield f'\'{l}\''
