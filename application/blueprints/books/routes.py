


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


    