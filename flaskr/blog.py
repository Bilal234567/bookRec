#this is the blog Blueprint

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from users import User
from books import Book
from recommender import *


#without a url_prefix, each of these functions will have their own url
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()

    #find books for this user
    posts = db.execute(
        " SELECT title, author, rate FROM book b JOIN reviewExp r ON b.isbn = r.isbn WHERE r.user_id = ?", (g.user['tableid'], )).fetchall()

    #get this user, recommend books
    u = User()
    u.getUser(g.user['tableid'], db)
    rec = recommendbook(u, db)

    #construct list of recommended books
    bookList = []
    for i, (rate, isbn) in enumerate(rec):
        book = Book()
        book.isbn_to_book(isbn, db)
        bookinfo = {}
        bookinfo['title'] = book.title
        bookinfo['author'] = book.author
        bookinfo['rate'] = "{:0.2f}".format(rate)
        bookList.append(bookinfo)

    return render_template('blog/index.html', posts=posts, books=bookList)

@bp.route('/addbook', methods = ('GET', 'POST'))
@login_required
def addbooks():
    if request.method == 'POST':
        title = request.form['title']
        rate = request.form['rate']
        error = None

        if not title:
            title = 'No Title, can\'t save book'

        if not rate:
            error = "No rate, can\'t save book"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            b = Book()
            b.title_to_book(title, db)
            #handle book not found?

            u = User()
            u.getUser(g.user['tableid'], db)
            u.addRates({b.isbn: rate}, db)

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))