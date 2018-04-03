import sqlite3
import os
from flask import Flask, request, render_template, session, url_for, redirect, g



from appdata import *

########################################################

app = Flask(__name__)
app.secret_key = os.environ['T_KEY']

# things to do before and after a request

########################################################

@app.before_request
def before_request():

	# connect to database
	g.db = sqlite3.connect("mrdata.db", check_same_thread=False)
	g.db.row_factory = sqlite3.Row
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
		return register_user(data)
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
		return login_user(data)
	
	return "Invalid request"


# TO DO: REMOVE GET
@app.route('/logout/', methods=['POST', 'GET'])
def logout():
	session.pop('usr', None)
	return redirect(url_for('home'))


@app.route('/<username>/')
def profile(username):

	user = get_user_by_name(username)

	if (user and len(user) > 0):
		return get_profile(user[0])
		
	return "Nothing here"


#### run app
if __name__ == '__main__':
	app.run(debug=True)
