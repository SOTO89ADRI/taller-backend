from flask import Blueprint, jsonify
from src.models.repuesto import SolicitudRepuesto

repuestos_bp = Blueprint('repuestos', __name__)

@repuestos_bp.route('/repuestos/solicitudes', methods=['GET'])
def get_solicitudes_repuestos():
    """Obtener lista de solicitudes de repuestos"""
    try:
        solicitudes = SolicitudRepuesto.query.order_by(SolicitudRepuesto.fecha_solicitud.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [solicitud.to_dict() for solicitud in solicitudes]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

