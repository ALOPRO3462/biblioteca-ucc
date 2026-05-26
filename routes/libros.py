from flask import Blueprint, render_template, request, redirect
from conexion import conexion

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/')
def inicio():

    cursor = conexion.cursor()

    # OBTENER LIBROS

    cursor.execute("""
        SELECT * FROM libros
    """)

    libros = cursor.fetchall()

    # TOTAL LIBROS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM libros
    """)

    total_libros = cursor.fetchone()

    # TOTAL ESTUDIANTES

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM estudiantes
    """)

    total_estudiantes = cursor.fetchone()

    # PRESTAMOS ACTIVOS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM prestamos
        WHERE estado = 'Activo'
    """)

    prestamos_activos = cursor.fetchone()

    # LIBROS DISPONIBLES

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM libros
        WHERE stock > 0
    """)

    libros_disponibles = cursor.fetchone()

    error = request.args.get('error')

    return render_template('index.html',libros=libros,error=error,total_libros=total_libros,total_estudiantes=total_estudiantes,prestamos_activos=prestamos_activos,libros_disponibles=libros_disponibles)

@libros_bp.route('/agregar_libro', methods=['POST'])
def agregar_libro():

    titulo = request.form['titulo']
    autor = request.form['autor']
    stock = request.form['stock']

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO libros (titulo, autor, stock)
        VALUES (?, ?, ?)
    """, (titulo, autor, stock))

    conexion.commit()

    return redirect('/')


@libros_bp.route('/eliminar_libro/<int:id>')
def eliminar_libro(id):

    cursor = conexion.cursor()

    # validar prestamos activos

    cursor.execute("""

        SELECT COUNT(*) AS total

        FROM prestamos

        WHERE id_libro = ?
        AND estado = 'Activo'

    """, (id))

    prestamos = cursor.fetchone()

    if prestamos.total > 0:

        return redirect('/?error=prestamo_activo')

    # eliminar libro

    cursor.execute("""

        DELETE FROM libros
        WHERE id_libro = ?

    """, (id))

    conexion.commit()

    return redirect('/')


@libros_bp.route('/editar_libro/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):

    cursor = conexion.cursor()

    if request.method == 'POST':

        titulo = request.form['titulo']
        autor = request.form['autor']
        stock = request.form['stock']

        cursor.execute("""
            UPDATE libros
            SET titulo = ?, autor = ?, stock = ?
            WHERE id_libro = ?
        """, (titulo, autor, stock, id))

        conexion.commit()

        return redirect('/')

    cursor.execute("""
        SELECT * FROM libros
        WHERE id_libro = ?
    """, (id))

    libro = cursor.fetchone()

    return render_template('editar.html', libro=libro)