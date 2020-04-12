from flask import Flask
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/umuzi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)


# Computer Class/Model
class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hard_drive_type = db.Column(db.String(100))
    processor = db.Column(db.String(100))
    amount_of_ram = db.Column(db.String(100))
    maximum_ram = db.Column(db.String(100))
    hard_drive_space = db.Column(db.String(100))
    form_factor = db.Column(db.String(100))

    def __init__(self, hard_drive_type, processor, amount_of_ram, maximum_ram, hard_drive_space, form_factor):
        self.hard_drive_type = hard_drive_type
        self.processor = processor
        self.amount_of_ram = amount_of_ram
        self.maximum_ram = maximum_ram
        self.hard_drive_space = hard_drive_space
        self.form_factor = form_factor


# Computer Schema
class ComputerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'hard_drive_type', 'processor', 'amount_of_ram',
                  'maximum_ram', 'hard_drive_space', 'form_factor')


# Init Schema
computer_schema = ComputerSchema()
computers_schema = ComputerSchema(many=True)

# Create a Computer
@app.route('/computer', methods=['POST'])
def add_computer():
    hard_drive_type = request.json['hard_drive_type']
    processor = request.json['processor']
    amount_of_ram = request.json['amount_of_ram']
    maximum_ram = request.json['maximum_ram']
    hard_drive_space = request.json['hard_drive_space']
    form_factor = request.json['form_factor']

    new_computer = Computer(hard_drive_type, processor,
                            amount_of_ram, maximum_ram, hard_drive_space, form_factor)

    db.session.add(new_computer)
    db.session.commit()

    return computer_schema.jsonify(new_computer)

# Get All Computers
@app.route('/computer', methods=['GET'])
def get_computers():
    all_computers = Computer.query.all()
    result = computers_schema.dump(all_computers)
    return jsonify(result)

# GET single computer
@app.route('/computer/<id>', methods=['GET'])
def get_product(id):
    computer = Computer.query.get(id)
    return computer_schema.jsonify(computer)

# Update a computer
@app.route('/computer/<id>', methods=['PUT'])
def update_computer(id):
    computer = Computer.query.get(id)

    hard_drive_type = request.json['hard_drive_type']
    processor = request.json['processor']
    amount_of_ram = request.json['amount_of_ram']
    maximum_ram = request.json['maximum_ram']
    hard_drive_space = request.json['hard_drive_space']
    form_factor = request.json['form_factor']

    computer.hard_drive_type = hard_drive_type
    computer.processor = processor
    computer.amount_of_ram = amount_of_ram
    computer.maximum_ram = maximum_ram
    computer.hard_drive_space = hard_drive_space
    computer.form_factor = form_factor

    db.session.commit()

    return computer_schema.jsonify(computer)

# Delete Computer
@app.route('/computer/<id>', methods=['DELETE'])
def delete_computer(id):
    computer = Computer.query.get(id)
    db.session.delete(computer)
    db.session.commit()

    return computer_schema.jsonify(computer)


# Run Server
if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
