print("Modulo estudiantes cargado")

from flask import Blueprint, render_template, request, redirect
from conexion import conexion

estudiantes_bp = Blueprint('estudiantes', __name__)


@estudiantes_bp.route('/estudiantes')
def estudiantes():

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM estudiantes")

    estudiantes = cursor.fetchall()

    return render_template(
        'estudiantes.html',
        estudiantes=estudiantes
    )


@estudiantes_bp.route('/agregar_estudiante', methods=['POST'])
def agregar_estudiante():

    nombre = request.form['nombre']
    cedula = request.form['cedula']
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

    cursor.execute("""
        DELETE FROM estudiantes
        WHERE id_estudiante = ?
    """, (id))

    conexion.commit()

    return redirect('/estudiantes')

