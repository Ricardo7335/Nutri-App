from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/ejercicio')
def ejercicio():
    return render_template('ejercicio.html')

@app.route('/receta')
def receta():
    return render_template('receta.html')

@app.route('/ia')
def ia():
    return render_template('ia.html')

@app.route('/sesion')
def sesion():
    return render_template('sesion.html')

if __name__ == '__main__':
    app.run(debug=True)