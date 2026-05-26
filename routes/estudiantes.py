print("Modulo estudiantes cargado")

from flask import Blueprint, render_template, request, redirect
from conexion import conexion

estudiantes_bp = Blueprint('estudiantes', __name__)


@estudiantes_bp.route('/estudiantes')
def estudiantes():

    cursor = conexion.cursor()

    buscar = request.args.get('buscar', '')

    error = request.args.get('error')

    cursor.execute("""
        SELECT *
        FROM estudiantes
        WHERE nombre LIKE ?
        OR cedula LIKE ?
    """, (
        '%' + buscar + '%',
        '%' + buscar + '%'
    ))

    estudiantes = cursor.fetchall()

    return render_template(
        'estudiantes.html',
        estudiantes=estudiantes,
        buscar=buscar,
        error=error
    )


@estudiantes_bp.route('/agregar_estudiante', methods=['POST'])
def agregar_estudiante():

    nombre = request.form['nombre']
    cedula = request.form['cedula']
    if len(cedula) < 9:

        return redirect('/estudiantes')
    correo = request.form['correo']
    carrera = request.form['carrera']
    

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO estudiantes
        (nombre, cedula, correo, carrera)
        VALUES (?, ?, ?, ?)
    """, (nombre,cedula, correo, carrera))

    conexion.commit()

    return redirect('/estudiantes')


@estudiantes_bp.route('/eliminar_estudiante/<int:id>')
def eliminar_estudiante(id):

    cursor = conexion.cursor()

    # VALIDAR PRESTAMOS
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM prestamos
        WHERE id_estudiante = ?
    """, (id))
    prestamos = cursor.fetchone()
    if prestamos.total > 0:
        return redirect('/estudiantes?error=prestamos')

    # ELIMINAR
    cursor.execute("""
        DELETE FROM estudiantes
        WHERE id_estudiante = ?
    """, (id))
    conexion.commit()
    return redirect('/estudiantes')

