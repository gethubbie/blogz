from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:wannaHedoit@localhost:8889/build-a-blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jeremiah33:3ephesians3:20isaiah54:17'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.Foreignkey('user.id'))

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)    
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog', 'index']
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

        username = User.query.filter_by(username = session['username']).first()   
            new_blog = Blog(blog_title, blog_body, username)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)
            return redirect (url)

    if request.args.get('username'):
        userid = request.args.get('username')
        username = User.query.get(userid)
        your_name = username.username
        blogs = username.blogs
        return render_template('singleUser.html', username = your_name, blogs=blogs)

    if request.args.get('id'):
        blogid= request.args.get('id')
        single_blog = Blog.query.get(blogid)
        return render_template('single.html', single_blog=single_blog) # title=blog.title, body=blog.body)
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


        else:   
            return render_template('newpost.html', body_error=body_error, title_error=title_error)    
    else:
        return render_template('newpost.html')          

@app.route('/blog', methods=["POST", "GET"])
def blog():
    single_blog = request.args.get('id')
    if single_blog:
        return render_template('single.html', title='single_blog', single_blog=Blog.query.get(single_blog))
       
    else:
        all_blogs = Blog.query.all()
        return render_template('blog.html', title='Build a Blog', all_blogs=all_blogs)

@app.route('/')
def index():
    usernames = User.query(User.username).all()
    return render_template('index.html', usernames = usernames)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password'] 

        username_error = ""
        password_error = ""
        verify_password_error = ""

        existing_username = User.query.filter_by(username=username).first()
        
        if existing_username:
            error["username_error"] = "Username already exit!"
        
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

        if username_error == "" and password_error == "" and verify_password_error == "":
            username = User(username, password)
            db.session.add(username)
            db.session.commit()
            session['username'] = username
        return redirect("/newpost")   

        else:
            return render_template("signup.html", title="Signup", username=username, username_error=username_error, password_error=password_error, verify_password_error=verify_passwor_error)              

@app.route('/login', methods = ['POST', 'GET'])
def login():
        username_error = ""
        password_error = ""
        
        if request.method == 'POST'
        username = request.form['username']
        password = request.form['password']  
        existing_username = User.query.filter_by(username=username).first()

        if existing_username: 
            session['username'] = username
            return redirect('/newpost')

        if not existing_username:
            return render_template('login.html', username_error="Username does not exist.")
        else:
            return render_template('login.html', password_error="Username or password was incorrect.")

        return render_template('login.html')  

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()

