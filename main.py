from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form, BooleanField, StringField, validators, SubmitField, TextAreaField
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c45264839c074e240ec999b2d2d97'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dvesti.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

ckeditor = CKEditor(app)


class Add_article(Form):
    title_article = StringField('title_article', [validators.DataRequired(), validators.Length(max=100)])
    text_article = CKEditorField('text_article', [validators.DataRequired()])
    submit = SubmitField('Сохранить')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_article = db.Column(db.String, nullable=False)
    text_article = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())


@app.route('/')
def index():
    return render_template('main/index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html', title='Dashboard')


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = Add_article()
    if request.method == 'POST' and form.validate():
        title_article = request.form['title_article']
        text_article = request.form['text_article']
        article = Article(
            title_article, text_article
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("dashboard.html"))
    return render_template('dashboard/add_article.html', form=form, title='Добавить статью')


if __name__ == '__main__':
    app.run(debug=True)
