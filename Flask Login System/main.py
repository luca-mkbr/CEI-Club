from flask import Flask, request, render_template
from replit import db
import json
from hashlib import sha256

app = Flask("LoginSystem")

#Home page
@app.route("/", methods=['GET'])
def login_page():
  return render_template("login.html")

#Sign up page
@app.route("/signup", methods=['GET'])
def signup():
  return render_template("signup.html")

#Account registration ROUTE
@app.route("/register", methods=['POST'])
def register():
  username = request.form.get("username") #get username and password from HTML page
  password = request.form.get("password")
  if not(username in db): #if the user is not already created
    db[username] = json.dumps({"password": sha256(password.encode('utf-8')).hexdigest()}) #create and store password hash as JSON
    return render_template("index.html", user=username, encryptedPass=db[username]) #show main page logged in
  else:
    return render_template("alreadyregistered.html")

@app.route("/login", methods=['POST']) #Login ROUTE
def login():
  username = request.form.get("username")
  password = request.form.get("password")
  if(not (username in db)): #if the account does not exist
    return("User not found")
  value = db[username] #get password stored as JSON
  json_object = json.loads(value) #decode JSON
  if json_object["password"] == sha256(password.encode()).hexdigest(): #compare password hash to stored password hash
    return render_template("index.html", user=username, encryptedPass=db[username])
  return("User not found")

#for debugging
@app.route("/getusers", methods=['GET'])
def getUsers():
  from replit import db
  return(str(db.keys()))

@app.route("/deleteusers", methods=['GET'])
def deleteUsers():
  from replit import db
  for user in db.keys():
    del db[user]
  return("All users deleted")

app.run(host='0.0.0.0')