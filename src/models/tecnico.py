from src.models import db
from datetime import datetime

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    especialidades = db.Column(db.Text)  # JSON string con lista de especialidades
    tarifa_hora = db.Column(db.Float, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    diagnosticos = db.relationship('Diagnostico', backref='tecnico', lazy=True)
    citas = db.relationship('Cita', backref='tecnico', lazy=True)
    
    def to_dict(self):
        import json
        especialidades_list = []
        if self.especialidades:
            try:
                especialidades_list = json.loads(self.especialidades)
            except:
                especialidades_list = []
        
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'especialidades': especialidades_list,
            'tarifa_hora': self.tarifa_hora,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'diagnosticos_activos': len([d for d in self.diagnosticos if d.estado in ['pendiente', 'en_proceso']]) if self.diagnosticos else 0
        }
    
    def set_especialidades(self, especialidades_list):
        import json
        self.especialidades = json.dumps(especialidades_list)
    
    def get_especialidades(self):
        import json
        if self.especialidades:
            try:
                return json.loads(self.especialidades)
            except:
                return []
        return []
    
    def __repr__(self):
        return f'<Tecnico {self.nombre}>'

