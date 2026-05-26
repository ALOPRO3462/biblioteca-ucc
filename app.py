from flask import Flask

from routes.libros import libros_bp
from routes.estudiantes import estudiantes_bp
from routes.prestamos import prestamos_bp

app = Flask(__name__)

app.register_blueprint(libros_bp)
app.register_blueprint(estudiantes_bp)
app.register_blueprint(prestamos_bp)

if __name__ == '__main__':
    app.run(debug=True)