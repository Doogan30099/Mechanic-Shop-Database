from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey, select
from datetime import date
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

app = Flask(__name__)
# Fixed: URL-encoded password ($ becomes %24), removed spaces from database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2733286Pj%24@localhost:3306/Library_Books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Create a base class for our models
class Base(DeclarativeBase):
    pass
 
#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)
ma = Marshmallow()



db.init_app(app) #adding our db extension to our app
ma.init_app(app)

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



# -------------schemas--------------
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route("/members", methods=['POST'])
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    


    query = select(Member).where(Member.email == member_data['email'])
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201


#GET ALL MEMBERS
@app.route("/members", methods=['GET'])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members)

#GET SPECIFIC MEMBER
@app.route("/members/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    if member:
        return member_schema.jsonify(member), 200
    return jsonify({"error": "Member not found."}), 404


#UPDATE SPECIFIC USER
@app.route("/members/<int:member_id>", methods=['PUT'])
def update_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member), 200


#DELETE SPECIFIC MEMBER
@app.route("/members/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f'Member id: {member_id}, successfully deleted.'}), 200

@app.route("/books", methods=["POST"])
def create_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    
    query = select(Book).where(Book.title == book_data['title'])
    existing_book = db.session.execute(query).scalars().all()
    if existing_book:
        return jsonify({"error": "Book already exists."}), 400
    
    new_book = Book(**book_data)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book), 201


    

with app.app_context():
    # add_new_member("Alexa Nunes", "ALexa.nunes@email.com", "1993-09-04", "Password04")
    # add_new_book(
    #     author = 'George Orwell',
    #     genre = 'Dystopian',
    #     desc = 'A novel about totalitarian surveillance',
    #     title = '1984'
    # )

    db.create_all()
     



			
app.run(debug=True)