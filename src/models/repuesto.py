from src.models import db
from datetime import datetime

class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    precio_referencia = db.Column(db.Float)
    proveedor_preferido_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    
    # Relaciones
    solicitudes = db.relationship('SolicitudRepuesto', backref='repuesto', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'precio_referencia': self.precio_referencia,
            'proveedor_preferido_id': self.proveedor_preferido_id
        }
    
    def __repr__(self):
        return f'<Repuesto {self.nombre}>'


class SolicitudRepuesto(db.Model):
    __tablename__ = 'solicitudes_repuestos'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'), nullable=False)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuestos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.String(20), default='solicitado')  # solicitado, cotizado, pedido, recibido, cancelado
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    precio_mejor_oferta = db.Column(db.Float)
    proveedor_seleccionado_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    tiempo_entrega = db.Column(db.String(50))
    
    # Relaciones
    cotizaciones = db.relationship('CotizacionRepuesto', backref='solicitud', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnostico_id': self.diagnostico_id,
            'repuesto_id': self.repuesto_id,
            'repuesto_nombre': self.repuesto.nombre if self.repuesto else None,
            'cantidad': self.cantidad,
            'estado': self.estado,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            'precio_mejor_oferta': self.precio_mejor_oferta,
            'proveedor_seleccionado_id': self.proveedor_seleccionado_id,
            'proveedor_seleccionado_nombre': self.proveedor_seleccionado.nombre if self.proveedor_seleccionado else None,
            'tiempo_entrega': self.tiempo_entrega,
            'cotizaciones': [c.to_dict() for c in self.cotizaciones] if self.cotizaciones else []
        }
    
    def __repr__(self):
        return f'<SolicitudRepuesto {self.repuesto.nombre if self.repuesto else "N/A"}>'


class CotizacionRepuesto(db.Model):
    __tablename__ = 'cotizaciones_repuestos'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes_repuestos.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tiempo_entrega = db.Column(db.String(50))
    fecha_cotizacion = db.Column(db.DateTime, default=datetime.utcnow)
    valida_hasta = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'solicitud_id': self.solicitud_id,
            'proveedor_id': self.proveedor_id,
            'proveedor_nombre': self.proveedor.nombre if self.proveedor else None,
            'proveedor_tipo': self.proveedor.tipo if self.proveedor else None,
            'precio': self.precio,
            'tiempo_entrega': self.tiempo_entrega,
            'fecha_cotizacion': self.fecha_cotizacion.isoformat() if self.fecha_cotizacion else None,
            'valida_hasta': self.valida_hasta.isoformat() if self.valida_hasta else None
        }
    
    def __repr__(self):
        return f'<CotizacionRepuesto {self.proveedor.nombre if self.proveedor else "N/A"} - €{self.precio}>'

