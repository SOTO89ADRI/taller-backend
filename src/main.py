
import os
import sys

# Añadir la ruta raíz del proyecto para que Flask y Python encuentren los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Modelos y base de datos
from src.models import db
from src.models.user import User
from src.models.cliente import Cliente
from src.models.vehiculo import Vehiculo
from src.models.tecnico import Tecnico
from src.models.diagnostico import Diagnostico
from src.models.repuesto import Repuesto, SolicitudRepuesto, CotizacionRepuesto
from src.models.proveedor import Proveedor
from src.models.cita import Cita
from src.models.factura import Factura

# Rutas
from src.routes.user import user_bp
from src.routes.clientes import clientes_bp
from src.routes.vehiculos import vehiculos_bp
from src.routes.dashboard import dashboard_bp
from src.routes.tecnicos import tecnicos_bp
from src.routes.diagnosticos import diagnosticos_bp
from src.routes.repuestos import repuestos_bp
from src.routes.proveedores import proveedores_bp
from src.routes.citas import citas_bp
from src.routes.facturas import facturas_bp

# Datos de prueba
from src.utils.seed_data import create_sample_data

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='')

    # Configuración
    app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taller.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    CORS(app, origins="*")

    # Crear tablas y datos de ejemplo
    with app.app_context():
        db.create_all()
        if not Cliente.query.first():
            create_sample_data()
            print("✅ Datos de ejemplo creados exitosamente.")

    # Registrar Blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(clientes_bp, url_prefix='/api')
    app.register_blueprint(vehiculos_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(diagnosticos_bp, url_prefix='/api')
    app.register_blueprint(tecnicos_bp, url_prefix='/api')
    app.register_blueprint(repuestos_bp, url_prefix='/api')
    app.register_blueprint(proveedores_bp, url_prefix='/api')
    app.register_blueprint(citas_bp, url_prefix='/api')
    app.register_blueprint(facturas_bp, url_prefix='/api')

    # Ruta principal del frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')

    # Archivos estáticos o rutas SPA
    @app.route('/<path:path>')
    def serve_static(path):
        if path.startswith('api/'):
            return {'error': 'API endpoint not found'}, 404
        static_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app

