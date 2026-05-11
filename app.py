from flask import Flask, render_template, request, jsonify
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()

prolog.consult("logic/easter_egg.pl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    data = request.json
    item = data.get('item')

    prolog.assertz(f"completado({item})")
    prolog.assertz(f"tiene({item})")

    guia = list(prolog.query("que_hacer(instruccion(X))"))
    mensaje = guia[0]['X'] if guia else "¡Easter Egg completado!"

    return jsonify({
        "status": "success",
        "siguiente_paso": mensaje
    })

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)