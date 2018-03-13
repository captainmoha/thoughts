import sqlite3
from flask import Flask, request


########################################################
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
	return "Welcome to thoughts, please register."


@app.route('/register/', methods=['POST'])
def register():
	data = request.json

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



@app.route('/login/', methods=['GET'])
def login_serve():
	return "Please login"




@app.route('/login/', methods=['POST'])
def login():
	data = request.get_json()

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
				
				if (row[2] == data.get("password")):
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
	keys = ['username', 'password', 'email', 'name']
	vals = []

	print("validate----- " +  str(type(reg_data)))
	for key, val in reg_data.items():
		if (key in keys and val != ""):
			continue
		else:
			return None


	for key in keys:
		vals.append(reg_data[key])


	return tuple(vals)


def encrupt_pass(password):
	return password

#### run app
if __name__ == '__main__':
	app.run(debug=True)




# db.commit()
# db.close()