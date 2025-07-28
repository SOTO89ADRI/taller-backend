from src.models import db
from datetime import datetime

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    numero_bastidor = db.Column(db.String(50), unique=True, nullable=False)
    kilometraje = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activo')  # activo, en_taller, inactivo
    
    # Relaciones
    diagnosticos = db.relationship('Diagnostico', backref='vehiculo', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else None,
            'marca': self.marca,
            'modelo': self.modelo,
            'año': self.año,
            'matricula': self.matricula,
            'numero_bastidor': self.numero_bastidor,
            'kilometraje': self.kilometraje,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'estado': self.estado,
            'ultimo_servicio': self.get_ultimo_servicio()
        }
    
    def get_ultimo_servicio(self):
        if self.diagnosticos:
            ultimo = max(self.diagnosticos, key=lambda d: d.fecha_diagnostico)
            return ultimo.fecha_diagnostico.isoformat()
        return None
    
    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo} - {self.matricula}>'

