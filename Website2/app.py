from flask import Flask, render_template, session, request, make_response, jsonify
# from flask.ext.socketio import SocketIO, emit
import time
import os
import sys
import hercubit
import urllib2,json
import sys
import pickle
# from hercubit import html_graph

# Changing the logging so that the output terminal is not overwhelmed.
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


app = Flask(__name__)
if 'production' not in sys.argv:
	app.debug=True  # Disabled before distributing
	bluetooth_enabled=True
elif "bt" in sys.argv:
	bluetooth_enabled=True
else:
	# bluetooth_enabled=False
	pass

app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
device_data_generator=[]
DEVICE_CONNECTED=False
ser=''

# Fusion Tables constants
exerciseTableId = "1OBObNVqy3kHdpdDaGaC1xH5sfmGWb-oGBNfosOMo";
goalTableId = "1R8s9_P6t9IH8DOG3rBieAh05W9_H5C2K4MdQCuRG";
scopes = 'https://www.googleapis.com/auth/fusiontables';
clientId = '755998331131-jsf1f67tj7ojvlc9bai1p6273qidsbn5.apps.googleusercontent.com';
# apiKey = 'AIzaSyD1nrNVFFr6z0_S9vOryX9kF7U-7pVZDBU'; //charles
apiKey = "AIzaSyA8juHC7LiH4pY4HM3XPIUTuFFt6y2jWqU"
# username=''
########################
# Normal web server stuff

@app.route('/')
def index():
	# global username
	#show cookie in terminal
	app.logger.debug("Cookie:\n"+str(request.cookies))

	if 'username' in request.cookies:
		username = request.cookies.get('username')
		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getAllGoals.php?username="+username
		response = urllib2.urlopen(url)
		goals = json.load(response)
		# app.logger.debug(goals)
		img_path="../static/img/"+username+".png"
	
	else: #first time users
		print "else"
		username = ""
		goals = ""
		img_path=""


	return render_template('index.html',username=username,month=time.strftime("%B"),goals=goals,img_path=img_path)



@app.route('/signup', methods=['POST'])
def signup():
	# global username
	username = request.form['username']
	# email= request.form['signup-email']
	app.logger.debug("signup completed for username: " + username)
	
	url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getUser.php?username="+username
	response = urllib2.urlopen(url)
	userInfo = json.load(response)
	
	
	#no user by this name so make a new one in 'user' table.
	new_user=False
	if userInfo ==False:
		app.logger.debug("username: "+username+" not found. Creating user")
		url="http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/addNewUser.php?username="+username
		response = urllib2.urlopen(url)
		userInfo = json.load(response)
		new_user=True
	resp = make_response(jsonify(username=username,new_user=new_user))
	# This is where we would create a new user in fusion tables
	#
	resp.set_cookie('username', username,)
	return resp

@app.route('/logout', methods=['POST'])
def logout():
	if 'username' in request.cookies:  
		resp = make_response(jsonify(success=True, type='logout'))
		resp.set_cookie('username', '')
		return resp
	else:
		resp = make_response(jsonify(success=False, type='logout'))
		return resp 
	# app.logger.debug("Cookie:\n"+str(request.cookies))
	# resp = make_response(jsonify(username="blerg"))
	# resp.delete_cookie("username","blerg",domain=".app.localhost")
	# app.logger.debug(resp)
	# return resp


########################
# connection to the db server
@app.route('/addGoal', methods=['POST'])
def addGoal():
	print 'addGoal'
	if 'username' in request.cookies: 
		username = request.cookies.get('username')

		exerciseType = request.form['exerciseType']
		exerciseCount = request.form['exerciseCount']
		exerciseWeight = request.form['exerciseWeight']

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/insertNewGoal.php?username="+username+"&exercise="+exerciseType+"&count="+exerciseCount+"&weight="+exerciseWeight
		print url
		response = urllib2.urlopen(url)
		insertStatus = json.load(response)

	resp = make_response(jsonify(username=username))
	return resp

@app.route('/deleteGoal', methods=['POST'])
def deleteGoal():
	print 'deleteGoal'
	if 'username' in request.cookies:
		
		username = request.cookies.get('username')
		# print username

		goalId = request.form['id'][5:]
		# print goalId

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/deleteGoal.php?id="+goalId
		response = urllib2.urlopen(url)
		deleteStatus = json.load(response)

	resp = make_response(jsonify(username=username))
	return resp

@app.route('/checkBadge', methods=['POST'])
def checkBadge():
	print 'checkBadge'
	if 'username' in request.cookies:
		username = request.cookies.get('username')
		# badgeNum = request.form['badgeNum']
		# print username

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getUser.php?username="+username
		response = urllib2.urlopen(url)
		userInfo = json.load(response)
		# print userInfo

	resp = make_response(jsonify(userInfo=userInfo))
	return resp

@app.route('/determineBadge', methods=['POST'])
def determineBadge():
	print 'determineBadge'
	if 'username' in request.cookies:
		username = request.cookies.get('username')
		badgeNum = request.form['badgeNum']
		# print username

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/determineBadge.php?username="+username+"&badgeNum="+badgeNum
		response = urllib2.urlopen(url)
		badgeInfo = json.load(response)
		print badgeInfo

	resp = make_response(jsonify(badgeInfo=badgeInfo))
	return resp

@app.route('/insertBadge', methods=['POST'])
def insertBadge():
	print 'insertBadge'
	if 'username' in request.cookies:
		username = request.cookies.get('username')
		badgeNum = request.form['badgeNum']

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/insertNewBadge.php?username="+username+"&badgeNum="+badgeNum
		response = urllib2.urlopen(url)
		userInfo = json.load(response)
		print userInfo

	resp = make_response(jsonify(userInfo=userInfo))
	return resp


@app.route('/getActivities', methods=['POST'])
def getActivities():
	print 'getActivities'
	if 'username' in request.cookies:
		username = request.cookies.get('username')

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getUser.php?username="+username
		response = urllib2.urlopen(url)
		userInfo = json.load(response)

	resp = make_response(jsonify(userInfo=userInfo))
	return resp

@app.route('/getFriendActivities', methods=['POST'])
def getFriendActivities():
	print 'getFriendActivities'
	# if 'username' in request.cookies:
		# username = request.cookies.get('username')
		# username = request.form['username']

	url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getUser.php"
	response = urllib2.urlopen(url)
	userInfo = json.load(response)

	resp = make_response(jsonify(userInfo=userInfo))
	return resp

@app.route('/determineActivity', methods=['POST'])
def determineActivity():
	print 'determineActivity'
	if 'username' in request.cookies:
		username = request.cookies.get('username')

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/determineActivity.php?username="+username
		response = urllib2.urlopen(url)
		activityInfo = json.load(response)

	resp = make_response(jsonify(activityInfo=activityInfo))
	return resp

@app.route('/updateActivity', methods=['POST'])
def updateActivity():
	print 'updateActivity'
	if 'username' in request.cookies:
		username = request.cookies.get('username')
		diff = request.form['diff']
		level = request.form['level']
		print level

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/updateActivity.php?username="+username+"&diff="+diff+"&level="+level
		response = urllib2.urlopen(url)
		activityInfo = json.load(response)

	resp = make_response(jsonify(activityInfo=activityInfo))
	return resp

########################
# connection with device

# @app.route('/debug')
# def debug():
#     return render_template('web_socket_debug.html')


# @socketio.on('bluetooth_conn', namespace='/test')
@app.route('/bluetooth_conn')
def bluetooth_conn():
	global device_data_generator, DEVICE_CONNECTED, ser, bluetooth_enabled
	print "user requested connection"
	DEVICE_CONNECTED=True
	from hercubit import device
	ser,conn_type=device.connect(bluetooth_enabled=bluetooth_enabled)
	if ser==None:
		resp = make_response(jsonify(connected=False))
		return resp
	device_data_generator=device.sensor_stream(ser,conn_type)#simulate_sample_rate=False
	from hercubit.settings import sampleRate
	resp = make_response(jsonify(sampleRate=sampleRate,bluetooth_enabled=bluetooth_enabled))
	return resp
	# emit('connection established',{'sample_rate': sampleRate*1000})

t0=0
all_data=[]
# Retrieve the data from device
# @socketio.on('get_sample', namespace='/test')
@app.route('/getsample')
def get_sample():
	global device_data_generator, t0,all_data
	from hercubit import rep_tracker
	if DEVICE_CONNECTED==True:
		if t0==0: t0=time.time()
		sample=device_data_generator.next()
		all_data.append(sample)
		# print sample #uncomment to see raw output
		# graph_html=hercubit.html_graph.run(sample,t0)
		# emit('graph',{"graph":graph_html})
		# print graph_html
		# app.logger.debug("done with grapher")
		count=rep_tracker.live_peaks(sample)
		if count!=None:
			# emit('device response', {'data': count})
			resp = make_response(jsonify(count=count))
		else:
			resp = make_response(jsonify(username=request.cookies['username']))
		return resp

#Exercise completed - add to DB
# @socketio.on('addexercise', namespace='/test')
@app.route('/addexercise', methods=['POST'])
def addexercise():
	global all_data
	exercise_data=request.form
	app.logger.debug(exercise_data)
	count= request.form['count']
	username = request.cookies.get('username')
	exercise=request.form['type']
	count=request.form['count']
	weight=request.form['weight']
	goal_complete=request.form['goal_complete']
	saved_data={"raw":all_data,"count":count,"username":username,"exercise":exercise,'weight':weight}
	# app.logger.debug(all_data)
	if os.path.exists('saved')==False: os.mkdir('saved')
	path=os.path.join("saved",time.strftime("%m-%d-%Y--%H-%M-%S")+".p")
	print os.listdir(os.getcwd())
	pickle.dump( saved_data, open( path, "wb" ) )

	url="http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/insertNewExercise.php?username="+username+"&exercise="+exercise+"&count="+str(count)+"&weight="+str(weight)+"&goal_complete="+goal_complete
	app.logger.debug("Exercise added to DB:\n"+str(exercise_data))
	response = urllib2.urlopen(url)
	userInfo = json.load(response)
	resp = make_response(jsonify(username=userInfo))
	return resp


# @socketio.on('stop', namespace='/test')
@app.route('/stop')
def stop():
	global DEVICE_CONNECTED, ser, t0
	ser.close()
	ser =''
	hercubit.rep_tracker.rep_count=0
	# from hercubit.html_graph import reset
	# t0=0
	# reset()
	#send to database - SEE ABOVE FUNCTION
	# addexercise(exercise_data)
	
	DEVICE_CONNECTED=False
	print "Connection stopped"
	# emit('Bluetooth Connection Stopped')
	resp = make_response(jsonify(conntction=DEVICE_CONNECTED))
	return resp


# # @socketio.on('web_socket_connected', namespace='/test')
# @app.route('/addexercise', methods=['POST'])
# def test_connect():
# 	print "Web Sockets: Client connected"
# 	emit('connect', {'data': 'Connected'})


# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Web Sockets: Client disconnected')


# @socketio.on('quit', namespace='/test')
@app.route('/quit')
def exit():
    quit()

# @app.route('/test_connection', methods=['POST'])
# def test_connection():
# 	resp = make_response(jsonify(connected=True))
# 	return resp


    

if __name__ == '__main__':
	import webbrowser
	# if app.debug!=True:
	webbrowser.open_new_tab('http://localhost:5000')
	# socketio.run(app)
	app.run()

