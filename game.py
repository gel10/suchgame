"""" 
THIS CODE IS UNFINISHED. 
THIS IS NOT AN OPTIMIZED CODE.
WILL FIX IT NEXT TIME :)
"""

from flask import *
from random import * 
import hashlib
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def home():
	resp = make_response(render_template('home.html' , uName = request.cookies.get('uName')))
	return resp


####################OPEN SIGNUP PAGE###################
@app.route('/opensignup')
def opensignup():
    return render_template('signup.html')
	

####################AUTHENTICATE SIGNUP################### 		
@app.route('/signup', methods=['POST'])
def signup():
    uName = request.form['uName']
    uPass = request.form['uPass']
    uRePass = request.form['uRePass']
    result = mongo.db.user.find({'uName' : request.form['uName'],'uPass':request.form['uPass']}).count()

    if len(uName) >= 3 :
	nameChecker = True
	name = request.form['name']
    else:
	nameChecker = False
	print nameChecker
    
    if uPass == uRePass:
	passChecker = True
	hashed = hashlib.md5(uPass.encode())
	hashedPass = hashed.hexdigest()
	print passChecker
    else:
	passChecker = False

    
    if (result != 0):
	nameChecker = False
    else:
	nameChecker = True

    return signupResult(nameChecker, passChecker, hashedPass)


####################SIGN UP RESULT SUCCESS OR FAIL###################
def signupResult(nameChecker, passChecker, hashedPass):
    uName = request.form['uName']

    if nameChecker == False or passChecker == False:
	 return "Wrong Format"
    elif nameChecker == True and passChecker == True: #if successful
   	 mongo.db.user.insert(
            {'name' : request.form['name'],'uName':request.form['uName'], 'uPass': hashedPass}      
            )
    return render_template('homepage.html', uName = uName)

####################OPEN SIGNIN PAGE###################
@app.route('/opensignin')
def opensignin():
    return render_template('signin.html')

####################AUTHENTICATE SIGNUP###################              
@app.route('/signin', methods=['POST'])
def signin():
    uName = request.form['uName']
    uPass = request.form['uPass']
    #mongo.db.user.ensure_index( {'uName':1}, {'unique': 'true'})
    #make uName field unique
    mongo.db.user.create_index('uName', unique = True)
    hashed = hashlib.md5(uPass.encode())
    hashedPass = hashed.hexdigest()

    result = mongo.db.user.find({'uName' : request.form['uName'],'uPass':hashedPass}).count()
    
    if (result != 0):
	print  mongo.db.user.find({'uName' : request.form['uName'],'uPass':request.form['uPass']}).count()
	

   	
	resp = make_response(render_template('home.html' , uName = request.cookies.get('uName')))
	resp.set_cookie('uName', uName)
	uName = request.cookies.get('uName')
	return resp
   	
    else:
	return "Not a valid user"
	

####################OPEN GAME PAGE###################
@app.route('/game')
def game():
    resp = make_response(render_template('game.html' , uName = request.cookies.get('uName')))
    
    return resp
	

####################GAME MECHANICS###################
@app.route('/playgame' , methods=['POST'])
def playgame():
	playerOpt = request.form['playerOpt']
	gameOptions = ['scissors', 'rock' , 'paper']
	computerOpt = gameOptions[randint(0,2)]
	uName = request.form['uName']
	score = 0

	if playerOpt == computerOpt:
			value = "TIE! computer picked %s and you picked %s" % (computerOpt, playerOpt)

	elif playerOpt == "rock":
			if computerOpt == "paper":
				value = "You lose! computer picked %s and you picked %s" % (computerOpt, playerOpt)
			elif computerOpt == "scissors":
				value = "You win! computer picked %s and you picked %s" % (computerOpt, playerOpt)
				score += 1
	elif playerOpt == "paper":
			if computerOpt == "scissors":
				value = "you lose!  computer picked %s and you picked %s" % (computerOpt, playerOpt)
			elif computerOpt == "rock":
				value = "you win! computer picked %s and you picked %s" % (computerOpt, playerOpt)
				score += 1
	elif playerOpt == "scissors":
			if computerOpt == "rock":
				value = "you lose! computer picked %s and you picked %s" % (computerOpt, playerOpt)
			elif computerOpt == "paper":
				value = "you win! computer picked %s and you picked %s" % (computerOpt, playerOpt)
				score += 1
	
	mongo.db.gameJack.insert(
            {'uName':request.form['uName'], 'jResult': value , 'jScore': score}      
        )
	currentScore = mongo.db.gameJack.find({'uName': request.cookies.get('uName') , 'jScore': 1}).count()
	resp = make_response(render_template('result.html' , uName = request.cookies.get('uName') , value = value , currentScore = currentScore))
	return resp

###############DISPLAY SCORE TO USER######################
@app.route('/showScore')
def showScore():
	currentScore = mongo.db.gameJack.find({'uName': request.cookies.get('uName') , 'jScore': 1}).count()
	resp = make_response(render_template('score.html' , uName = request.cookies.get('uName') , currentScore = currentScore))
	
	return resp 

@app.route('/game2')
def game2():
	resp = make_response(render_template('room.html' , uName = request.cookies.get('uName')))
	
	return resp 
	


####################GAME MECHANICS###################
@app.route('/gamePvp' , methods=['POST'])
def gamePvp():
	uName =  request.cookies.get('uName')
	roomNo = request.form['roomNo']
	resultList = []
	noDupes = []
	message = ""

	mongo.db.roomNumber2.insert( {'uName':request.form['uName'], 'roomNo': roomNo , 'roomStatus': 'open'})
	
	if mongo.db.roomNumber2.find({'roomNo': roomNo}).count() == 1 :
		message = "waiting for the other player"
		return render_template('error.html' , roomNo = roomNo, uName = uName , message = message)
	else:
		users = mongo.db.roomNumber2.find({'roomNo': roomNo} , {'uName': 1 , '_id' : 0})
		#inserts cursor type result to a list 
		for x in users :
			val = str(x[u'uName'])
			resultList.append(val)

		#inserts the unique value of a resultList in a new list.
		[noDupes.append(i) for i in resultList  if not noDupes.count(i)]
	
		#if the user is only one in a room, it goes back to the same page.
		if (len(noDupes) == 1): 
			message = "waiting for the other player"
			return render_template('error.html' , roomNo = roomNo, uName = uName , message = message)

		# if there are 2 users in a room 
		elif (len(noDupes) == 2):
			resp1 = make_response(render_template('gamePvp.html' , noDupes = noDupes, roomNo = roomNo, uName = request.cookies.get('uName')))
			resp1.set_cookie('roomNo' , roomNo)
			return resp1
		#in case there are 3 or more users in a room
		else:
			return "this room is full"
			#return redirect(url_for('gamePvpPlay',users = users, roomNo = roomNo,  uName = request.cookies.get('uName')))
	

####################GAME MECHANICS###################
@app.route('/gamePvpPlay' , methods=['POST'])
def gamePvpPlay():
	playerOpt = request.form['playerOpt']
	roomNo = request.form['roomNo']
	uName = request.form['uName']
	uNameCookie  = request.cookies.get('uName')
	score = 0

	mongo.db.gameJack2.insert(
            {'uName':request.form['uName'], 'roomNo': roomNo , 'playerOpt': playerOpt}      
        )
	
	#checks if there are only one result found in a room
	if mongo.db.gameJack2.find({'roomNo' : roomNo}).count() == 1:
		message = "waiting for the other player to respond..."
		playerOpt = mongo.db.gameJack2.find({'uName' : uNameCookie , 'roomNo': roomNo} , {'playerOpt' :1 , '_id': 0})
			    
		resultList = []
		for x in playerOpt:
			val = str(x[u'playerOpt'])
			resultList.append(val)

		return render_template('gamePvp-error.html' , roomNo = roomNo, uName = uName , message = message , resultList = resultList)
	
	else:
		#gets the value (rock, paper or scissors) the user picked 
		mongo.db.gameJack2.find({'uName': uNameCookie , 'roomNo': roomNo} , {'playerOpt':1 , '_id':0})

		#gets all the value(rock, paper or scissors) picked by all user in the room
		result = mongo.db.gameJack2.find({'roomNo': roomNo} , {'playerOpt':1 , '_id':0})

		#compare = mongo.db.gameJack2.find({'roomNo': roomNo} , {'_id':0})
		resultList = []
		for x in result:
			val = str(x[u'playerOpt'])
			resultList.append(val)
		
		#prints player names  in the corresponding room and the value they picked (rock paper or scissors) 
		playerResults = mongo.db.gameJack2.find({'roomNo' : roomNo}, {'playerOpt': 1 , '_id':0 , 'uName': 1})
		playerOpt = []
		playerNames = []
		NameOfWinner = ""
		for x in playerResults:
			value = str(x[u'playerOpt'])
			playerOpt.append(value)

		playerResults2 = mongo.db.gameJack2.find({'roomNo' : roomNo}, {'playerOpt': 1 , '_id':0 , 'uName': 1})
		for y in playerResults2:
			name = str(y[u'uName']) 
			playerNames.append(name)

		resultList = zip(playerNames , playerOpt)
		
		for z in resultList:
			print "%s , %s" % z

		
		if (len(resultList) == 2):
			if playerOpt[0] == playerOpt[1]:
				value = "it's a tie"
				return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = "draw!")
			elif playerOpt[0] == 'rock':
				if playerOpt[1] == 'paper': #winner  playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'scissors': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
			elif playerOpt[0] == 'paper':
				if playerOpt[1] == 'scissors': #winner playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'rock': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
			elif playerOpt[0] == 'scissors':
				if playerOpt[1] == 'rock': #winner playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'paper': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
		
####################GAME MECHANICS###################
@app.route('/gamePvpPlayResult' , methods=['POST'])
def gamePvpPlayResult():		
	playerOpt = request.form['playerOpt']
	roomNo = request.form['roomNo']
	uName = request.form['uName']
	uNameCookie  = request.cookies.get('uName')
	
	
	##########REMEMBER TO PUT THIS INTO A FUNCTION AND JUST CALL IT!################
	if mongo.db.gameJack2.find({'roomNo' : roomNo}).count() == 1:
		message = "waiting for the other player to respond..."
		playerOpt = mongo.db.gameJack2.find({'uName' : uNameCookie , 'roomNo': roomNo} , {'playerOpt' :1 , '_id': 0})
			    
		resultList = []
		for x in playerOpt:
			val = str(x[u'playerOpt'])
			resultList.append(val)

		return render_template('gamePvp-error.html' , roomNo = roomNo, uName = uName , message = message , resultList = resultList)
	else:
		#gets the value (rock, paper or scissors) the user picked 
		mongo.db.gameJack2.find({'uName': uNameCookie , 'roomNo': roomNo} , {'playerOpt':1 , '_id':0})

		#gets all the value(rock, paper or scissors) picked by all user in the room
		result = mongo.db.gameJack2.find({'roomNo': roomNo} , {'playerOpt':1 , '_id':0})

		#compare = mongo.db.gameJack2.find({'roomNo': roomNo} , {'_id':0})
		resultList = []
		for x in result:
			val = str(x[u'playerOpt'])
			resultList.append(val)
		
		#prints player names  in the corresponding room and the value they picked (rock paper or scissors) 
		playerResults = mongo.db.gameJack2.find({'roomNo' : roomNo}, {'playerOpt': 1 , '_id':0 , 'uName': 1})
		playerOpt = []
		playerNames = []
		NameOfWinner = ""
		for x in playerResults:
			value = str(x[u'playerOpt'])
			playerOpt.append(value)

		playerResults2 = mongo.db.gameJack2.find({'roomNo' : roomNo}, {'playerOpt': 1 , '_id':0 , 'uName': 1})
		for y in playerResults2:
			name = str(y[u'uName']) 
			playerNames.append(name)
		
		resultList = zip(playerNames, playerOpt)
		for z in resultList:
			print "%s , %s" %z 

		if (len(resultList) == 2):
			if playerOpt[0] == playerOpt[1]:
				value = "it's a tie"
				return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = "draw!")
			elif playerOpt[0] == 'rock':
				if playerOpt[1] == 'paper': #winner  playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'scissors': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
			elif playerOpt[0] == 'paper':
				if playerOpt[1] == 'scissors': #winner playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'rock': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
			elif playerOpt[0] == 'scissors':
				if playerOpt[1] == 'rock': #winner playerNames[1] perspective
					NameOfWinner = playerNames[1]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
				elif playerOpt[1] == 'paper': #loser
					NameOfWinner = playerNames[0]
					return render_template("resultPvp.html", uName = uName ,resultList = resultList , val = NameOfWinner)
		
				

###########################RUN THE APP##########################
if __name__ == '__main__':
	app.debug = True
	app.run()

