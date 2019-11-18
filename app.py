from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)

class zzhijie_singersAPP(db.Model):
    singerid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2}".format(self.singerid, self.first_name, self.last_name)

class singersForm(FlaskForm):
    pokemon_name = StringField('first name:', validators=[DataRequired()])
    maximum_cp = StringField('last name' CP:', validators=[DataRequired()])


@app.route('/')
def index():
    all_singers = zzhijie_singersAPP.query.all()
    return render_template('index.html', singers=all_singers, pageTitle='New Singer')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        form=request.form
        search_value=form['search_string']
        search = "%{}%".format(search_value)
        results = zzhijie_singersAPP.query.filter(zzhijie_singersAPP.first_name.like(search)).all()
        return render_template('index.html', singer=results, pageTitle='Singers',legend="Search Result")
    else:
        return redirect('/')




@app.route('/singers/new', methods=['GET', 'POST'])
def add_singer():
    form = singersForm()
    if form.validate_on_submit():
        singers = zzhijie_singersAPP(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')

    return render_template('add_singer.html', form=form, pageTitle='Add A New Singer', legend="Add A New Singer")

@app.route('/singers/<int:singerid>', methods=['GET','POST'])
def singers(singerid):
    singers = zzhijie_singersAPP.query.get_or_404(singerid)
    return render_template('singer.html', form=singers, pageTitle='Singers Details')

@app.route('/pokemon/<int:pokemon_Id>/update', methods=['GET','POST'])
def update_singers(singerid):
    singer = zzhijie_singersAPP.query.get_or_404(singer_id)
    form = SingersForm()
    if form.validate_on_submit():
        singers.first_name = form.first_name.data
        singers.last_name = form.last_name.data
        db.session.commit()
        flash('The singer has been updated.')
        return redirect(url_for('singers', singerid=singers.singerid))
    elif request.method == 'GET':
        form.first_name.data = singers.first_name
        form.last_name.data = singers.last_name


    return render_template('add_singer.html', form=form, pageTitle='Update Post', legend="Update a singer")

@app.route('/delete_singer/<int:singerid>', methods=['POST'])
def delete_singers(singerid):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        singers = zzhijie_singersAPP.query.get_or_404(singerid)
        db.session.delete(singer)
        db.session.commit()
        flash('Singer was successfully deleted!')
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
