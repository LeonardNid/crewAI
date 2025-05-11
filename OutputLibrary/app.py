from flask import Flask, request, jsonify
from models import db, Book, Member, Loan

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Small Public Library Management API running'})

# List all books or add a new book
@app.route('/books', methods=['GET', 'POST'])
def books(): 
    if request.method == 'GET':
        objs = Book.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        data = request.get_json()
        new_obj = Book(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a specific book by id
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def books_int_id(id): 
    if request.method == 'GET':
        obj = Book.query.get(id)
        if not obj:
            return jsonify({"message": "Book not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        obj = Book.query.get(id)
        if not obj:
            return jsonify({"message": "Book not found"}), 404
        data = request.get_json()
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Book.query.get(id)
        if not obj:
            return jsonify({"message": "Book not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Book deleted"})

# Search books by title
@app.route('/books/title/<string:title>', methods=['GET'])
def books_title_string_title(title):
    objs = Book.query.filter_by(**{"title": title}).all()
    if not objs or len(objs) == 0:
        return jsonify({"message": "Book not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# Search books by author
@app.route('/books/author/<string:author>', methods=['GET'])
def books_author_string_author(author):
    objs = Book.query.filter_by(**{"author": author}).all()
    if not objs or len(objs) == 0:
        return jsonify({"message": "Book not found"}), 404
    return jsonify([o.to_dict() for o in objs])

# List all members or add a new member
@app.route('/members', methods=['GET', 'POST'])
def members(): 
    if request.method == 'GET':
        objs = Member.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import date

        data = request.get_json()
        if 'membership_expiry_date' in data:
            data['membership_expiry_date'] = date.fromisoformat(data['membership_expiry_date'])
        new_obj = Member(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update or delete a specific member by id
@app.route('/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def members_int_id(id): 
    if request.method == 'GET':
        obj = Member.query.get(id)
        if not obj:
            return jsonify({"message": "Member not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        from datetime import date
        obj = Member.query.get(id)
        if not obj:
            return jsonify({"message": "Member not found"}), 404
        data = request.get_json()
        if 'membership_expiry_date' in data:
            data['membership_expiry_date'] = date.fromisoformat(data['membership_expiry_date'])
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Member.query.get(id)
        if not obj:
            return jsonify({"message": "Member not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Member deleted"})

# List all loans or create a new loan (borrow a book)
@app.route('/loans', methods=['GET', 'POST'])
def loans(): 
    if request.method == 'GET':
        objs = Loan.query.all()
        return jsonify([o.to_dict() for o in objs])
    elif request.method == 'POST':
        from datetime import date

        data = request.get_json()
        if 'checkout_date' in data:
            data['checkout_date'] = date.fromisoformat(data['checkout_date'])
        if 'due_date' in data:
            data['due_date'] = date.fromisoformat(data['due_date'])
        new_obj = Loan(**data)
        db.session.add(new_obj)
        db.session.commit()
        return jsonify(new_obj.to_dict()), 201

# Retrieve, update (return book) or delete a specific loan by id
@app.route('/loans/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def loans_int_id(id): 
    if request.method == 'GET':
        obj = Loan.query.get(id)
        if not obj:
            return jsonify({"message": "Loan not found"}), 404
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        from datetime import date
        obj = Loan.query.get(id)
        if not obj:
            return jsonify({"message": "Loan not found"}), 404
        data = request.get_json()
        if 'checkout_date' in data:
            data['checkout_date'] = date.fromisoformat(data['checkout_date'])
        if 'due_date' in data:
            data['due_date'] = date.fromisoformat(data['due_date'])
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return jsonify(obj.to_dict())
    elif request.method == 'DELETE':
        obj = Loan.query.get(id)
        if not obj:
            return jsonify({"message": "Loan not found"}), 404
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"message": "Loan deleted"})

# List all overdue loans
@app.route('/loans/overdue', methods=['GET'])
def loans_overdue():
    from datetime import date
    objs = Loan.query.filter(Loan.due_date < date.today(), Loan.returned_flag == False).all()
    return jsonify([o.to_dict() for o in objs])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)