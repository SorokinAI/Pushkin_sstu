from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Posts(db.Model):
    author = db.Column(db.String(100), default='Александр Пушкин')
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Posts %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    articles = Posts.query.order_by(func.random()).all()
    return render_template("index.html", articles=articles)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/error_db_01')
def error_db_01():
    return render_template("error_db.html")


@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        if request.form['author'] == '':
            post = Posts(title=request.form['title'], text=request.form['text'])
        else:
            post = Posts(title=request.form['title'], text=request.form['text'], author=request.form['author'])

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/home')
        except:
            return redirect('/error_db_01')

    else:
        return render_template("create_post.html")


@app.route('/authors/<string:author>')
def profile(author):
    article = Posts.query.filter_by(author=author).all()
    data_first = Posts.query.filter_by(author=author).first()
    return render_template("profile.html", article=article, data=data_first)


if __name__ == "__main__":
    app.run(debug=True)
