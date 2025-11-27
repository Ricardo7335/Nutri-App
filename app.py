from flask import Flask, render_template, request, redirect, url_for, flash, session 
import requests 

app = Flask(__name__)
app.secret_key = 'vane_clave_segura_2025'

API_KEY = "sW5cNacxmey8KAmb8zwGF7Lv2lPfBTodv4ewa5dy"

@app.route('/')
def inicio():
    return render_template('inicio.html', usuario=session.get('usuario'))

@app.route('/recetas')
def recetas():
    return render_template('receta.html')

@app.route('/ejercicios')
def ejercicios():
    return render_template('ejercicio.html')

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

@app.route("/an")
def an():
    return render_template("analizador.html", resultado=None)

@app.route("/analizar", methods=["POST"])
def analizar():
    receta = request.form.get("receta")
    ingredientes = request.form.get("ingredientes").split(",")

    resultado = {
        "receta": receta,
        "ingredientes": [],
        "sin_gluten": True,
        "sin_lacteos": True,
        "es_vegetariana": True,
        "es_vegana": True
    }

    lacteos = ["leche", "queso", "yogur", "mantequilla"]
    gluten = ["pan", "trigo", "pasta", "harina"]
    carnes = ["pollo", "carne", "res", "cerdo", "pescado"]

    for ing in ingredientes:
        ing = ing.strip()
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={ing}&api_key={API_KEY}"
        r = requests.get(url)
        data = r.json()

        energia = "No encontrado"
        nombre = ing
        if "foods" in data and len(data["foods"]) > 0:
            food = data["foods"][0]
            nombre = food.get("description", ing)
            for n in food.get("foodNutrients", []):
                if n["nutrientName"] == "Energy":
                    energia = f"{n['value']} {n['unitName']}"
                    break

        resultado["ingredientes"].append({"nombre": nombre, "energia": energia})

    
        if any(l in ing.lower() for l in lacteos):
            resultado["sin_lacteos"] = False
            resultado["es_vegana"] = False
        if any(g in ing.lower() for g in gluten):
            resultado["sin_gluten"] = False
        if any(c in ing.lower() for c in carnes):
            resultado["es_vegetariana"] = False
            resultado["es_vegana"] = False

    return render_template("analizador.html", resultado=resultado)

RESPUESTAS = {
    "hola": "¡Hola! ¿Cómo estás?",
    "que ejercicios me recomiendas": "Puedes empezar con caminatas, sentadillas, abdominales y ejercicios de resistencia ligera.",
        "que alimentos puedo comer si soy vegetariana": "Frutas, verduras, legumbres, cereales integrales, frutos secos y lácteos si los consumes.",
    "que alimentos puedo comer si soy vegana": "Frutas, verduras, legumbres, cereales integrales, semillas y frutos secos, evitando productos animales.",
    "que alimentos puedo comer si soy omnivoro": "Puedes comer de todo: carnes, pescados, vegetales, frutas, cereales y lácteos, buscando equilibrio.",
    "que alimentos puedo comer si soy flexitariano": "Principalmente vegetales y legumbres, pero ocasionalmente carnes o pescados en pequeñas cantidades.",
    "que puedo hacer si quiero bajar de peso": "Mantén una dieta balanceada, controla las porciones y combina con ejercicio regular.",
    "que ejercicios para ganar musculo": "Entrenamiento de fuerza: pesas, flexiones, dominadas y una dieta rica en proteínas.",
    "para que sirven los planes nutricionales": "Sirven para organizar tu alimentación según tus objetivos y necesidades de salud.",
    "por que es importante empezar tu vida saludable desde hoy": "Porque cada hábito que inicias ahora mejora tu bienestar futuro y previene enfermedades."
}

@app.route("/ia", methods=["GET", "POST"])
def ia():
    if "chat" not in session:
        session["chat"] = [("IA", "¡Hola! ¿En qué puedo ayudarte hoy?")]

    if request.method == "POST":
        pregunta = request.form.get("pregunta", "").lower()
        respuesta = RESPUESTAS.get(pregunta, "Lo siento, solo puedo responder 5 preguntas predefinidas.")
        session["chat"].append(("Tú", pregunta))
        session["chat"].append(("IA", respuesta))

    return render_template("ia.html", chat=session["chat"])

if __name__=="__main__":
    app.run(debug=True)