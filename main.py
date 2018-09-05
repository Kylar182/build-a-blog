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
    #name = db.Column(db.String(120))
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        #self.name = name
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect("/blog")

@app.route('/blog', methods=['POST', 'GET'])
def index():
    if request.args.get('id'):
        blog_posts = Blog.query.filter_by(id=request.args.get('id')).all()
        title_h1 = blog_posts[0].title
        body = blog_posts[0].body
    else:
        blog_posts = Blog.query.filter_by().all()
        title_h1 = "Build a Blog"
        body = ''
    print(title_h1)
    return render_template('blog.html', title_h1=title_h1, blog_posts=blog_posts, body=body)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_blog = Blog(new_title, new_body)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()