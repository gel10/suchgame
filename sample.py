
from flask import *
from flask_pymongo import PyMongo
import hashlib
#import markdown2
#import re

app = Flask(__name__)
mongo = PyMongo(app)

################HOME PAGE###################
@app.route('/')
def home():
    return render_template('home.html')


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
	return render_template('homepage.html', uName = uName)
    else:
	return "Not a valid user"
	
   

####################run the function###################
if __name__ == '__main__': 
   
    app.debug = True
    app.run()

    
