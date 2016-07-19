from flask import *
from flask_pymongo import PyMongo 
import sample
   
if len(sample.signup.uName) >= 3 :
	nameChecker = True
	#print nameChecker
	name = request.form['name']
else:
	nameChecker = False
	print nameChecker
    
if sample.uPass == sample.uRePass:
	passChecker = True
	print passChecker
else:
	passChecker = False

