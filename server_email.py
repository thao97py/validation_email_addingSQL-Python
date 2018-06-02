from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import MySQLConnector
import re   ## the "re" module will let us perform some regular expression operations

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key= '234jrgmfkbgg0opfl'
mysql = MySQLConnector(app, 'friendsdb')

@app.route('/')
def index():
    return render_template('index_email.html')

@app.route('/success', methods=['POST'])
def create_email():
    email = request.form['email']
  
    if len(email)<1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(email):
        flash("Email is Invalid!")
    else:
        flash("The email address you entered: ("+ email + ") is a valid email address! Thank you!")
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {'email':email  }
        email_address = mysql.query_db(query, data)
        emails = mysql.query_db('select * from emails')
        return render_template("success.html", all_email=emails)
    return redirect('/')

@app.route('/deleting', methods=['POST'])
def delete_email():
    flash('An email is deleted!')
    query = "DELETE FROM emails WHERE id = :id"
    index = int(request.form['index'])
    data = {'id': index}
    mysql.query_db(query, data)
    emails = mysql.query_db('select * from emails')
    return render_template("success.html", all_email=emails)

if __name__ == "__main__":
    app.run(debug=True)
