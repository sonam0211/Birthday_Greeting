from flask import Flask, redirect, url_for, request , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import and_
from sqlalchemy import text
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('guest_id', db.Integer, primary_key = True)
   	name = db.Column(db.String(100))
   	last  = db.Column(db.String(50)) 
   	date = db.Column(db.Integer)
   	email = db.Column(db.String(50)) 

   	def __init__(self, name, last, date,email):
	  	self.name = name
	  	self.last = last
	  	self.date = date
	  	self.email = email

@app.route('/')
def welcome():
	return render_template('welcome.html')

@app.route('/fill')
def fill():
	return render_template('fill.html')               

@app.route('/mail')	
def mail():
	today = datetime.date.today().strftime("%d/%m")
	if db.session.query(User).filter_by(date = today).first():
		fromaddr = "example@gmail.com"
		toaddr = db.session.query(User).filter_by(date = today).first().email 
		msg = MIMEMultipart() 
		msg['From'] = fromaddr
		msg['To'] = toaddr
		name1= db.session.query(User).filter_by(date = today).first().name 
		msg['Subject'] = "Happy BirthDay"
		body = "Many Many Happy Returns Of The Day %s" %name1
		msg.attach(MIMEText(body, 'plain'))
		filename = "best-birthday-greeting-cards.jpg"
		attachment = open(".\\best-birthday-greeting-cards.jpg","rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "password")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
		return "mail has been sent"


@app.route('/addrec', methods = ['GET', 'POST'])
def addrec():
	if request.method == 'POST':
		 if request.form['name'] and request.form['last'] and request.form['date'] and request.form['email']:
			data = User(request.form['name'], request.form['last'],request.form['date'],request.form['email'])
		 db.session.add(data)
		 db.session.commit()
	return render_template('next.html')  


@app.route('/see')
def see():
   return render_template('see.html' ,data=User.query.all())

	
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
