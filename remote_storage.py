import pyodbc

server = '192.168.137.50'
database = 'master' # or another system database
username = '<username>'
password = '<password>'
cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()