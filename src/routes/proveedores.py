from flask import Blueprint, jsonify
from src.models.proveedor import Proveedor

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/proveedores', methods=['GET'])
def get_proveedores():
    """Obtener lista de proveedores"""
    try:
        proveedores = Proveedor.query.all()
        
        return jsonify({
            'success': True,
            'data': [proveedor.to_dict() for proveedor in proveedores]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

