#importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem 
#Produto (id, name, price, description)
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(120), nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.Text, nullable=True)

@app.route('/products/add', methods=["POST"])
def add_product():
  data = request.json
  if 'nome' in data and 'price' in data:
    product = Product(nome=data["nome"], price=data["price"], description=data.get("description", ""))
    db.session.add(product)
    db.session.commit()
    return jsonify({"message" : "Product added successfully"})
  return jsonify({"message": "Invalid product data"}), 400


@app.route('/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
  #Recuperar prod for database
  #verify is product exists
  #se sim deletar
  product = Product.query.get(product_id)
  if product:
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
  return jsonify ({"message": "Product not found"}), 404



@app.route('/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
  product = Product.query.get(product_id)
  if not product:
    return jsonify({"message": "Product not found"}), 404
  
  data = request.json
  if 'nome' in data:
    product.nome = data['nome']
  
  if "price" in data:
    product.price = data["price"]
  
  if 'description' in data:
    product.description = data['description']

  db.session.commit()
  return jsonify({'message': 'Product updated successfully'})

@app.route('/products/', methods=['GET'])
def get_products():
  products = Product.query.all()
  product_list =[]
  for product in products:
    product_data= {
      "id": product.id,
      "nome": product.nome,
      "price": product.price,
      "description": product.description
    }
    print(product)
    product_list.append(product_data)
  return jsonify(product_list)

@app.route('/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
  print("aqui vamos trazer os producto escolhido")
  product = Product.query.get(product_id)
  if product:
    return jsonify({
      "id": product.id,
      "nome": product.nome,
      "price": product.price,
      "description": product.description
    }), 200 
  return jsonify({"message": "Product not found"}), 404

#Definir rota raiz
@app.route('/')
def hello_world():
  return 'Hello World'

if __name__ == "__main__":
  app.run(debug=True)