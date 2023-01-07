from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, InputRequired
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from time import strftime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
with app.app_context():
    class Cafe(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(250), unique=True, nullable=False)
        map_url = db.Column(db.String(500), nullable=False)
        img_url = db.Column(db.String(500), nullable=False)
        location = db.Column(db.String(250), nullable=False)
        seats = db.Column(db.String(250), nullable=False)
        has_toilet = db.Column(db.Boolean, nullable=False)
        has_wifi = db.Column(db.Boolean, nullable=False)
        has_sockets = db.Column(db.Boolean, nullable=False)
        can_take_calls = db.Column(db.Boolean, nullable=False)
        coffee_price = db.Column(db.String(250), nullable=True)

        db.session.commit()


class NewCafe(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Address", validators=[DataRequired()])
    coffee_price = StringField("Average Price", validators=[DataRequired()])
    seats = StringField("Seats?", validators=[DataRequired()])
    has_toilet = SelectField("Toilet? ", choices=[('', 'No'), (True, 'Yes')], coerce=bool)
    has_wifi = SelectField("WiFi? ", choices=[('', 'No'), (True, 'Yes')], coerce=bool)
    has_sockets = SelectField("Sockets? ", choices=[('', 'No'), (True, 'Yes')], coerce=bool)
    can_take_calls = SelectField("Take Calls? ", choices=[('', 'No'), (True, 'Yes')], coerce=bool)
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = Cafe.query.all()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = Cafe.query.get(post_id)
    if not requested_post.has_wifi:
        wifi = "👎"
    else:
        wifi = "👍"
    if requested_post.has_toilet:
        toilet = "👍"
    else:
        toilet = "👎"
    if requested_post.has_sockets:
        sockets = "👍"
    else:
        sockets = "👎"
    if requested_post.can_take_calls:
        calls = "👍"
    else:
        calls = "👎"
    return render_template("post.html", post=requested_post, wifi=wifi, toilet=toilet, sockets=sockets,
                           calls=calls)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = NewCafe()

    if form.validate_on_submit():
        new_post = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            location=form.location.data,
            img_url=form.img_url.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
            seats=form.seats.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Cafe.query.get(post_id)
    edit_form = NewCafe(
        name=post.name,
        location=post.location,
        img_url=post.img_url,
        map_url=post.map_url,
        has_toilet=post.has_toilet,
        has_wifi=post.has_wifi,
        has_sockets=post.has_sockets,
        can_take_calls=post.can_take_calls,
        coffee_price=post.coffee_price,
        seats=post.has_toilet
    )
    if edit_form.validate_on_submit():
        post.name = edit_form.name.data
        post.location = edit_form.location.data
        post.img_url = edit_form.img_url.data
        post.map_url = edit_form.map_url.data
        post.has_toilet = edit_form.has_toilet.data
        post.has_wifi = edit_form.has_wifi.data
        post.has_sockets = edit_form.has_sockets.data
        post.can_take_calls = edit_form.can_take_calls.data
        post.coffee_price = edit_form.coffee_price.data
        post.seats = edit_form.seats.data
        db.session.commit()
        return redirect(url_for("get_all_posts", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


if __name__ == "__main__":
    app.run(debug=True)
