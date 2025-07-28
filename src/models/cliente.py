from src.models import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(300), nullable=False)
    persona_contacto = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    vehiculos = db.relationship('Vehiculo', backref='cliente', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'dni': self.dni,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'persona_contacto': self.persona_contacto,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo,
            'vehiculos_count': len(self.vehiculos) if self.vehiculos else 0
        }
    
    def __repr__(self):
        return f'<Cliente {self.nombre_completo}>'

