import sqlite3

from flask import Flask, render_template, url_for, request, redirect, flash
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
from flask_paginate import Pagination, get_page_parameter

# instantiate the Flask app
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Oldmonkrsk5@'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = sqlite3.connect('database.db')
    posts = conn.execute('SELECT * FROM posts WHERE id=?',
                        (post_id,)).fetchone()
    print(posts)
    conn.close()
    if posts is None:
        abort(404)
    return posts


# function to delete from blog post table
def delete_from_blog_table(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    print('successfully deleted')
# delete_from_blog_table(62)


def get_portfolio_post(post_title):
    conn = sqlite3.connect('database.db')
    posts = conn.execute('SELECT * FROM portfolio WHERE title=?',
                        (post_title,)).fetchone()
    print(posts)
    conn.close()
    if posts is None:
        abort(404)
    return posts

# home page route
@app.route("/")
@app.route("/home")
def home():
    posts = [
        {
            "title": "Python with XSUAA",
            "link": "https://github.com/ishika1234-sudo/xsuaa-python",
            "content": "The python application uses XSUAA service to enable user authentication.\
                    It uses tokens using the authentication code to store the users details.",
            "image": "https://2.bp.blogspot.com/-PqGSPMF9pKE/W1hih6PBvvI/AAAAAAAAUDU/sVk7wntbavAb0Lzu91TksuaQw6Mcbn1gwCLcBGAs/s1600/1.png"
        },
        {
            "title": "Postman Clone",
            "link": "https://github.com/ishika1234-sudo/Postman-Clone-website",
            "content": "This is simple website that shows a postman clone using javascript.\
                            languages used are pure javascript, HTML and CSS.",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAR8AAACvCAMAAADzNCq+AAABIFBMVEX////+bTj6///+bTT5/////v7+//72///8//z8azL9azb//fvz/////f////z9bTn+ajr/Zy79+PT+//n9ZzH6//j/+//5azv6bjf3lnDzwKf99O36YCH+ai3weUv/ZynwdkT68OLwmXLpglT6WQDxbz38+e30YyTudTr5UwDwhVz76N7zbTX6YCX/ZR/z4tL00rv1s43xqIPzqZP4waz00cb34Nv0moDzflnr0bTxnon0aSrvpYr2tZ/stJT4dE785+PpmWf1xqbywK/tjFv57Nj2k3brcC31fmD8Zg/1za/4WCv22MT4inT31M33imPqtI7ybB7yloLxgEv1q53pmXX9y8L14MXqh2LpkF3xc0/7dCzy//DytaX6UQDufED9kPPbAAAR50lEQVR4nO1dC1vaSNsOTyaTyYQkhASJJCGCQigkAY91N6K+VdvV5V2/fl3f9Wu77/7/f/FNQFvPyiFL6Hpf7eUJwbl5zvPMMxz3ile84hWveMUrXvGKV7xicQCEAGYghMiyrKrsPybAcZgTBIzn/dfNH4oiKAr7CMD+AUIYkMI+x4BlwGTef938gYCotW7v3frGRX05Qf1ic3Nre+ewiA31nyo/IBBMDAxgD/pvdxtmGDq6qV/Dcz1H9xu7G5WujZiqIUHg4B9FlbAkADR/+vkgdkzTpLkczUkSzz4yUKol36DU1EMnru5t2yqIhFH0DwIqdfurvuO5tMDz/JCW64/fQa3AiqUo8tv9bpOZpH8GFIzUzv6B75k5TdNyT0IbyZPnOdVK10DCD2+vmZLk7aNL05cs+jQ1N+VIYgid1aMmh7gfWM1AkRFXexs4Jl94TnJu8cPzErUs04n3OsxOK/NeR1qQCfrtre9J9OWic4smZrD95S5GaN4LSQm4uxy5/H07/GJYOc0Mlwfqj6dkwhLhTi58k/nuyelh/FDJcvX6oWjg0g9lqpV8cb+sT0zMd7Agieqnm4RTfhwZYpEvnK045hgu61HwjJ9cOQrOxB/FCgmGArV/+a41jst6GpSnTr3GMv+FlyGB0SOSXtmk0szYSaBJTvkd/gHsNBbArvtmOZBmSQ8TIS126jbgBc/wCaDuridN7rKeokivdoEscAmNSb+AzwpeMIVLf5og/0gVjXkv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"
        },
        {
            "title": "Angular 6 website",
            "link": "https://github.com/ishika1234-sudo/Angular-6-website",
            "content": "A simple website with no backend that demonstrates only the frontend functionality. It is made in\
                          angular JS, a javascript framework.",
            "image": "data:image/png;base64,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"

        }]

    blog =[{"title": "Wo baani khubsurat",
            "link": "http://127.0.0.1:5000/blog/1",
            "image":"https://neilpatel.com/wp-content/uploads/2017/08/blog.jpg"

    },
  {         "title": "The journey of an athiest",
            "link": "https://github.com/ishika1234-sudo/xsuaa-python",
            "image":"data:image/png;base64,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"
  },
            {       "title": "Empower me the truth",
             "link": "https://github.com/ishika1234-sudo/xsuaa-python",
             "image": "data:image/jpeg;base64,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"

             }
            ]
    return render_template('home.html', posts=posts, blog=blog)


# about page route
@app.route("/about")
def about():
    return render_template('about.html')


# about page route
@app.route("/blog")
def blog():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    print('blog',posts)
    conn.close()
    search = False
    limit = 4
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * limit
    end = page * limit if len(posts) > page * limit else len(posts)
    pagination = Pagination(page=page, total=len(posts), css_framework='foundation', search=search, record_name='blogs',
                            per_page=4)
    posts = posts[start: end]
    return render_template('blog.html', posts=posts, pagination=pagination)


# view function to return a particular post
@app.route("/blog/<int:post_id>")
def post(post_id):
    posts = get_post(post_id)
    print(posts[1])
    return render_template('post.html', post=posts)


# form to fill blog details into table
@app.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('TITLE IS NEEDED')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
            # return 'INSERTED SUCCESS'
    return render_template('create.html')


# form to edit blog
@app.route("/blog/<int:id>/edit", methods=('GET', 'POST'))
def edit(id):
    edit_posts = get_post(id)
    print('edit posts', edit_posts)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('TITLE IS NEEDED')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE ID=?',(title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    return render_template('edit.html', posts=edit_posts)


# form to delete blog
@app.route("/blog/<int:id>/delete", methods=('POST',))
def delete(id):
    delete_posts = get_post(id)
    print('delete posts', delete_posts)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id, ))
    conn.commit()
    conn.close()
    flash ('"{}" was successfully deleted'.format(delete_posts[0]))
    return redirect(url_for('home'))


# portfolio page route
@app.route("/portfolio", methods=['GET', 'POST'])
def portfolio():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM portfolio').fetchall()
    print('portfolio', posts)
    conn.close()
    search = False
    limit = 4
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * limit
    end = page * limit if len(posts) > page * limit else len(posts)
    pagination = Pagination(page=page, total=len(posts), css_framework='foundation', search=search, record_name='posts', per_page=4)
    posts = posts[start: end]
    return render_template('portfolio.html', posts=posts, pagination=pagination)


@app.route("/portfolio_edit", methods=('GET', 'POST'))
def portfolio_edit():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        link = request.form['link']
        if not title:
            flash('TITLE IS NEEDED')
        else:
            if request.form['submit_button'] == 'editbtn':
                conn = get_db_connection()
                conn.execute('UPDATE portfolio SET title = ?, content = ?, link = ? WHERE title=?',(title, content, link, title))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))
            elif request.form['submit_button'] == 'deletebtn':
                conn = get_db_connection()
                conn.execute('DELETE FROM portfolio WHERE title = ?', (title, ))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))
    return render_template('portfolio_edit.html')


# form to fill portfolio details into table
@app.route("/portfolio-post", methods=('GET', 'POST'))
def portfolio_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        link = request.form['link']
        if not title:
            flash('TITLE IS NEEDED')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO portfolio (title, content, link) VALUES (?,?,?)',
                         (title, content,link))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    return render_template('portfolio-posts.html')


# contact me page route
@app.route("/contact")
def contact():
    return render_template('contact.html')


# route to receive user queries on email
@app.route("/send_email", methods=['POST'])
def send_email():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['inputEmail4']
        message = request.form['validationTextarea']
        print(first_name, last_name, email, message)

        my_name = 'Ishika Bhattacharya'
        my_email = 'bishika603@gmail.com'
        my_password = 'oldmonkrsk'

        # log in to the email account
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(my_email, my_password)

        sender_email = 'bishika603@gmail.com'
        receiver_email = 'bishika603@gmail.com'

        msg = EmailMessage()
        msg.set_content("First name: " + str(first_name) + "\nLast name: "+str(last_name) + "\nEmail: " + str(email) + "\nMessage: " +str(message))
        msg['Subject'] = "New Response on personal website from {}".format(email)
        msg['From'] = sender_email
        msg['To'] = receiver_email
        try:
            server.send_message(msg)
        except Exception as e:
            return e
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)
