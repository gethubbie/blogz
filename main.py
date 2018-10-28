from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:wannaHedoit@localhost:8889/build-a-blog'
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
    allowed_routes = ['login', 'signup','blog', 'home']
    if request.endpoint not in allowed_routes and 'username' not in session:
return redirect('/login')       

@app.route('/')
def index():
    return redirect('/blog')

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
            
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)
            return redirect (url)
          
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

if __name__ == '__main__':
    app.run()

