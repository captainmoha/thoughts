import sqlite3
import os
from flask import Flask, request, render_template, session, url_for, redirect, g

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




########################################################

app = Flask(__name__)
app.secret_key = os.environ['T_KEY']

# things to do before and after a request

########################################################

@app.before_request
def before_request():

	# connect to database
	g.db = sqlite3.connect("mrdata.db", check_same_thread=False)
	g.db_cursor = g.db.cursor()

	# handle session
	g.usr = None
	if 'usr' in session:
		g.usr = session['usr']

@app.teardown_request
def teardown_request(exception):
	
	# close database
	g.db.close()


########################################################


@app.route('/')
def home():
	if g.usr:
		# get in, later will show home page
		return "Logged in as {}".format(session['usr'])

	return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
	
	if request.method == 'GET':
		if g.usr:
			return redirect(url_for('home'))

		return render_template('register.html')

	
	# Handle post request from front-end Login a user

	data = request.form

	if (data != None):
		print("----: " + str(data))
		
		reg_data = validate_register(data)
		if (reg_data != None):
			username = data.get("username", "")
			email = data.get("email", "")
			if (username != "" and email != ""):

				g.db_cursor.execute("SELECT username, email, password FROM users WHERE username = ? OR email = ? ", (username, email))
				row = g.db_cursor.fetchone()
				print("reg------ " + str(row))
				if (row == None):
					g.db_cursor.execute("INSERT INTO users(username, password, email, name) VALUES(?, ?, ?, ?)", reg_data)
					g.db.commit()

					return redirect(url_for('login'))
	
				else:
					return "already registered" 
		else:
			return "incomplete data"
	else:
		return "Invalid request"



@app.route('/login/', methods=['GET', 'POST'])
def login():


	if request.method == 'GET':

		if g.usr:
			return redirect(url_for('home')) 

		return render_template("login.html")


	data = request.form

	username = ""

	if (data != None):
		username = data.get("username")
		

		if (username != None and username != ''):

			# check if user exists in the database
			g.db_cursor.execute("SELECT id, username, email, password FROM users WHERE username = ?", (username,))
			row = g.db_cursor.fetchone()


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
	
	return "Invalid request"


# TO DO: REMOVE GET
@app.route('/logout/', methods=['POST', 'GET'])
def logout():
	session.pop('usr', None)
	return redirect(url_for('home'))
	

def validate_register(reg_data):

	'''
		Validate registration form
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



#### run app
if __name__ == '__main__':
	app.run(debug=True)
