from users_cr_app import app
from flask import render_template,redirect,request,session,flash
from users_cr_app.models.users import User



# these are all the sites different pages
@app.route('/users')
def index():
    users = User.get_all()
    return render_template('read.html', all_users = users)
 
@app.route('/users/new')
def new():
    return render_template('create.html')

@app.route("/users/<int:id>")
def show(id):
    data = {
        "id": id
    }
    user = User.get_one(data)
    return render_template('show.html', user=user)

@app.route('/users/edit/<int:id>')
def edit(id):
    data = {
        "id":id
    }
    user = User.get_one(data)
    return render_template('edit.html', user=user)

# this is where information is processed
@app.route('/users/creating_user', methods=["POST"])
def user():
    data = {
        "session['first_name']": request.form["first_name"],
        "session['last_name']" : request.form["last_name"],
        "session['email']" : request.form["email"]
    }
    User.save(data)
    return redirect('/users')

@app.route('/users/editing_user', methods=['POST'])
def editing():
    data = {
        "session['id']" : request.form['id'],
        "session['first_name']": request.form["first_name"],
        "session['last_name']" : request.form["last_name"],
        "session['email']" : request.form["email"]
    }
    User.edit(data)
    return redirect('/users')

@app.route('/users/delete/<int:id>')
def delete(id):
    data = {
        "id" : id
    }
    User.delete(data)
    return redirect('/users')

