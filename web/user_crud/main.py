import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect,url_for,session
from werkzeug import generate_password_hash, check_password_hash

@app.route('/new_user')
def add_user_view():
	return render_template('add.html')
		
@app.route('/add', methods=['POST'])
def add_user():
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User added successfully!')
			return redirect('/')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
'''
@app.route('/')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		return render_template('users.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
'''
@app.route("/")
def index():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		if 'username' not in session:
			return redirect(url_for('login'))
		else:
			print(session)
			#username_session = escape(session['username']).capitalize()
			return render_template('index.html', session_user_name="James")
	except Exception as e:
   		print(e)
	finally:
   		cursor.close()
   		conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		error = None
		if 'username' in session:
			return redirect(url_for('index'))
		if request.method == 'POST':
			username_form  = request.form['username']
			password_form  = request.form['password']
			cursor.execute("SELECT COUNT(1) FROM tbl_user WHERE user_name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
			if cursor.fetchone()[0]:
				cursor.execute("SELECT user_password FROM tbl_user WHERE user_name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
				for row in cursor.fetchall():
					if check_password_hash(row[0],password_form):
						session['username'] = request.form['username']
						return redirect(url_for('index'))
					else:
						error = "Invalid Credential"
			else:
				error = "Invalid Credential"
		return render_template('login.html', error=error)
	except Exception as e:
   		print(e)
	finally:
   		cursor.close()
   		conn.close()


@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_id = request.form['id']
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
if __name__ == "__main__":
    app.run()