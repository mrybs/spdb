
# SPDB - Sassy Python DB

LICENSE: The MIT License


## Requirements

- Python 3.7 or higher
- pyotp
- qrcode
- setuptools


## Usage 

	import spdb

### Database

---
	spdb.Database.__init__(path: str, logger: BaseLogger=BaseLogger(), database_type='sqlite3', encoding='UTF-8')  # Create Database object
	spdb.Database.create_tables(tables_names: list[str]) -> None  # Create tables if not exists
	spdb.Database.execute(code: str) -> str  # Execute database query
	spdb.Database.get_columns(table_name: str)  -> list[str]  # Get columns from table
	spdb.Database.read_json(name: str, data_id: str | list[str]) -> dict  # Read data by ID as dict
	spdb.Database.read_object(Class: class, name: str, data_id: str | list[str]) -> Class  # Read data by ID as object
	spdb.Database.write_json(name: str, json_id: str | list[str], data: dict) -> None  # Write dict by ID
	spdb.Database.write_object(name: str, object_id: str | list[str], object: Class) -> None  # Write object by ID
	spdb.Database.delete_json(name: str, json_id: str | list[str]: str) -> None  # Delete JSON by ID
	spdb.Database.delete_object(name: str, object_id: str | list[str]: str) -> None  # Delete object by ID

	Static:
		spdb.Database.object_to_dict(object: Class) -> dict  # Convert object into dict
		spdb.Database.object_to_json(object: Class) -> dict  # Convert object into JSON-compatible dict
		spdb.Database.dict_to_object(Class: class, Dict: dict) -> Class  # Convert dict into object
		spdb.Database.dict_to_json(Dict: dict) -> dict  # Convert dict into JSON-compatible dict
		spdb.Database.json_to_object(Class: class, JSON: dict) -> Class  # Convert JSON into object

### TOTP - HOTP

---
	spdb.OTP.__init__(token: str=None, app_name: str=None)  # Create OTP object
	spdb.OTP.now() -> str  # Get TOTP code
	spdb.OTP.at(index: int) -> str  # Get HOTP code
	spdb.OTP.time_verify(code: str) -> bool  # Verify TOTP code
	spdb.OTP.counter_verify(index: int, code: str) -> bool  # Verify HOTP code
	spdb.OTP.TQR(name: str) ->  # Get TOTP QR-code for Google Authentificator
	spdb.OTP.HQR(name: str) ->  # Get HOTP QR-code for Google Authentificator

	Static:
		stdb.OTP.generate_token() -> str  # Generate random token

### Token Generator

---
	spdb.TokenGenerator.__init__(code: str)  # Create TokenGenerator object
	spdb.TokenGenerator.gen(type: str, ID: str, key: str) -> str  # Generate token

	Static:
		spdb.TokenGenerator.parse_token(token: str) -> dict  # Parse token


### REstr

---

	spdb.REstr.__init__(string: str='')  # Create REstr object
	spdb.REstr.replace(find: str/REstr, to: str/REstr) -> REstr  # Replace substring
	spdb.REstr.toReplaced(find: str/REstr, to: str/REstr) -> REstr  # Get replaced REstr
	spdb.REstr.clean(find: str/REstr) -> REstr  # Removes all matches 
	spdb.REstr.toCleaned(find: str/REstr) -> REstr  # Get removed all matches REstr
	spdb.REstr.isReplacing(find: str/REstr, to: str/REstr='') -> bool  # Will be changes when replacing?
	spdb.REstr.isMatches(find: str/REstr) -> bool  # Is entire REstr equal find regular expression?
	spdb.REstr.matches(find: str/REstr) -> int  # Count of matches
	spdb.REstr.match(find: str/REstr) -> re.Match  # The same as re.match
	spdb.REstr.setFromStr(string: str) -> REstr  # Sets new REstr from str
	spdb.REstr.toStr() -> str  # Converts REstr to str
	spdb.REstr.len() -> int  # Length of REstr
	spdb.REstr.at(index: int/tuple) -> REstr  # The same as str slicer
	spdb.REstr.join(array: list[str]/list[REstr]) ->  # The same as str join()
	spdb.REstr.convertFrom(var: Class) -> REstr  # Convert from any class to REstr
	spdb.REstr.convertTo(Class: class) -> Class  # Convert from REstr to any class
	spdb.REstr.isEmpty() -> bool  # Is REstr equal empty str

	Static:
		spdb.REstr.fromStr(string: str) -> REstr  # Create REstr object from str
		spdb.REstr.strOrREstr(string: str/REstr) -> REstr  # Converts str to REstr if type(string) == str


### Logging

---
	
	spdb.log_levels  # DEBUG, INFO, WARNING, ERROR, CRITICAL  # All logging levels in ascending order

	spdb.LogText.__init__(log_type: str, text: str, time: str=None)  # Create LogText object
	str(spdb.LogText)  # Converts LogText to str

	spdb.BaseLogger.__init__(min_log_level: str='WARNING')  # Create abstract BaseLogger object
	spdb.BaseLogger.can_log(log_level: str) -> bool:  # Can log by logging level
	spdb.BaseLogger.log(text: LogText) -> None  # Log message

	# spdb.PrintLogger is extended BaseLogger. It logs into stdout
	# spdb.FileLogger is extended BaseLogger. It logs into file and stdout
	spdb.FileLogger.__init__(path: str='log.txt', min_log_level: str='WARNING', isPrint=False)  # Create FileLogger object



### Text Validator

---
	
	spdb.TextValidator.__init__(min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+')  # Create TextValidator object
	spdb.TextValidator.check(text: REstr) -> bool  # Check text for conditions


### Quotes

---

	spdb.Quotes.__init__(open_quote: REstr=REstr.fromStr('<%'), close_quote: REstr=REstr.fromStr('%>'), validator: TextValidator=TextValidator())  # Create Quotes object
	spdb.Quotes.replace(text: REstr, data: dict) -> REstr  # Replaces entries
	spdb.Quotes.clean(text: REstr) -> REstr  # Removes all entires
	spdb.Quotes.replace_all(text: REstr, data: dict) -> REstr  # The same as stdb.Quotes.replace and stdb.Quotes.clean
	spdb.Quotes.count(text: REstr) -> int  # Count of all entries
	spdb.Quotes.count_trash(text: REstr, data: dict) -> int  # Count of all not replaced entries


### Utils

---
	spdb.utils.sha256(text: str) -> str  # Get sha256 from text
	spdb.utils.b32encode(text: str) -> str  # Encode str into base32 str
	spdb.utils.random_text(length: int=None) -> str  # Get random text
	spdb.utils.random_sha256() -> str  # Get random sha256 str
	spdb.utils.random_b32 -> str  # Get random base32 str

