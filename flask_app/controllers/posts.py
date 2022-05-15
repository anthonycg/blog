# from crypt import methods
from crypt import methods
from flask_app.controllers import posts
from flask_app import app
from flask_app.models import user
from flask import Flask, render_template, request, session, flash, redirect
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/new/post')
def new_post():
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    #if in session, proceed to display page
    return render_template('create_post.html', user=user.User.get_one(data))

@app.route('/create/post', methods=['POST'])
def create_post():
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #validate user inputs
    if not Post.validate_post(request.form):
        return redirect('/new/post')
    #declare the data we received
    data = {
        "title": request.form['title'],
        "body": request.form['body'],
        "user_id": session['user_id']
    }
    Post.save(data)
    return redirect('/dashboard')



@app.route('/edit/post/<int:id>')
def edit(id):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "id": id
    }
    session_data = {
        "id":session['user_id']
    }
    return render_template('edit_post.html', post=Post.get_one(data), user=user.User.get_one(session_data))


@app.route('/update/post/<int:id>', methods=['POST'])
def update_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    #validate user inputs
    if not Post.validate_post(request.form):
        return redirect('/new/post')
    #declare needed data
    data = {
        "id":id,
        # "id": request.form['id'],
        "title": request.form['title'],
        "body": request.form['body'],
        # "user_id": session['user_id']
    }
    #invoke method save updates
    Post.update(data)
    return redirect('/dashboard')

@app.route('/post/<int:id>')
def show_post(id):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "id": id
    }
    session_data = {
        "id":session['user_id']
    }
    #invoke method to grab post with specified id
    post = Post.get_one_post_by_user(data)
    return render_template('show_post.html', post = post, user = user.User.get_one(session_data))

@app.route('/destroy/post/<int:id>')
def dunzo(id):
    #user must be in session bc anyone could delete paintings without logging in otherwise
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data we need to delete record
    data = {
        "id": id
    }
    #invoke delete method
    Post.dunzo(data)
    #return to dash
    return redirect('/dashboard')
