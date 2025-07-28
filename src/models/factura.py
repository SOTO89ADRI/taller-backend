from src.models import db
from datetime import datetime, timedelta

class Factura(db.Model):
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_factura = db.Column(db.String(20), unique=True, nullable=False)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'), nullable=False)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='borrador')  # borrador, enviada, pagada, vencida
    
    # Importes
    subtotal_repuestos = db.Column(db.Float, default=0.0)
    margen_repuestos = db.Column(db.Float, default=0.0)
    subtotal_mano_obra = db.Column(db.Float, default=0.0)
    iva = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    # Detalles JSON
    detalle_repuestos = db.Column(db.Text)  # JSON con detalles de repuestos
    detalle_mano_obra = db.Column(db.Text)  # JSON con detalles de mano de obra
    
    # Archivo PDF
    ruta_pdf = db.Column(db.String(500))
    
    def to_dict(self):
        import json
        
        detalle_repuestos_list = []
        detalle_mano_obra_list = []
        
        if self.detalle_repuestos:
            try:
                detalle_repuestos_list = json.loads(self.detalle_repuestos)
            except:
                pass
        
        if self.detalle_mano_obra:
            try:
                detalle_mano_obra_list = json.loads(self.detalle_mano_obra)
            except:
                pass
        
        return {
            'id': self.id,
            'numero_factura': self.numero_factura,
            'diagnostico_id': self.diagnostico_id,
            'vehiculo_info': f"{self.diagnostico.vehiculo.marca} {self.diagnostico.vehiculo.modelo} - {self.diagnostico.vehiculo.matricula}" if self.diagnostico and self.diagnostico.vehiculo else None,
            'cliente_nombre': self.diagnostico.vehiculo.cliente.nombre_completo if self.diagnostico and self.diagnostico.vehiculo and self.diagnostico.vehiculo.cliente else None,
            'cliente_datos': self.get_cliente_datos(),
            'fecha_emision': self.fecha_emision.isoformat() if self.fecha_emision else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'estado': self.estado,
            'subtotal_repuestos': self.subtotal_repuestos,
            'margen_repuestos': self.margen_repuestos,
            'subtotal_mano_obra': self.subtotal_mano_obra,
            'iva': self.iva,
            'total': self.total,
            'detalle_repuestos': detalle_repuestos_list,
            'detalle_mano_obra': detalle_mano_obra_list,
            'ruta_pdf': self.ruta_pdf
        }
    
    def get_cliente_datos(self):
        if self.diagnostico and self.diagnostico.vehiculo and self.diagnostico.vehiculo.cliente:
            cliente = self.diagnostico.vehiculo.cliente
            return {
                'nombre_completo': cliente.nombre_completo,
                'dni': cliente.dni,
                'telefono': cliente.telefono,
                'email': cliente.email,
                'direccion': cliente.direccion,
                'persona_contacto': cliente.persona_contacto
            }
        return None
    
    def set_detalle_repuestos(self, detalle_list):
        import json
        self.detalle_repuestos = json.dumps(detalle_list)
    
    def set_detalle_mano_obra(self, detalle_list):
        import json
        self.detalle_mano_obra = json.dumps(detalle_list)
    
    def calcular_totales(self, margen_nuevos=20, margen_usados=30, iva_porcentaje=21):
        """Calcula automáticamente los totales de la factura"""
        import json
        
        # Calcular subtotal repuestos con margen
        subtotal_repuestos_base = 0
        margen_total = 0
        
        if self.detalle_repuestos:
            try:
                repuestos = json.loads(self.detalle_repuestos)
                for repuesto in repuestos:
                    precio_base = repuesto.get('precio', 0)
                    tipo = repuesto.get('tipo', 'nuevo')
                    margen_porcentaje = margen_usados if tipo == 'usado' else margen_nuevos
                    margen_item = precio_base * (margen_porcentaje / 100)
                    
                    subtotal_repuestos_base += precio_base
                    margen_total += margen_item
                    
                    # Actualizar precio final en el detalle
                    repuesto['precio_final'] = precio_base + margen_item
                    repuesto['margen'] = margen_porcentaje
                
                self.detalle_repuestos = json.dumps(repuestos)
            except:
                pass
        
        self.subtotal_repuestos = subtotal_repuestos_base
        self.margen_repuestos = margen_total
        
        # Calcular subtotal mano de obra
        subtotal_mano_obra = 0
        if self.detalle_mano_obra:
            try:
                trabajos = json.loads(self.detalle_mano_obra)
                for trabajo in trabajos:
                    subtotal_mano_obra += trabajo.get('total', 0)
            except:
                pass
        
        self.subtotal_mano_obra = subtotal_mano_obra
        
        # Calcular IVA y total
        subtotal_sin_iva = (subtotal_repuestos_base + margen_total + subtotal_mano_obra)
        self.iva = subtotal_sin_iva * (iva_porcentaje / 100)
        self.total = subtotal_sin_iva + self.iva
        
        # Establecer fecha de vencimiento (30 días)
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_emision + timedelta(days=30)
    
    def generar_numero_factura(self):
        """Genera un número de factura único"""
        if not self.numero_factura:
            # Buscar el último número de factura
            ultima_factura = Factura.query.order_by(Factura.id.desc()).first()
            if ultima_factura and ultima_factura.numero_factura:
                try:
                    ultimo_numero = int(ultima_factura.numero_factura.replace('FT', ''))
                    nuevo_numero = ultimo_numero + 1
                except:
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            
            self.numero_factura = f"FT{nuevo_numero:03d}"
    
    def __repr__(self):
        return f'<Factura {self.numero_factura}>'

