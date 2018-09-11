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
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect("/home")

@app.route('/register', methods=['GET','POST'])
def register():
    password_error = ''
    verify_error = ''
    email_error = ''
    password = ''
    verify = ''
    email = ''

    if request.method == 'POST':
        email = (request.form['email'])
        password = (request.form['password'])
        verify = (request.form['verify'])

        if password == '' or len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = 'Password Invalid'
        if verify != password:
            verify_error = 'Password Invalid'
        if len(email) < 3 or len(email) > 50 or ' ' in email or '.' not in email or '@' not in email:
            email_error = 'Email Invalid'
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            email_error = 'Email in Database'

        if password_error == '' and email_error == '':
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
    
    return render_template('signup.html',title="Signups", password_error=password_error, verify_error=verify_error, email_error=email_error, email=email, )

@app.before_request
def require_login():
    allowed_routes=['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/')
        else:
            flash("You failed Dummy", "error")

    return render_template("login.html")

@app.route('/singleuser')
def spec_user():
    if "id" in request.args:
        user_id = request.args.get("id")
        id = User.query.get(user_id)
        user_blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleuser.html', user_blogs=user_blogs, id=id, user_id=user_id)

@app.route('/home', methods=['POST', 'GET'])
def homie():
    user_id = User.query.filter_by().all()
    return render_template('home.html', user_id=user_id)

@app.route('/blog', methods=['POST', 'GET'])
def index():
    current_user = User.query.filter_by(email=session['email']).first()
    spec_user = User.query.filter_by(email=session['email']).first()
    if request.args.get('id'):
        blog_posts = Blog.query.filter_by(id=request.args.get('id')).all()
        title_h1 = blog_posts[0].title
        body = blog_posts[0].body
    else:
        blog_posts = Blog.query.filter_by().all()
        title_h1 = "Build a Blog"
        body = ''
    blogz = Blog.query.filter_by(owner=current_user).all()
    return render_template('blog.html', title_h1=title_h1, blog_posts=blog_posts, body=body, blogz=blogz)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        current_user = User.query.filter_by(email=session['email']).first()
        new_blog = Blog(new_title, new_body, current_user)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()