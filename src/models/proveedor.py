from src.models import db
from datetime import datetime

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    tipo = db.Column(db.String(20), nullable=False)  # nuevo, usado
    activo = db.Column(db.Boolean, default=True)
    tiempo_respuesta_promedio = db.Column(db.String(50))  # ej: "2-4h"
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cotizaciones = db.relationship('CotizacionRepuesto', backref='proveedor', lazy=True)
    solicitudes_seleccionadas = db.relationship('SolicitudRepuesto', backref='proveedor_seleccionado', lazy=True)
    repuestos_preferidos = db.relationship('Repuesto', backref='proveedor_preferido', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'tipo': self.tipo,
            'activo': self.activo,
            'tiempo_respuesta_promedio': self.tiempo_respuesta_promedio,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'cotizaciones_enviadas': len(self.cotizaciones) if self.cotizaciones else 0,
            'pedidos_realizados': len(self.solicitudes_seleccionadas) if self.solicitudes_seleccionadas else 0
        }
    
    def __repr__(self):
        return f'<Proveedor {self.nombre} ({self.tipo})>'

