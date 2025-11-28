from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey
from datetime import date
from typing import List
\


app = Flask(__name__)
# Fixed: URL-encoded password ($ becomes %24), removed spaces from database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2733286Pj%24@localhost:3306/Library_Books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create a base class for our models
class Base(DeclarativeBase):
    pass
 
#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)

db.init_app(app) #adding our db extension to our app


loan_book = db.Table(
    'loan_book',
    Base.metadata,
    db.Column('loan_id', db.ForeignKey('loans.id')),
    db.Column('book_id', db.ForeignKey('books.id'))
)



class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    DOB: Mapped[date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    loans: Mapped[List['Loan']] = db.relationship(back_populates='member') #New relationship attribute




class Loan(Base):
    __tablename__ = 'loans'

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(Date, nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id'), nullable=False)


    member: Mapped['Member'] = db.relationship(back_populates='loans') #New relationship attribute
    books: Mapped[List['Book']] = db.relationship(secondary=loan_book, back_populates='loans')

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    loans: Mapped[List['Loan']] = db.relationship(secondary=loan_book, back_populates='books')



def add_new_member(name, email, dob_str, password):
    try:
        dob_object =date.fromisoformat(dob_str)

        new_member = Member (
            name = name,
            email = email,
            DOB = dob_object,
            password = password
          )

        # db.session.add(new_member)
        # db.session.commit()
        print( f"Member '{name}' successfully added.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding member: {e}")

         

def add_new_book(author,genre,desc,title):
    try:
        new_book = Book(
            author = author,
            genre = genre, 
            desc = desc,
            title = title
        )


        # db.session.add(new_book)
        # db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error adding book: {e}")


with app.app_context():
    # add_new_member("Alexa Nunes", "ALexa.nunes@email.com", "1993-09-04", "Password04")
    add_new_book(
        author = 'George Orwell',
        genre = 'Dystopian',
        desc = 'A novel about totalitarian surveillance',
        title = '1984'
    )

    db.create_all()
     


			
app.run(debug=True)