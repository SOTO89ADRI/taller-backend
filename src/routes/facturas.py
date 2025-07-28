from flask import Blueprint, jsonify
from src.models.factura import Factura

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/facturas', methods=['GET'])
def get_facturas():
    """Obtener lista de facturas"""
    try:
        facturas = Factura.query.order_by(Factura.fecha_emision.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [factura.to_dict() for factura in facturas]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

