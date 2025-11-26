from flask import Flask, render_template, request, redirect, url_for, flash, session 

app = Flask(__name__)
app.secret_key = 'vane_clave_segura_2025'

@app.route('/')
def inicio():
    return render_template('inicio.html', usuario=session.get('usuario'))

@app.route('/recetas')
def recetas():
    return render_template('receta.html')

@app.route('/ejercicios')
def ejercicios():
    return render_template('ejercicio.html')

@app.route('/ia')
def ia():
    return render_template('ia.html')

@app.route('/educacion')
def educacion():
    return render_template('educacion.html')


@app.route('/planificacion')
def planificacion():
    return render_template('planificacion.html')

@app.route('/sesion')
def sesion():
    return render_template('sesion.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        session['usuario'] = request.form['nombre']
        return redirect(url_for('inicio'))
    return render_template('sesion.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route("/imcc")
def imcc():
    return render_template("calculadora-IMC.html")

@app.route("/tbmm")
def tbmm():
    return render_template("calculadora-TBM.html")

@app.route("/gctt")
def gctt():
    return render_template("calculadora-GCT.html")

@app.route("/peso")
def peso():
    return render_template("calculadora-de-peso-ideal.html")

@app.route("/mn")
def mn():
    return render_template("macros.html")

@app.route("/an")
def an():
    return render_template("analizador.html")

@app.route('/imc', methods=['GET', 'POST'])
def imc():
    imc = None
    mensaje = ''
    if request.method == 'POST':
        altura = float(request.form['altura']) / 100
        peso = float(request.form['peso'])
        imc = round(peso / (altura * altura), 1)

        if imc < 18.5:
            mensaje = 'Bajo peso'
        elif imc < 25:
            mensaje = 'Peso saludable'
        elif imc < 30:
            mensaje = 'Sobrepeso'
        else:
            mensaje = 'Obesidad'

    return render_template('calculadora-IMC.html', imc=imc, mensaje=mensaje)

@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        try:
            sexo = request.form['sexo']
            edad = float(request.form['edad'])
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])

            if sexo == 'hombre':
                geb = 10 * peso + 6.25 * altura - 5 * edad + 5
            else:
                geb = 10 * peso + 6.25 * altura - 5 * edad - 161

            gct = round(geb * 1.5) 
            resultado = f"Tu Gasto Calórico Total estimado es {gct} kcal/día"
        except:
            resultado = "Hubo un error al procesar los datos. Verifica que todos los campos estén completos."

    return render_template('calculadora-GCT.html', resultado=resultado)

@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    resultado = None
    if request.method == 'POST':
        try:
            sexo = request.form['sexo']
            edad = float(request.form['edad'])
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])

            if sexo == 'hombre':
                tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
            else:
                tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

            resultado = f"Tu Tasa Metabólica Basal estimada es {round(tmb)} kcal/día"
        except:
            resultado = "Hubo un error al procesar los datos. Verifica que todos los campos estén completos."

    return render_template('calculadora-TBM.html', resultado=resultado)

@app.route('/peso_ideal', methods=['GET', 'POST'])
def peso_ideal():
    resultado = None
    if request.method == 'POST':
        sexo = request.form['sexo']
        altura = float(request.form['altura'])

        if sexo == 'hombre':
            base = 50
        else:
            base = 45.5

        if altura > 152:
            peso_ideal = base + 0.9 * (altura - 152)
        else:
            peso_ideal = base

        resultado = f"Tu peso corporal ideal estimado es {round(peso_ideal, 1)} kg"

    return render_template('calculadora-de-peso-ideal.html', resultado=resultado)

@app.route('/macros', methods=['GET', 'POST'])
def macros():
    resultado = None
    if request.method == 'POST':
        sexo = request.form['sexo']
        edad = float(request.form['edad'])
        altura = float(request.form['altura'])
        peso = float(request.form['peso'])
        actividad = float(request.form['actividad'])
        objetivo = request.form['objetivo']

        if sexo == 'hombre':
            tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

        gct = tmb * actividad

        if objetivo == 'mantener':
            calorias = gct
        elif objetivo == 'perder':
            calorias = gct * 0.85
        else: 
            calorias = gct * 1.15

        proteinas = peso * 2  
        grasas = (calorias * 0.25) / 9 
        carbos = (calorias - (proteinas * 4 + grasas * 9)) / 4 

        resultado = (
            f"Calorías: {round(calorias)} kcal/día"
            f"Proteínas: {round(proteinas)} g"
            f"Grasas: {round(grasas)} g"
            f"Carbohidratos: {round(carbos)} g"
        )

    return render_template('macros.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)