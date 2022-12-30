from flask import render_template, request, redirect, session, flash
from flask_app.models.shows_model import Show
from flask_app.models.users_model import User
from flask_app import app



@app.route('/shows')
def shows():
    user_id = session['user_id']
    return render_template("all_shows.html", shows=Show.get_all(user_id))

@app.route("/shows/create")
def create_shows_form():
    return render_template("new_show.html")

@app.route('/shows/new', methods=["POST"])
def create_recipe():
    data = {
        "user_id": session['user_id'],
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
    }
    if Show.is_valid_show(request.form):
        Show.save(data)
        return redirect('/shows')
    return redirect('/shows/create')

@app.route("/shows/edit/<int:id>")
def edit_show(id):
    data={
        "id":id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("edit_show.html", show=Show.get_one(data))

@app.route('/shows/update',methods=['POST'])
def update_show():
    data = {
        "id":id,
        "user_id": session['user_id'],
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
    }
    if not Show.is_valid_show(request.form):
        return redirect('/shows/edit/<int:id>', show=Show.get_one(data))
    Show.update(request.form)
    return redirect('/shows')


@app.route('/shows/view/<int:id>')
def view_show(id):
    data ={ 
        "id":id
    }
    return render_template("view_show.html",show=Show.get_one_with_user(data))

@app.route('/shows/delete/<int:id>')
def delete_show(id):
    data ={
        'id': id
    }
    Show.destroy(data)
    return redirect('/shows')