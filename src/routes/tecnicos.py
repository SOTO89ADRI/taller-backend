from flask import Blueprint, jsonify
from src.models.tecnico import Tecnico

tecnicos_bp = Blueprint('tecnicos', __name__)

@tecnicos_bp.route('/tecnicos', methods=['GET'])
def get_tecnicos():
    """Obtener lista de técnicos"""
    try:
        tecnicos = Tecnico.query.filter_by(activo=True).all()
        
        return jsonify({
            'success': True,
            'data': [tecnico.to_dict() for tecnico in tecnicos]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

