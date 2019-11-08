from flask import Flask
from flask import render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
@@ -43,6 +43,22 @@ def add_Song():

    return render_template('add_friend.html', form=form, pageTitle='Add A New Friend')

@app.route('/delete_Songs/<int:songID>', methods=['GET','POST'])
def delete_friend(songID):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        obj = colbert_friends.query.filter_by(friendid=friendid).first()
        db.session.delete(obj)
        db.session.commit()
        flash('Song was successfully deleted!')
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")







if __name__ == '__main__':
