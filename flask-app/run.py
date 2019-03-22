from flask import Flask, render_template, redirect, jsonify, request
from pymongo import MongoClient
from classes import *

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('mongo:27017')
db = client.ProductManager

if db.settings.find({'name': 'product_id'}).count() <= 0:
    print("product_id Not found, creating....")
    db.settings.insert_one({'name': 'product_id', 'value': 0})


def updateProductID(value):
    product_id = db.settings.find_one()['value']
    product_id += value
    db.settings.update_one(
        {'name': 'product_id'},
        {'$set':
            {'value': product_id}
         })


def createProduct(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    product_id = db.settings.find_one()['value']

    product = {
        'id': product_id,
        'title': title,
        'shortdesc': shortdesc,
        'priority': priority}

    db.products.insert_one(product)
    updateProductID(1)
    return redirect('/')


def deleteProduct(form):
    key = form.key.data
    title = form.title.data

    if(key):
        print(key, type(key))
        db.products.delete_many({'id': int(key)})
    else:
        db.products.delete_many({'title': title})

    return redirect('/')


def updateProduct(form):
    key = form.key.data
    shortdesc = form.shortdesc.data

    db.products.update_one(
        {"id": int(key)},
        {"$set":
            {"shortdesc": shortdesc}
         }
    )

    return redirect('/')


def resetProduct(form):
    db.products.drop()
    db.settings.drop()
    db.settings.insert_one({'name': 'product_id', 'value': 0})
    return redirect('/')


@app.route('/products', methods=['GET'])
def get_all_products():
    products = db.products
    output = []
    for q in products.find():
        output.append({'id': q['id'],
                       'title': q['title'],
                       'shortdesc': q['shortdesc'],
                       'priority': q['priority']})

    return jsonify({'result': output})


@app.route('/product/<id>', methods=['GET'])
def get_one_product(id):
    products = db.products
    q = products.find_one({'id': int(id)})
    if q:
        output = {
            'id': q['id'],
            'title': q['title'],
            'shortdesc': q['shortdesc'],
            'priority': q['priority']}
    else:
        output = 'No results found'
    return jsonify({'result': output})


@app.route('/product', methods=['POST'])
def add_products():
    products = db.products

    title = request.json['title']
    product_id = db.settings.find_one()['value']
    shortdesc = request.json['shortdesc']
    priority = request.json['priority']
    product = {
        'id': product_id,
        'title': title,
        'shortdesc': shortdesc,
        'priority': priority}
    new_product = products.insert_one(product)
    updateProductID(1)
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    cform = CreateProduct(prefix='cform')
    dform = DeleteProduct(prefix='dform')
    uform = UpdateProduct(prefix='uform')
    reset = ResetProduct(prefix='reset')

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createProduct(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteProduct(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateProduct(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetProduct(reset)

    # read all data
    docs = db.products.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template('home.html', cform=cform, dform=dform, uform=uform,
                           data=data, reset=reset)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
