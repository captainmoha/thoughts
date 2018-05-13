import sqlite3
import os
from flask import Flask, request, render_template, session, url_for, redirect, g
from flask_bootstrap import Bootstrap


from appdata import *

########################################################

app = Flask(__name__)
Bootstrap(app)
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
		g.username = session['username']

@app.teardown_request
def teardown_request(exception):
	
	# close database
	g.db.close()


########################################################


@app.route('/')
def home():
	if g.usr:
		# get in, later will show home page
		# return "Logged in as {}".format(session['usr'])
		return render_template('home.html', loggedin=True, username=g.username, title="Welcome to Thoughts :)")

	return render_template('login.html', title="Login to Thoughts")


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

		loggedin = False

		if g.usr:
			loggedin = True

		thoughts = get_thoughts_by_id(user[0])
		return render_template("profile.html", thoughts=thoughts, loggedin=loggedin, username=username, img_url="https://avatars2.githubusercontent.com/u/6375633?s=88&v=4")

		return get_profile(user[0])
		
	return "Nothing here"


@app.route('/upload/',methods=['POST'])
def upload():
	pic_data = request.json
	user_name = pic_data.get("username"," ")

	if (user_name != ""):
		row = get_user_by_name(user_name)
		val = pic_data.get("type","")
		link = pic_data.get("link")
		print(link)
		print(len(link))

		if(val == "p"):
			g.db_cursor.execute("UPDATE profiles SET img = ? WHERE user_id = ?", (str(link),row[0]))
			g.db.commit()

		elif (val == "t"):
			# g.db_cursor.execute("INSERT INTO thoughts(img) VALUES(?)", str(link))
			pass
		else:
			return "Invalid req"
	else:
		return "invalid req!"

@app.route('/thought/', methods=['POST'])
def thought():
	data = request.form
	add_thought(data['txt'])
	return "Success!"



#### run app
if __name__ == '__main__':
	app.run(debug=True)
