import sqlite3
from flask import Flask, request, render_template

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

# connect to database

db = sqlite3.connect("data.db", check_same_thread=False)
curr = db.cursor()


# curr.execute('''
# 	CREATE TABLE users
# 	(id integer PRIMARY KEY, username text UNIQUE NOT NULL,
#    	email text UNIQUE NOT NULL, password text NOT NULL,
#    	name text NOT NULL,

# 	reg_date DATETIME DEFAULT CURRENT_TIMESTAMP
# 	)
# 	''')


# curr.execute('''
# 	CREATE TABLE profiles
# 	(id integer AUTO INCREMENT, username text UNIQUE NOT NULL, name text NOT NULL, birthday text,
# 	phone_number text, about text,

# 	FOREIGN KEY(username) REFERENCES users(username)
# 	)
# 	''')

# db.commit()


########################################################

app = Flask(__name__)


@app.route('/')
def home():
	return "I AM HOME"


@app.route('/register/', methods=['GET'])
def register_serve():
	# curr.execute("INSERT INTO users(username, email, password, reg_date) VALUES('captainmoha', 'farouk@thoughts.com', '1234', '15th NOV 2017')")
	return render_template('register.html')


@app.route('/register/', methods=['POST'])
def register():

	'''
		Handle post request from front-end Login a user
	'''
	data = request.form

	if (data != None):
		print("----: " + str(data))
		
		reg_data = validate_register(data)
		if (reg_data != None):
			username = data.get("username", "")
			email = data.get("email", "")
			if (username != "" and email != ""):

				curr.execute("SELECT username, email, password FROM users WHERE username = ? OR email = ? ", (username, email))
				row = curr.fetchone()
				print("reg------ " + str(row))
				if (row == None):
					curr.execute("INSERT INTO users(username, password, email, name) VALUES(?, ?, ?, ?)", reg_data)
					db.commit()
					return "Welcome to thoughts, you're signed up :D"
	
				else:
					return "already registered" 
		else:
			return "incomplete data"
	else:
		return "Invalid request"



@app.route('/login/', methods=['GET'])
def login_serve():

	return render_template("login.html")




@app.route('/login/', methods=['POST'])
def login():

	'''
		Handle post request from front-end Register a user
	'''
	data = request.form

	username = ""

	if (data != None):
		username = data.get("username")
		

		if (username != None and username != ''):

			# check if user exists in the database
			curr.execute("SELECT username, email, password FROM users WHERE username = ?", (username,))
			row = curr.fetchone()


			if (row != None and len(row) > 0):
				# user exists, validate password
				print(str(type(row)) + " - " + str(row))
				
				# validate hashes
				
				check_pass = check_password_hash(row[2], data.get("password", ""))

				if (check_pass):
					# correct password was entered
					return "Logged in!"

				else:
					return "wrong password"
			else:
				return "user doesn't exist, please register"

		else:
			return "incomplete data"
	
	return "Invalid request"


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




# db.commit()
# db.close()