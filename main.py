from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'grace'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    map_url = db.Column(db.Text, unique=True, nullable=False)
    img_url = db.Column(db.Text, unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    has_sockets = db.Column(db.Float, nullable=False)
    has_toilet = db.Column(db.Float, nullable=False)
    has_wifi = db.Column(db.Float, nullable=False)
    can_take_calls = db.Column(db.Float, nullable=False)
    seats = db.Column(db.String(120), nullable=False)
    coffee_price = db.Column(db.String(120), nullable=False)

    # def to_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Add_Cafe(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Map_url', validators=[DataRequired()])
    img_url = StringField('Image_url', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = StringField('Has sockets? e.g 1,2,3,...', validators=[DataRequired()])
    has_toilet = StringField('Has Toilet? e.g 1,2,3,...', validators=[DataRequired()])
    has_wifi = StringField('Has Wi-fi? e.g 1,2,3,...', validators=[DataRequired()])
    can_take_calls = StringField('Can take calls? e.g 1,2,3,..', validators=[DataRequired()])
    seats = StringField('Number of Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price in $', validators=[DataRequired()])
    Done = SubmitField('Add')


@app.route("/")
def Home():
    return render_template("index.html")


@app.route("/cafes")
def show_cafes():
    cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = Add_Cafe()
    if form.validate_on_submit():
        data = form.data
        new_cafe = Cafe(
            name=data['cafe_name'],
            map_url=data['map_url'],
            img_url=data['img_url'],
            location=data['location'],
            has_sockets=data['has_sockets'],
            has_toilet=data['has_toilet'],
            has_wifi=data['has_wifi'],
            can_take_calls=data['can_take_calls'],
            seats=data['seats'],
            coffee_price=data['coffee_price']
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('show_cafes'))

    return render_template('add.html', form=form)


@app.route("/delete/<cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('show_cafes'))


if __name__ == '__main__':
    app.run(debug=True)
