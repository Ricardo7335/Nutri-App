from flask import Flask, render_template, request, redirect, url_for, flash, session 
import requests 

app = Flask(__name__)
app.secret_key = 'vane_clave_segura_2025'

API_KEY = "sW5cNacxmey8KAmb8zwGF7Lv2lPfBTodv4ewa5dy"

@app.route('/')
def inicio():
    return render_template('inicio.html', usuario=session.get('usuario'))

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

recetas = [
    {"nombre": "Filete a la plancha", "nivel": "principiante", "tipo": "omnivoro",
     "link": "https://www.recetasgratis.net/receta-de-filete-de-ternera-a-la-plancha-64377.html",
     "imagen": "static/img/filete.jpg"},
    {"nombre": "Pollo al curry", "nivel": "intermedio", "tipo": "omnivoro",
     "link": "https://www.recetasgratis.net/receta-de-pollo-al-curry-facil-64384.html",
     "imagen": "static/img/pollo.jpg"},
    {"nombre": "Costillas al horno", "nivel": "chef", "tipo": "omnivoro",
     "link": "https://www.recetasgratis.net/receta-de-costillas-de-cerdo-al-horno-64382.html",
     "imagen": "static/img/costillas.jpg"},

    {"nombre": "Bowl de quinoa y vegetales", "nivel": "principiante", "tipo": "vegetariano",
     "link": "https://www.recetasgratis.net/receta-de-ensalada-de-quinoa-con-verduras-64381.html",
     "imagen": "static/img/bowl.jpg"},
    {"nombre": "Hamburguesa de lentejas", "nivel": "intermedio", "tipo": "vegetariano",
     "link": "https://www.recetasgratis.net/receta-de-hamburguesa-de-lentejas-64380.html",
     "imagen": "static/img/hamburguesa.jpg"},
    {"nombre": "Pasta con pesto de espinaca", "nivel": "chef", "tipo": "vegetariano",
     "link": "https://www.recetasgratis.net/receta-de-pasta-con-pesto-de-espinacas-64379.html",
     "imagen": "static/img/pasta.jpg"},

    {"nombre": "Crema de calabaza", "nivel": "principiante", "tipo": "vegano",
     "link": "https://www.recetasgratis.net/receta-de-crema-de-calabaza-64378.html",
     "imagen": "static/img/crema.jpg"},
    {"nombre": "Tostadas con aguacate", "nivel": "principiante", "tipo": "vegano",
     "link": "https://danzadefogones.com/tostadas-de-aguacate/",
     "imagen": "static/img/tostadas.jpg"},
    {"nombre": "Ensalada de garbanzos", "nivel": "intermedio", "tipo": "vegano",
     "link": "https://comedera.com/receta-ensalada-de-garbanzos/",
     "imagen": "static/img/garbanzos.jpg"},

    {"nombre": "Arroz con verduras", "nivel": "principiante", "tipo": "flexitariano",
     "link": "https://recetasdecocina.elmundo.es/2021/06/arroz-con-verduras-receta-sana.html",
     "imagen": "static/img/arroz.jpg"},
    {"nombre": "Tortilla de papa", "nivel": "intermedio", "tipo": "vegetariano",
     "link": "https://www.paulinacocina.net/tortilla-de-papas-espanola/10476",
     "imagen": "static/img/tortilla.jpg"},
    {"nombre": "Fajitas de pollo sin tortilla", "nivel": "chef", "tipo": "omnivoro",
     "link": "https://www.tengounhornoysecomousarlo.com/2012/05/fajitas-de-pollo-sin-tortilla.html?m=1",
     "imagen": "static/img/fajitas.jpg"},

    {"nombre": "Batido de proteína natural", "nivel": "principiante", "tipo": "flexitariano",
     "link": "https://www.mundodeportivo.com/uncomo/deporte/articulo/6-batidos-de-proteinas-caseros-para-aumentar-masa-muscular-45400.html",
     "imagen": "static/img/batido.jpg"},
    {"nombre": "Huevos revueltos con espinaca", "nivel": "intermedio", "tipo": "omnivoro",
     "link": "https://www.recetasgratis.net/receta-de-revuelto-de-espinacas-con-huevo-64796.html",
     "imagen": "static/img/espinacas.jpg"},
    {"nombre": "Pasta integral con pollo", "nivel": "chef", "tipo": "omnivoro",
     "link": "https://easyrecetas.com/receta/pasta-integral-con-pollo/",
     "imagen": "static/img/pasta-integral.jpg"}
]


@app.route("/rc", methods=["GET"])
def recetas_view():
    nivel = request.args.get("nivel")
    tipo = request.args.get("tipo")

    filtradas = recetas
    if nivel and nivel != "":
        filtradas = [r for r in filtradas if r["nivel"] == nivel]
    if tipo and tipo != "":
        filtradas = [r for r in filtradas if r["tipo"] == tipo]

    return render_template("receta.html", recetas=filtradas)

ejercicios = [
    {"nombre": "Sentadillas", "descripcion": "3 series de 15 repeticiones",
     "imagen": "static/img/sentadilla.webp", "link": "https://www.youtube.com/watch?v=aclHkVaku9U", "objetivo": "ganar"},
    {"nombre": "Plancha", "descripcion": "3 series de 30 segundos",
     "imagen": "static/img/plancha.webp", "link": "https://www.youtube.com/watch?v=pSHjTRCQxIw", "objetivo": "bajar"},
    {"nombre": "Abdominales bicicleta", "descripcion": "3 series de 20 repeticiones",
     "imagen": "static/img/abdominales.webp", "link": "https://www.youtube.com/watch?v=9FGilxCbdz8", "objetivo": "bajar"},
    {"nombre": "Puente de glúteos", "descripcion": "3 series de 20 repeticiones",
     "imagen": "static/img/gluteos.webp", "link": "https://www.youtube.com/watch?v=1f8yoFFdkcY", "objetivo": "ganar"},
    {"nombre": "Jumping Jacks", "descripcion": "3 series de 1 minuto",
     "imagen": "static/img/jumping.webp", "link": "https://www.youtube.com/watch?v=c4DAnQ6DtF8", "objetivo": "bajar"},
    {"nombre": "Zancadas", "descripcion": "3 series de 12 por pierna",
     "imagen": "static/img/zancadas.webp", "link": "https://www.youtube.com/watch?v=wrwwXE_x-pQ", "objetivo": "ganar"},
    {"nombre": "Crunch clásico", "descripcion": "3 series de 20 repeticiones",
     "imagen": "static/img/crunch.webp", "link": "https://www.youtube.com/watch?v=Xyd_fa5zoEU", "objetivo": "bajar"},
    {"nombre": "Elevación de piernas", "descripcion": "3 series de 15 repeticiones",
     "imagen": "static/img/elevacion.webp", "link": "https://www.youtube.com/watch?v=JB2oyawG9KI", "objetivo": "bajar"},
    {"nombre": "Russian twists", "descripcion": "3 series de 20 giros",
     "imagen": "static/img/russian.webp", "link": "https://www.youtube.com/watch?v=wkD8rjkodUI", "objetivo": "bajar"},
    {"nombre": "Correr", "descripcion": "20 minutos",
     "imagen": "static/img/correr.webp", "link": "https://www.youtube.com/watch?v=Qd4x8xJzK0g", "objetivo": "bajar"},
    {"nombre": "Piernas + Cardio", "descripcion": "1–3 series según tu nivel",
     "imagen": "static/img/cardio.webp", "link": "https://www.youtube.com/watch?v=ml6cT4AZdqI", "objetivo": "bajar"},
    {"nombre": "Flexiones", "descripcion": "3 series de 10–15 repeticiones",
     "imagen": "static/img/flexion.jpg", "link": "https://www.youtube.com/watch?v=IODxDxX7oi4", "objetivo": "ganar"},
    {"nombre": "Escaladores", "descripcion": "3 series de 30 segundos",
     "imagen": "static/img/escaladores.webp", "link": "https://www.youtube.com/watch?v=nmwgirgXLYM", "objetivo": "bajar"},
    {"nombre": "Plancha con toque de hombros", "descripcion": "3 series de 30 segundos",
     "imagen": "static/img/hombros.webp", "link": "https://www.youtube.com/watch?v=DJQGX2J4IVw", "objetivo": "bajar"},
    {"nombre": "Sentadilla con salto", "descripcion": "3 series de 12 repeticiones",
     "imagen": "static/img/salto.webp", "link": "https://www.youtube.com/watch?v=U3HlEF_E9fo", "objetivo": "ganar"},
    {"nombre": "Fondos de tríceps", "descripcion": "3 series de 15 repeticiones",
     "imagen": "static/img/triceps.webp", "link": "https://www.youtube.com/watch?v=0326dy_-CzM", "objetivo": "ganar"},
    {"nombre": "Superman", "descripcion": "3 series de 30 segundos",
     "imagen": "static/img/superman.webp", "link": "https://www.youtube.com/watch?v=z6PJ6Zk8y8g", "objetivo": "ganar"},
    {"nombre": "Crunch en V", "descripcion": "3 series de 15 repeticiones",
     "imagen": "static/img/crunch-v.webp", "link": "https://www.youtube.com/watch?v=WSu-wci9uTo", "objetivo": "ganar"}
]

@app.route("/ejercicio", methods=["GET"])
def ejercicio_view():
    objetivo = request.args.get("objetivo")

    filtrados = ejercicios
    if objetivo and objetivo != "":
        filtrados = [e for e in filtrados if e["objetivo"] == objetivo]

    return render_template("ejercicio.html", ejercicios=filtrados)

if __name__ == "__main__":
    app.run(debug=True)
