from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helper_functions import salt_password
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b51bbb993d3d5f:c72744a4@us-cdbr-iron-east-05.cleardb.net/heroku_7fe1da7f2899a08'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(100), nullable=False, unique=True)
    
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    password = db.Column(db.String(120), nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        
        salted_pass = salt_password(_password)
        hashed_pass = bcrypt.generate_password_hash(salted_pass)
        
        new_user = User(username=_username, email=_email, password=hashed_pass)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            print("there was an error creating your account") 
            return redirect('/')
        return redirect('/')
    else:
        return render_template('auth/reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        
        user = User.query.filter_by(username=_username).first()
        
        if bcrypt.check_password_hash(user.password, salt_password(_password)):
            return redirect('/')
        else:
            print("there was an error creating your account") 
            return render_template('index.html')
    else:
        return render_template('auth/login.html')

if __name__ == '__main__':
    app.run(debug=True)