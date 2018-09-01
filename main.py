from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pewpew@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '3j2kl3j4kl123j415@@28n'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, name, title, body):
        self.name = name
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, current_user)
        db.session.add(new_task)
        db.session.commit()

    blog_posts = Blog.query.filter_by().all()
    return render_template('blog.html',title="Build a Blog", blog_posts=blog_posts)

@app.route('/newpost', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, current_user)
        db.session.add(new_task)
        db.session.commit()

    return render_template('newpost.html',title="Add a Blog Entry")


if __name__ == '__main__':
    app.run()