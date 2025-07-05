from flask import Flask, jsonify, render_template, url_for
import mysql.connector
from flask import request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv() #Permite usar variabales de conexion a la base de datos de forma mas segura en produccion y test 

app = Flask(__name__, template_folder='Menus', static_folder='static')

app.secret_key = 'clave_secreta_segura'  # Usa una más segura en producción



# ------------------ FUNCIONES DE CONEXIÓN ------------------

CORS(app)

def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    

def obtener_maestros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()     
    cursor.execute("SELECT nombreMaestro FROM maestros ORDER BY nombreMaestro ASC")
    maestros = cursor.fetchall()
    conexion.close()
    return [fila[0] for fila in maestros]

def obtener_resenas_maestro(nombre_maestro): 
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    consulta = """
    SELECT r.comentario, r.calificacion, u.NomUsuario, m.nombreMateria
    FROM reseñas r
    JOIN usuarios u ON r.idUsuario = u.idUsuario
    JOIN maestro_materia mm ON r.idMaestro_Materia = mm.idMaestro_Materia
    JOIN maestros ma ON mm.idMaestro = ma.idMaestro
    JOIN materias m ON mm.idMateria = m.idMateria
    WHERE ma.nombreMaestro = %s
    """
    cursor.execute(consulta, (nombre_maestro,))
    resultados = cursor.fetchall()
    conexion.close()
    
    return resultados

def obtener_nombre_materia(idMateria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombreMateria FROM materias WHERE idMateria = %s", (idMateria,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado[0] if resultado else "Materia desconocida"

def obtener_materias():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT idMateria, nombreMateria FROM materias ORDER BY nombreMateria ASC")
    materias = cursor.fetchall()
    conexion.close()
    return materias

    

# ------------------ RUTAS ------------------

@app.route('/maestro/<nombre>')
def ver_resenas_maestro(nombre):
    resenas = obtener_resenas_maestro(nombre)
    return render_template('resenasMaestro.html', nombre=nombre, resenas=resenas)

@app.route("/")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.comentario, r.calificacion, r.fecha,
            u.NomUsuario,
            m.nombreMateria,
            ma.nombreMaestro
        FROM reseñas r
        JOIN usuarios u ON r.idUsuario = u.idUsuario
        JOIN maestro_materia mm ON r.idMaestro_Materia = mm.idMaestro_Materia
        JOIN materias m ON mm.idMateria = m.idMateria
        JOIN maestros ma ON mm.idMaestro = ma.idMaestro
        ORDER BY r.fecha DESC
    """)
    
    resenas = cursor.fetchall()
    cursor.close()
    conexion.close()

    if 'rol' in session:
        if session['rol'] == 'Administrador':
            return render_template("inicio.html", resenas=resenas)  # Aquí sin "Menus/"
        elif session['rol'] == 'Estudiante':
            return render_template("inicio.html", resenas=resenas)

    return render_template("inicio.html", resenas=resenas)


@app.route('/agregar_peticion', methods=['GET'])
def agregar_peticion():
    return render_template('agregarPeticion.html')


@app.route('/materias')
def mostrar_materias():
    materias = obtener_materias()
    return render_template('menuMateria.html', materias=materias)

@app.route('/maestros')
def mostrar_maestros():
    maestros = obtener_maestros()
    return render_template('menuMaestro.html', maestros=maestros)

@app.route('/login')
def inicio_sesion():
    return render_template('inicioSesion.html')

@app.route('/materia/<int:idMateria>')
def reseñas_por_materia(idMateria):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
    SELECT r.comentario, r.calificacion, u.NomUsuario, m.nombreMaestro
    FROM reseñas r
    JOIN maestro_materia mm ON r.idMaestro_Materia = mm.idMaestro_Materia
    JOIN maestros m ON mm.idMaestro = m.idMaestro
    JOIN usuarios u ON r.idUsuario = u.idUsuario
    WHERE mm.idMateria = %s
    """
    cursor.execute(query, (idMateria,))
    reseñas = cursor.fetchall()
    conexion.close()
    
    nombre_materia = obtener_nombre_materia(idMateria)

    return render_template('resenasMaterias.html', reseñas=reseñas, nombre_materia=nombre_materia)

@app.route('/test-template')
def test_template():
    try:
        return render_template('resenasMaterias.html', reseñas=[], nombre_materia="Prueba")
    except Exception as e:
        return f"Error cargando template: {str(e)}"

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.idUsuario, u.NomUsuario, u.contraseña, r.NomRol 
        FROM usuarios u 
        JOIN Roles r ON u.idRol = r.idRol 
        WHERE u.NomUsuario = %s
    """, (username,))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario and check_password_hash(usuario['contraseña'], password):
        session['usuario'] = usuario['NomUsuario']
        session['idUsuario'] = usuario['idUsuario']  # ✅ Aquí lo agregas
        session['rol'] = usuario['NomRol']
        if usuario['NomRol'] == 'Administrador':
            return redirect('/')
        else:
            return redirect('/')
    else:
        flash("Usuario o contraseña incorrectos")
        return redirect('/login')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash("Las contraseñas no coinciden.")
        return redirect('/login')

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(buffered=True)  

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE NomUsuario = %s", (username,))
        if cursor.fetchone():
            flash("El nombre de usuario ya existe.")
            conexion.close()
            return redirect('/login')

        # Obtener el idRol del Estudiante
        cursor.execute("SELECT idRol FROM Roles WHERE NomRol = 'Estudiante'")
        id_rol = cursor.fetchone()
        if not id_rol:
            flash("No existe el rol Estudiante en la base de datos.")
            conexion.close()
            return redirect('/login')

        # Insertar nuevo usuario
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (NomUsuario, contraseña, idRol) VALUES (%s, %s, %s)",
            (username, hashed_password, id_rol[0])
        )
        conexion.commit()
        flash("Registro exitoso, ahora puedes iniciar sesión.")
        return redirect('/login')

    except Exception as e:
        flash(f"Error en el registro: {str(e)}")
        return redirect('/login')
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

@app.route('/agregarAdmi')
def agregar_admi():
    return render_template('agregarAdmi.html')

# ------------------ RUTA INICIAL pag reseñas ------------------
@app.route('/agregar-resena')
def agregar_resena():
    materias = obtener_materias()
    return render_template('agregarRes.html', materias=materias)



# ------------------ RUTA PARA OBTENER MAESTROS pag reseñas ------------------
@app.route('/obtener-maestros/<int:id_materia>')
def obtener_maestros_por_materia(id_materia):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
    SELECT m.idMaestro, m.nombreMaestro
    FROM maestro_materia mm
    JOIN maestros m ON mm.idMaestro = m.idMaestro
    WHERE mm.idMateria = %s
    """
    cursor.execute(query, (id_materia,))
    maestros = cursor.fetchall()
    conexion.close()
    
    return {'maestros': maestros}

# ------------------ RUTA PARA AGREGAR PETICION para Usuarios ------------------
@app.route('/guardar_peticion', methods=['POST'])
def guardar_peticion():
    if 'idUsuario' not in session:
        return redirect(url_for('inicio_sesion'))

    nombre_maestro = request.form['nombre_maestro']
    nombre_materia = request.form['nombre_materia']
    mensaje = request.form.get('mensaje', '')
    id_usuario = session['idUsuario']

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO peticiones (nombreMaestro, nombreMateria, mensaje, idUsuario)
        VALUES (%s, %s, %s, %s)
    """, (nombre_maestro, nombre_materia, mensaje, id_usuario))

    conexion.commit()
    conexion.close()

    return render_template('agregarPeticion.html')  # regresa a la misma página

# ------------------ RUTA PARA AGREGAR RESEÑA pag reseñas ------------------
@app.route('/guardar-resena', methods=['POST'])
def guardar_resena():
    if 'usuario' not in session:
        flash("Debes iniciar sesión para agregar una reseña.")
        return redirect('/login')

    comentario = request.form['comentario']
    calificacion = int(request.form['calificacion'])
    id_maestro = int(request.form['maestro'])
    id_materia = int(request.form['materia'])
    id_usuario = session['usuario']

    # Obtener idMaestro_Materia
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT idMaestro_Materia FROM maestro_materia
        WHERE idMaestro = %s AND idMateria = %s
    """, (id_maestro, id_materia))
    resultado = cursor.fetchone()

    if not resultado:
        flash("No se encontró relación maestro-materia.")
        conexion.close()
        return redirect('/agregar-resena')

    id_maestro_materia = resultado[0]

    cursor.execute("""
        INSERT INTO reseñas (comentario, calificacion, idUsuario, idMaestro_Materia)
        VALUES (%s, %s, %s, %s)
    """, (comentario, calificacion, session['idUsuario'], id_maestro_materia))
    conexion.commit()
    conexion.close()
    flash("¡Reseña guardada con éxito!")
    return redirect('/')

# ------------------ LIKES Y DISLIKES ------------------
@app.route('/votar', methods=['POST'])
def votar():
    # Validar que el usuario haya iniciado sesión
    if 'idUsuario' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión'})

    data = request.get_json()
    tipo = data.get('tipo')       # 'like' o 'dislike'
    id_resena = data.get('idResena')
    id_usuario = session['idUsuario']

    # Validar datos recibidos
    if tipo not in ['like', 'dislike'] or not id_resena:
        return jsonify({'success': False, 'message': 'Datos inválidos'})

    try:  
        with conn.cursor() as cursor:
            # Obtener el idTipo correspondiente al nombre (like/dislike)
            cursor.execute("SELECT idTipo FROM tipo_reaccion WHERE nombre = %s", (tipo,))
            tipo_row = cursor.fetchone()

            if not tipo_row:
                return jsonify({'success': False, 'message': 'Tipo inválido'})

            id_tipo = tipo_row['idTipo']

            # Insertar o actualizar la reacción (ON DUPLICATE KEY UPDATE)
            cursor.execute("""
                INSERT INTO reacciones (idUsuario, idResena, idTipo)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE idTipo = VALUES(idTipo)
            """, (id_usuario, id_resena, id_tipo))
            conn.commit()

            # Consultar el conteo actualizado de likes y dislikes para la reseña
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN idTipo = 1 THEN 1 ELSE 0 END) AS likes,
                    SUM(CASE WHEN idTipo = 2 THEN 1 ELSE 0 END) AS dislikes
                FROM reacciones
                WHERE idResena = %s
            """, (id_resena,))
            resultados = cursor.fetchone()

        return jsonify({
            'success': True,
            'likes': resultados['likes'] or 0,
            'dislikes': resultados['dislikes'] or 0
        })

    except Exception as e:
        print("Error en /votar:", e)
        return jsonify({'success': False, 'message': 'Error en el servidor'})
    
    

# ------------------ CRUD DE MATERIAS ------------------

@app.route('/admin/materias')
def crud_materias():
    if 'rol' not in session or session['rol'] != 'Administrador':
        flash("Acceso denegado.")
        return redirect('/')

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT idMateria, nombreMateria FROM materias ORDER BY nombreMateria ASC")
    materias = cursor.fetchall()
    conexion.close()
    return render_template('crudMaterias.html', materias=materias)

@app.route('/admin/materias/agregar', methods=['POST'])
def agregar_materia():
    if 'rol' not in session or session['rol'] != 'Administrador':
        flash("Acceso denegado.")
        return redirect('/')

    nombre = request.form['nombreMateria']
    if not nombre.strip():
        flash("El nombre de la materia no puede estar vacío.")
        return redirect('/admin/materias')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO materias (nombreMateria) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()
    flash("Materia agregada correctamente.")
    return redirect('/admin/materias')

@app.route('/admin/materias/eliminar/<int:idMateria>', methods=['POST'])
def eliminar_materia(idMateria):
    if 'rol' not in session or session['rol'] != 'Administrador':
        flash("Acceso denegado.")
        return redirect('/')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM materias WHERE idMateria = %s", (idMateria,))
    conexion.commit()
    conexion.close()
    flash("Materia eliminada correctamente.")
    return redirect('/admin/materias')

@app.route('/admin/materias/editar/<int:idMateria>', methods=['POST'])
def editar_materia(idMateria):
    if 'rol' not in session or session['rol'] != 'Administrador':
        flash("Acceso denegado.")
        return redirect('/')

    nuevo_nombre = request.form['nuevoNombre']
    if not nuevo_nombre.strip():
        flash("El nuevo nombre no puede estar vacío.")
        return redirect('/admin/materias')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE materias SET nombreMateria = %s WHERE idMateria = %s", (nuevo_nombre, idMateria))
    conexion.commit()
    conexion.close()
    flash("Nombre de la materia actualizado.")
    return redirect('/admin/materias')

@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    if 'idUsuario' not in session:
        return jsonify({'error': 'no autorizado'}), 403

    user_id = session['idUsuario']

    # Verifica si ya reaccionó
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM reacciones WHERE idUsuario=%s AND idReseña=%s",
        (user_id, id)
    )
    reaccion = cursor.fetchone()

    if reaccion:
        conexion.close()
        return jsonify({'message': 'ya reaccionaste'}), 400

    # Insertar like
    cursor.execute(
        "INSERT INTO reacciones (idUsuario, idReseña, idTipo) VALUES (%s, %s, 1)",
        (user_id, id)
    )
    conexion.commit()
    conexion.close()
    return jsonify({'message': 'like registrado'})

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Its_131406136',
    database='PagWeb'
)
cursor = conexion.cursor()

# ------------------ FUNCION PARA AGREGAR ADMINISTRADORES ------------------
@app.route('/agregar_admin', methods=['GET', 'POST'])
def agregar_admin():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('❌ Las contraseñas no coinciden.')
        else:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE NomUsuario = %s", (usuario,))
            if cursor.fetchone():
                flash('⚠️ Este nombre de usuario ya está registrado.')
            else:
                # Obtener idRol del rol 'Administrador'
                cursor.execute("SELECT idRol FROM Roles WHERE NomRol = 'Administrador'")
                id_rol = cursor.fetchone()
                if id_rol:
                    hashed_password = generate_password_hash(password)
                    # Insertar nuevo administrador
                    cursor.execute("""
                        INSERT INTO usuarios (NomUsuario, contraseña, idRol)
                        VALUES (%s, %s, %s)
                    """, (usuario, hashed_password, id_rol['idRol']))
                    conexion.commit()
                    flash('✅ Administrador agregado exitosamente.')
                else:
                    flash("❌ No se encontró el rol 'Administrador'.")

    # Consultar todos los administradores para mostrar en la lista
    try:
        cursor.execute("""
            SELECT usuarios.idUsuario, usuarios.NomUsuario
            FROM usuarios
            INNER JOIN Roles ON usuarios.idRol = Roles.idRol
            WHERE Roles.NomRol = 'Administrador'
            ORDER BY usuarios.NomUsuario ASC
        """)
        administradores = cursor.fetchall()
    except Exception as e:
        administradores = []
        flash(f"⚠️ Error al obtener administradores: {str(e)}")

    conexion.close()
    return render_template('agregarAdmi.html', administradores=administradores)

@app.route('/eliminar_admin/<int:id>', methods=['POST'])
def eliminar_admin(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE idUsuario = %s", (id,))
        conexion.commit()
        flash("✅ Administrador eliminado correctamente.")
    except Exception as e:
        conexion.rollback()
        flash(f"❌ Error al eliminar: {str(e)}")
    finally:
        conexion.close()
    return redirect('/agregar_admin')




#----------------------------PETCIONES ADMINISTRADOR------------------------------------

@app.route('/ver_peticiones')
def ver_peticiones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT 
            p.idPeticion AS id,
            p.nombreMaestro,
            p.nombreMateria,
            p.mensaje,
            u.NomUsuario AS usuario
        FROM peticiones p
        JOIN usuarios u ON p.idUsuario = u.idUsuario;
    """
    cursor.execute(query)
    peticiones = cursor.fetchall()
    conexion.close()
    return render_template('peticion.html', peticiones=peticiones)


@app.route('/aceptar_peticion/<int:id>', methods=['POST'])
def aceptar_peticion(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Obtener la petición con los nombres
    cursor.execute("SELECT * FROM peticiones WHERE idPeticion = %s", (id,))
    peticion = cursor.fetchone()

    if peticion:
        nombre_maestro = peticion['nombreMaestro']
        nombre_materia = peticion['nombreMateria']

        # Buscar o insertar maestro
        cursor.execute("SELECT idMaestro FROM maestros WHERE nombreMaestro = %s", (nombre_maestro,))
        maestro = cursor.fetchone()
        if maestro:
            id_maestro = maestro['idMaestro']
        else:
            cursor.execute("INSERT INTO maestros (nombreMaestro) VALUES (%s)", (nombre_maestro,))
            conexion.commit()
            id_maestro = cursor.lastrowid

        # Buscar o insertar materia
        cursor.execute("SELECT idMateria FROM materias WHERE nombreMateria = %s", (nombre_materia,))
        materia = cursor.fetchone()
        if materia:
            id_materia = materia['idMateria']
        else:
            cursor.execute("INSERT INTO materias (nombreMateria) VALUES (%s)", (nombre_materia,))
            conexion.commit()
            id_materia = cursor.lastrowid

        # Insertar la relación maestro_materia si no existe ya
        cursor.execute("""
            INSERT IGNORE INTO maestro_materia (idMaestro, idMateria)
            VALUES (%s, %s)
        """, (id_maestro, id_materia))

        # Eliminar la petición ya procesada
        cursor.execute("DELETE FROM peticiones WHERE idPeticion = %s", (id,))
        conexion.commit()

    conexion.close()
    return redirect(url_for('ver_peticiones'))


@app.route('/denegar_peticion/<int:id>', methods=['POST'])
def denegar_peticion(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM peticiones WHERE idPeticion = %s", (id,))
    conexion.commit()

    conexion.close()
    return redirect(url_for('ver_peticiones'))

@app.route('/buscar_maestros')
def buscar_maestros():
    consulta = request.args.get('q', '')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Buscar todos los maestros que coincidan con la consulta
    cursor.execute("SELECT idMaestro, nombreMaestro FROM maestros WHERE nombreMaestro LIKE %s", ('%' + consulta + '%',))
    maestros = cursor.fetchall()  # ✅ Aquí está la corrección

    if not maestros:
        conexion.close()
        return render_template("resultados_maestros.html", consulta=consulta, maestros=[], resenas=[], nombre="")

    todos_resultados = []

    for id_maestro, nombre_maestro in maestros:
        cursor.execute("""
            SELECT r.comentario, r.calificacion, u.NomUsuario, m.nombreMateria
            FROM reseñas r
            JOIN usuarios u ON r.idUsuario = u.idUsuario
            JOIN maestro_materia mm ON r.idMaestro_Materia = mm.idMaestro_Materia
            JOIN materias m ON mm.idMateria = m.idMateria
            WHERE mm.idMaestro = %s
        """, (id_maestro,))
        resenas = cursor.fetchall()
        todos_resultados.append((nombre_maestro, resenas))  # Para mostrar varios maestros

    conexion.close()
    return render_template("resultados_maestros.html", consulta=consulta, resultados=todos_resultados)


@app.route('/buscar_materia')
def buscar_materia():
    consulta = request.args.get('consulta', '')
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT idMateria, nombreMateria FROM materias WHERE nombreMateria LIKE %s", (f"%{consulta}%",))
    resultados = cursor.fetchall()  # ✅ cambia esto

    resenas = []
    nombre_materia = ""

    if resultados:
        # Tomamos solo la primera coincidencia
        id_materia, nombre_materia = resultados[0]

        cursor.execute("""
            SELECT r.comentario, r.calificacion, u.NomUsuario, ma.nombreMaestro
            FROM reseñas r
            JOIN usuarios u ON r.idUsuario = u.idUsuario
            JOIN maestro_materia mm ON r.idMaestro_Materia = mm.idMaestro_Materia
            JOIN maestros ma ON mm.idMaestro = ma.idMaestro
            WHERE mm.idMateria = %s
        """, (id_materia,))
        resenas = cursor.fetchall()
    
    conexion.close()

    return render_template("resultados_materias.html", consulta=consulta, materias=True, resenas=resenas, nombre=nombre_materia)

#----------------------------------------------------------------------------------

@app.route('/reportar/<int:id_resena>', methods=['POST'])
def reportar_resena(id_resena):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE resenas SET reportada = 1 WHERE idResena = %s", (id_resena,))
        conexion.commit()
        conexion.close()
        return '', 204  # No Content
    except Exception as e:
        print("Error al reportar reseña:", e)
        return 'Error interno del servidor', 500

# ------------------ INICIO DEL SERVIDOR ------------------

if __name__ == '__main__':
    app.run(debug=True, port=5001)
