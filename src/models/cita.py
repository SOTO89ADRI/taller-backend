from src.models import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnosticos.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('tecnicos.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion_estimada = db.Column(db.Integer, nullable=False)  # en minutos
    estado = db.Column(db.String(20), default='programada')  # programada, en_curso, completada, cancelada
    tipo = db.Column(db.String(20), default='reparacion')  # reparacion, mantenimiento, diagnostico
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnostico_id': self.diagnostico_id,
            'vehiculo_info': f"{self.diagnostico.vehiculo.marca} {self.diagnostico.vehiculo.modelo} - {self.diagnostico.vehiculo.matricula}" if self.diagnostico and self.diagnostico.vehiculo else None,
            'cliente_nombre': self.diagnostico.vehiculo.cliente.nombre_completo if self.diagnostico and self.diagnostico.vehiculo and self.diagnostico.vehiculo.cliente else None,
            'tecnico_id': self.tecnico_id,
            'tecnico_nombre': self.tecnico.nombre if self.tecnico else None,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'fecha': self.fecha_hora.date().isoformat() if self.fecha_hora else None,
            'hora_inicio': self.fecha_hora.time().strftime('%H:%M') if self.fecha_hora else None,
            'hora_fin': self.get_hora_fin(),
            'duracion_estimada': self.duracion_estimada,
            'duracion_horas': f"{self.duracion_estimada // 60}h {self.duracion_estimada % 60}m" if self.duracion_estimada else None,
            'estado': self.estado,
            'tipo': self.tipo,
            'descripcion': self.diagnostico.descripcion_fallo if self.diagnostico else None,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def get_hora_fin(self):
        if self.fecha_hora and self.duracion_estimada:
            from datetime import timedelta
            hora_fin = self.fecha_hora + timedelta(minutes=self.duracion_estimada)
            return hora_fin.time().strftime('%H:%M')
        return None
    
    def __repr__(self):
        return f'<Cita {self.id} - {self.fecha_hora}>'

