from flask import Flask, redirect, url_for, request , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import and_
from sqlalchemy import text
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	last  = db.Column(db.String(50)) 
	date = db.Column(db.Integer)
	email = db.Column(db.String(50),unique=True) 

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
	bday_list = db.session.query(User).filter_by(date = today)
	return render_template('bday_list.html',bday = bday_list)
	

@app.route('/addrec', methods = ['GET', 'POST'])
def addrec():
	if request.method == 'POST':
		data = User(request.form['name'], request.form['last'],request.form['date'],request.form['email'])
		db.session.add(data)
		db.session.commit()	
	return render_template('next.html')  


@app.route('/see')
def see():
   return render_template('see.html' ,data=User.query.all())

@app.route('/send') 
def send():
	today = datetime.date.today().strftime("%d/%m")
	fromaddr = "sonam0211@gmail.com"
	toaddr = db.session.query(User).filter_by(date = today)
	
	for a in toaddr:

		msg = MIMEMultipart() 
		msg['From'] = fromaddr
		msg['To'] = a.email 
		msg['Subject'] = "Happy BirthDay"
		body = "Many Many Happy Returns Of The Day %s" %a.name
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
		server.login(fromaddr, "02111996")
		text = msg.as_string()
		server.sendmail(fromaddr, a.email, text)
		server.quit()
	return "mail has been sent" 

	
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
