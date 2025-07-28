from flask import Blueprint, jsonify
from src.models.cita import Cita

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/citas', methods=['GET'])
def get_citas():
    """Obtener lista de citas"""
    try:
        citas = Cita.query.order_by(Cita.fecha_hora.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [cita.to_dict() for cita in citas]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

