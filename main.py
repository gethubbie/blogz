from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:wannaHedoit@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jeremiah33:3ephesians3:20isaiah54:17'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)    
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref ='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup',  '/', 'newpost']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')       

#@app.route('/')
#def index():
    #return redirect('/blog')

@app.route('/newpost', methods=["POST", "GET"])
def newpost():
    if request.method == "POST":
        blog_title = request.form["blog_title"]
        blog_body = request.form["blog_body"]
        title_error = ""
        body_error = ""

        if blog_title == "":
            title_error = "Please provide a title!"
        if blog_body == "":
            body_error = "Please provide a body!"

        if blog_title != "" and blog_body != "":

            user = User.query.filter_by(username = session['username']).first()   
            new_blog = Blog(blog_title, blog_body, user)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)
            return redirect (url)

        if request.args.get('user'):
            userid = request.args.get('user')
            user = User.query.get(userid)
            your_name = user.username
            blogs = user.blogs
            return render_template('singleUser.html', username = your_name, blogs=blogs)

        if request.args.get('id'):
            blogid= request.args.get('id')
            single_blog = Blog.query.get(blogid)
            return render_template('single.html', single_blog=single_blog) 
            blogs = Blog.query.all()
            return render_template('blog.html', blogs=blogs)

        else:   
            return render_template('newpost.html')    
    return render_template('newpost.html')        
    
@app.route('/blog', methods=["POST", "GET"])
def blog():
    owner = User.query.filter_by(username=session['username']).first()
    
    single_blog = request.args.get('id')
    if single_blog:
        return render_template('single.html', title='single_blog', single_blog=Blog.query.get(single_blog))

    if request.args.get('userid'):
        user_id = request.args.get('userid')
        owner_blogs=Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blog.html', all_blogs=owner_blogs)

    else:
        all_blogs = Blog.query.all()
        return render_template('blog.html', title='Build a Blog', all_blogs=all_blogs)

@app.route('/')
def index():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', users=users)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify'] 
        existing_user = User.query.filter_by(username=username).first()
        
        username_error = ""
        password_error = ""
        verify_password_error = ""
               
        if username == '':
            username_error = 'Username cannot be blank!'
            
        if len(username) < 3 or len(username) > 35:
            username_error = "Username length must be between 3 and 35 characters"

        if password == '':
            password_error ='Password cannot be blank!'
            
        if len(password) < 3 or len(password) > 35:
            password_error = "Password length must be between 3 and 35 characters"      

        if verify_password != password:
            verify_password_error = "Passwords do not match.  Please verify password"

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')  

        else:
            flash("User already exists")

    return render_template('signup.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        if user and user.password != password:
            flash('User password incorrect.', 'error')
        else:
            flash('User does not exist.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()

