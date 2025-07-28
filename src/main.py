import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, send_file
from flask_cors import CORS

# Importar todos los modelos
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

# Importar rutas
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

# Importar datos de ejemplo
from src.utils.seed_data import create_sample_data

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, static_folder='../static', static_url_path='')
    
    # Configuración
    app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taller.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, origins="*")  # Permitir CORS para todas las rutas
    
    # Función para inicializar la base de datos
    def init_database():
        try:
            with app.app_context():
                db.create_all()
                # Crear datos de ejemplo si no existen
                if not Cliente.query.first():
                    create_sample_data()
                    print("Datos de ejemplo creados exitosamente")
                    return True
                return False
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            return False
    
    # Endpoint para inicializar la base de datos
    @app.route('/api/init-db')
    def initialize_database():
        success = init_database()
        return {
            'success': True,
            'message': 'Base de datos inicializada correctamente' if success else 'Base de datos ya estaba inicializada'
        }
    
    # Registrar blueprints
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
    
    # Ruta para servir el frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    # Ruta para servir archivos estáticos del frontend
    @app.route('/<path:path>')
    def serve_static(path):
        if path.startswith('api/'):
            # Si es una ruta de API, devolver 404
            return {'error': 'API endpoint not found'}, 404
        
        # Verificar si el archivo existe
        static_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_path):
            return send_from_directory(app.static_folder, path)
        else:
            # Si no existe, servir index.html para rutas del frontend (SPA)
            return send_from_directory(app.static_folder, 'index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas
        db.create_all()
        
        # Crear datos de ejemplo si no existen
        if not Cliente.query.first():
            create_sample_data()
            print("Datos de ejemplo creados exitosamente")
        
        print("Servidor iniciado en http://0.0.0.0:5000")
        print("Frontend disponible en: http://0.0.0.0:5000")
        print("API disponible en: http://0.0.0.0:5000/api/")
    
    # Ejecutar la aplicación
    app.run(host='0.0.0.0', port=5000, debug=False)

