from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:gloryglory@localhost:8889/build-a=blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'habakkuk2:3proberts3:1-5psalms119:71'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
    self.title = title
    self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=["POST", "GET"])
def newpost():
    if request.method == "POST":
        blog_title = request.form["title"]
        blog_body = request.form["body"]
        if blog_title == "" or blog_body == "":
           flash("DO NOT leave this field empty, please fill in both fields", 'error')
           render_template(newpost.html, title="Build a Blog", blog_body=new_blog)
    else:
        db.sesion.add(new_blog)
        db.session.commit()
        url = '/blog?id=' + str(new_blog.id)
        return redirect (url)
 
return render_template(newpost_html, title="Build a Blog")       

@app.route('/blog', methods=["POST", "GET"])
def blog():
    single_blog = request.args.get('id')
    return render_template('single_blog.html', title='Build a Blog', post=get_blog(single_blog))
    else:
        all_blogs = Blog.query.all()
        return render_template('blog.html'.title='Build a Blog', blog=all_blogs)

if __name__ == '__main__':
    app.run()

