#importação
from flask import Flask

app = Flask(__name__)

#Definir rota raiz
@app.route('/')
def hello_world():
  return 'Hello World'

if __name__ == "__main__":
  app.run(debug=True)