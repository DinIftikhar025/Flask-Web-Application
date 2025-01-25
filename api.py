from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
        {'id': 1, 'name': 'Task 1', 'description': 'Description for Task 1'},
        {'id': 2, 'name': 'Task 2', 'description': 'Description for Task 2'},
        {'id': 3, 'name': 'Task 3', 'description': 'Description for Task 3'}
    ]
    
@app.route('/')
def home():
    return jsonify(message="Welcome to the Sample TODO List Application!")

## Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

## RETRIEVE A SPECIFIC ITEM BY ID  
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = next(filter(lambda x: x['id'] == id, items), None)
    if item is None:
        return jsonify(message="Item not found"), 404
    return jsonify(item)

## Post: Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if data is None:
        return jsonify(message="No input data provided"), 400
    
    new_item = {
        'id': len(items) + 1,
        'name': data['name'],
        'description': data['description']
    }
    items.append(new_item)
    return jsonify(new_item), 201

## Put: Update an existing item
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    if data is None:
        return jsonify(message="No input data provided"), 400
    
    item = next(filter(lambda x: x['id'] == id, items), None)
    if item is None:
        return jsonify(message="Item not found"), 404
    item['name'] = data.get('name', item['name'])
    item['description'] = data.get('description', item['description'])
    
    item.update(data)
    return jsonify(item)

## Delete: Delete an existing item
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    global items
    items = list(filter(lambda x: x['id'] != id, items))
    return jsonify(message="Item deleted successfully")



if __name__ == '__main__':
    app.run(debug=True)