# Client implementations for accessing the database
#
import sqlite3
from sqlite3 import Error

def db_new(name, *args, **kwargs):
	if kwargs is not None:
		counter = 0
		conn = sqlite3.connect(name)
		c = conn.cursor()
		for key, value in kwargs.iteritems():
			counter += 1
			try:
				c.execute("CREATE TABLE {tn} ({nf} {ft})").format(tn=args[counter], nf=key, ft=value)
			except Error as e:
				print(e)
		print("DB created")
		conn.commit()
		conn.close()
	else:
		print("fields and types not properly created")

def check_clearances(id):
	c.execute("SELECT ({cn}) FROM {tn} WHERE {idf}={id}".format(cn=column_name, tn=table_name, idf=id_column, id=id))
	all_rows = c.fetchone()
	print(all_rows)
	if (all_rows is not None and all_rows[0] != 0):
		return True
	return False

# def main():
# 	c.execute("UPDATE {tn} SET {cn}=(0) WHERE {idf}=(48)".format(tn=table_name, cn=column_name, idf=id_column))
# 	c.execute("UPDATE {tn} SET {nc}='Timbuktu' WHERE {idf}=(42)".format(tn=table_name, nc=name_col, idf=id_column))
# 	c.execute("SELECT * FROM {tn} WHERE {idf}='Jerry'".format(tn=table_name, idf=name_col))

# 	c.execute("UPDATE {tn} SET {cn}=(1) WHERE {idf}=(48)".format(tn=table_name, cn=column_name, idf=id_column))
# 	print("Tim: ", check_clearances(42))
# 	print('Jerry: ', check_clearances(48))
# 	conn.commit()
# 	conn.close()

	

if __name__ == '__main__':
	main()