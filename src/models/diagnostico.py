from src.models import db
from datetime import datetime

class Diagnostico(db.Model):
    __tablename__ = 'diagnosticos'
    
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('tecnicos.id'), nullable=False)
    descripcion_fallo = db.Column(db.Text, nullable=False)
    fecha_diagnostico = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, en_proceso, completado, cancelado
    prioridad = db.Column(db.String(10), default='media')  # baja, media, alta
    tiempo_estimado = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    costo_estimado = db.Column(db.Float, default=0.0)
    
    # Relaciones
    solicitudes_repuestos = db.relationship('SolicitudRepuesto', backref='diagnostico', lazy=True, cascade='all, delete-orphan')
    cita = db.relationship('Cita', backref='diagnostico', uselist=False, cascade='all, delete-orphan')
    factura = db.relationship('Factura', backref='diagnostico', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehiculo_id': self.vehiculo_id,
            'vehiculo_info': f"{self.vehiculo.marca} {self.vehiculo.modelo} - {self.vehiculo.matricula}" if self.vehiculo else None,
            'cliente_nombre': self.vehiculo.cliente.nombre_completo if self.vehiculo and self.vehiculo.cliente else None,
            'tecnico_id': self.tecnico_id,
            'tecnico_nombre': self.tecnico.nombre if self.tecnico else None,
            'descripcion_fallo': self.descripcion_fallo,
            'fecha_diagnostico': self.fecha_diagnostico.isoformat() if self.fecha_diagnostico else None,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'tiempo_estimado': self.tiempo_estimado,
            'observaciones': self.observaciones,
            'costo_estimado': self.costo_estimado,
            'repuestos_necesarios': [sr.repuesto.nombre for sr in self.solicitudes_repuestos] if self.solicitudes_repuestos else []
        }
    
    def __repr__(self):
        return f'<Diagnostico {self.id} - {self.vehiculo.matricula if self.vehiculo else "N/A"}>'

