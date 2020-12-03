from users import User
from books import Book
from recommender import *

#print values from DATABASE
'''
conn = sqlite3.connect("bookreviews.db")
cursor = conn.cursor()

cursor.execute('SELECT isbn FROM book LIMIT 10')
b = cursor.fetchall()
print(b)
'''

#book tests
'''
b = Book()
b.isbn_to_book('0155061224')
print(b.id)
print(b.isbn)
print(b.title)
print(b.author)
print(b.year)

b.id_to_book(225817)
print(b.id)
print(b.isbn)
print(b.title)
print(b.author)
print(b.year)

b.title_to_book('Carnival of the Spirit')
print(b.id)
print(b.isbn)
print(b.title)
print(b.author)
print(b.year)
'''

#user tests
'''
u = User()
u2 = User()
u3 = User()
u1 = u.makeUser(age= 34, rates = {'0195153448':3})
u1.addBooks(books = ['0195153448','0002005018','0060973129','0374157065','0393045218','0399135782','0425176428','0671870432','0679425608','074322678X'])
u1.addRates(rates =  {'0002005018':9,'0060973129':2,'0374157065':7,'0393045218':2,'0399135782':1,'0425176428':4,'0671870432':6,'0679425608':2,'074322678X':8})
print(u1.rates)
print(u1.books)
u1.recommend()
u1.deleteUser()

u2.getUser(2033)
print(u2.rates)

u3.getUser(254)
print(u3.books)

conn = sqlite3.connect("bookreviews.db")
cursor = conn.cursor()
cursor.execute('SELECT * FROM reviewImp WHERE user_id = 278854')
b = cursor.fetchall()
print(b)
'''

#recommender tests
user1 = User()
user1.getUser(11676)

rec = recommendbook(user1)

for i, (rate, isbn) in enumerate(rec):
    book = Book()
    book.isbn_to_book(isbn)
    print("{} {} (expected rating {:0.2f})".format(i+1, book.title, rate))
