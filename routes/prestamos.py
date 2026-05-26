from flask import Blueprint, render_template, request, redirect
from conexion import conexion

prestamos_bp = Blueprint('prestamos', __name__)


@prestamos_bp.route('/prestamos')
def prestamos():

    cursor = conexion.cursor()
    buscar = request.args.get('buscar', '')

    # estudiantes

    cursor.execute("""
        SELECT * FROM estudiantes
    """)

    estudiantes = cursor.fetchall()

    # libros

    cursor.execute("""
        SELECT * FROM libros
    """)

    libros = cursor.fetchall()

    # prestamos activos

    cursor.execute("""

        SELECT
            p.id_prestamo,
            e.nombre AS estudiante,
            e.cedula,
            l.titulo AS libro,
            p.fecha_prestamo,
            p.fecha_limite,
            CASE
                WHEN p.fecha_limite < GETDATE()
                THEN 'Vencido'
                ELSE 'En tiempo'
            END AS estado_tiempo,
            p.estado

        FROM prestamos p

        INNER JOIN estudiantes e
        ON p.id_estudiante = e.id_estudiante

        INNER JOIN libros l
        ON p.id_libro = l.id_libro

        WHERE p.estado = 'Activo'

        AND (

            e.nombre LIKE ?
            OR e.cedula LIKE ?
            OR l.titulo LIKE ?

        )

    """, (

        '%' + buscar + '%',
        '%' + buscar + '%',
        '%' + buscar + '%'

    ))

    prestamos_activos = cursor.fetchall()

    # historial devoluciones

    cursor.execute("""

        SELECT
            p.id_prestamo,
            e.nombre AS estudiante,
            e.cedula,
            l.titulo AS libro,
            p.fecha_prestamo,
            p.fecha_devolucion,
            p.estado

        FROM prestamos p

        INNER JOIN estudiantes e
        ON p.id_estudiante = e.id_estudiante

        INNER JOIN libros l
        ON p.id_libro = l.id_libro

        WHERE p.estado = 'Devuelto'

    """)

    prestamos_devueltos = cursor.fetchall()

    error = request.args.get('error')

    return render_template(
        'prestamos.html',

        estudiantes=estudiantes,
        libros=libros,

        prestamos_activos=prestamos_activos,
        prestamos_devueltos=prestamos_devueltos,

        buscar=buscar,
        error=error
    )


@prestamos_bp.route('/agregar_prestamo', methods=['POST'])
def agregar_prestamo():

    id_estudiante = request.form['id_estudiante']
    id_libro = request.form['id_libro']

    cursor = conexion.cursor()

    # VALIDAR MAXIMO 3 PRESTAMOS

    cursor.execute("""

        SELECT COUNT(*) AS total
        FROM prestamos
        WHERE id_estudiante = ?
        AND estado = 'Activo'

    """, (id_estudiante))

    cantidad = cursor.fetchone()

    if cantidad.total >= 3:

        return redirect('/prestamos?error=maximo')

    # VALIDAR STOCK

    cursor.execute("""

        SELECT stock
        FROM libros
        WHERE id_libro = ?

    """, (id_libro))

    libro = cursor.fetchone()

    if libro.stock <= 0:

        return redirect('/prestamos?error=stock')

    # REGISTRAR PRESTAMO

    cursor.execute("""

        INSERT INTO prestamos
            (id_estudiante,id_libro,fecha_limite)
        VALUES
        (?, ?, DATEADD(DAY, 7, GETDATE()))

    """, (id_estudiante, id_libro))

    # DESCONTAR STOCK

    cursor.execute("""

        UPDATE libros
        SET stock = stock - 1
        WHERE id_libro = ?

    """, (id_libro))

    conexion.commit()

    return redirect('/prestamos')


@prestamos_bp.route('/devolver_prestamo/<int:id>')
def devolver_prestamo(id):

    cursor = conexion.cursor()

    # obtener libro prestado

    cursor.execute("""

        SELECT id_libro
        FROM prestamos
        WHERE id_prestamo = ?

    """, (id))

    prestamo = cursor.fetchone()

    id_libro = prestamo.id_libro

    # actualizar estado

    cursor.execute("""

        UPDATE prestamos
        SET estado = 'Devuelto',
            fecha_devolucion = GETDATE()
        WHERE id_prestamo = ?

    """, (id))

    # devolver stock

    cursor.execute("""

        UPDATE libros
        SET stock = stock + 1
        WHERE id_libro = ?

    """, (id_libro))

    conexion.commit()

    return redirect('/prestamos')