from flask import render_template, session, url_for, redirect, g
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
	'''
		Encrypt passwords
	'''
	def __init__(self, username, password):
		self.username = username
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)


def get_user_by_name(username):

	g.db_cursor.execute("SELECT id, username, email, password, reg_date FROM users WHERE username = ? ", (username,))
	row = g.db_cursor.fetchone()
	print("usr------ " + str(row))
	
	return row


def get_user_by_id(id):

	g.db_cursor.execute("SELECT id, username, email, password, reg_date FROM users WHERE id = ? ", (id,))
	row = g.db_cursor.fetchone()
	print("usr_id------ " + str(row))
	
	return row


def register_user(data):

	print("----: " + str(data))
		
	reg_data = validate_reg_data(data)

	if (reg_data != None):
		username = data.get("username", "")

		if (username != ""):

			row = get_user_by_name(username)

			if (row == None):
				g.db_cursor.execute("INSERT INTO users(username, password, email, name) VALUES(?, ?, ?, ?)", reg_data)
				g.db.commit()
				return redirect(url_for('login'))

			else:
				return "already registered" 
	else:
		return "incomplete data"


def login_user(data):


	username = data.get("username")
		
	if (username != None and username != ''):
		# check if user exists in the database

		row = get_user_by_name(username)

		if (row != None and len(row) > 0):
			# user exists, validate password
			print(str(type(row)) + " - " + str(row))
			
			# validate hashes
			
			check_pass = check_password_hash(row[3], data.get("password", ""))
			if (check_pass):
				# correct password was entered
				session['usr'] = row[0]
				return redirect(url_for('home'))

			else:
				return "wrong password"
		else:
			return "user doesn't exist, please register"
	else:
		return "incomplete data"




def validate_reg_data(reg_data):

	'''
		Validatlse registration form
	'''
	keys = ['username', 'password', 'email', 'name']
	vals = []

	print("validate----- " +  str(type(reg_data)))
	


	for key in keys:
		val = reg_data.get(key, None)

		if (val):
			vals.append(val)

	# make sure that all 4 essential fields are filled
	if (len(vals) != 4):
		return None

	#encrypt password
	secure_user = User(vals[0], vals[1])
	vals[1] = secure_user.pw_hash

	return tuple(vals)