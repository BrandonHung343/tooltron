import sqlite3
from sqlite3 import Error

# columns is a dictionary with the key being the name, value being the type
def new_table(db_name, table_name, columns):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    col_string = ''
    for key in columns:
    	col_string = col_string + str(key) + ' ' + str(columns[key] + ', ')
    col_string = col_string.strip(', ')
    c.execute('CREATE TABLE {tn} ({cs})'.format(tn=table_name, cs=col_string))
    print('DB created')
    conn.commit()
    conn.close()


# each field is a string
def add_col(db_name, table_name, col_name, col_type, def_value=None):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	if def_value is not None:
	    c.execute('ALTER TABLE {tn} ADD COLUMN {cn} {ct} DEFAULT {df}'.format(tn=table_name, cn=col_name, ct=col_type, df=def_value))
	else:
	    c.execute('ALTER TABLE {tn} ADD COLUMN {cn} {ct}'.format(tn=table_name, cn=col_name, ct=col_type))
	conn.commit()
	conn.close()

# columns and values are tuples of data in the right places
# columns is going to be all strings, while values is 
# the value of the correct data type in the matching space
# ex. insert_entry('testdb', 'persons', ('name', 'id', 'machine', 'mill'), ('Marianne', '22211902', 1, 1))
def insert_entry(db_name, table_name, columns, values):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	col_string = ''
	val_string = ''
	for col in columns:
		col_string = col_string + col + ', '
	col_string = col_string.strip(', ')
	for val in values:
		val_string = val_string + '?, '
	val_string = val_string.strip(', ')
	sql_cmd = 'INSERT INTO {tn} ({cs}) VALUES({vs})'.format(tn=table_name, cs=col_string, vs=val_string)
	c.execute(sql_cmd, values)
	lastid = c.lastrowid
	conn.commit()
	conn.close()
	return lastid
 
def update_entry(db_name, table_name, entry_name, entry_value, columns, values):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	col_string = ''
	val_string = ''
	for col in columns:
		col_string = col_string + col + ' = ?, '
	col_string = col_string.strip(', ')
	# combine entry_value with values in tuple to make executing easier
	cmd_tuple = list(values)
	cmd_tuple.append(entry_value)
	cmd_tuple = tuple(cmd_tuple)
	sql_cmd = 'UPDATE {tn} SET {cs} WHERE {en} = ?'.format(tn=table_name, cs=col_string, en=entry_name)
	c.execute(sql_cmd, cmd_tuple)
	conn.commit()
	conn.close()

# column is a string, value is the serach condition (value and datatype) of the column 
# value is a tuple (item,)
def remove_entry(db_name, table_name, column, value):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	# combine entry_value with values in tuple to make executing easier
	sql_cmd = 'DELETE FROM {tn} WHERE {cs} = ?'.format(tn=table_name, cs=column)
	c.execute(sql_cmd, value)
	conn.commit()
	conn.close()

# query information about a single thing. 
# supply a tuple to columns to limit the number of solumns returned, else returns all information about them
def query_db(db_name, table_name, cond, values, columns=None):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	col_string = ''
	if columns is not None:
		for col in columns:
			col_string = col_string + col + ', '
		col_string = col_string.strip(', ')
		sql_cmd = 'SELECT {cs} FROM {tn} WHERE {cl} = ?'.format(cs=col_string, tn=table_name, cl=cond)
	else:
		sql_cmd = 'SELECT * FROM {tn} WHERE {cl} = ?'.format(tn=table_name, cl=cond)
	c.execute(sql_cmd, values)
	queried = c.fetchall()
	conn.close()
	return queried

def get_col_names(db_name, table_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute('SELECT * FROM {tn}'.format(tn=table_name))
	names = [thing[0] for thing in c.description]
	print(names)

# print everyone in the table
def get_table_info(db_name, table_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute('SELECT * FROM {tn}'.format(tn=table_name))
	info = c.fetchall()
	for row in info:
		print(row)
	conn.close()
