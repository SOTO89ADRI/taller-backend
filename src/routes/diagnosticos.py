from flask import Blueprint, request, jsonify
from src.models import db
from src.models.diagnostico import Diagnostico

diagnosticos_bp = Blueprint('diagnosticos', __name__)

@diagnosticos_bp.route('/diagnosticos', methods=['GET'])
def get_diagnosticos():
    """Obtener lista de diagnósticos"""
    try:
        search = request.args.get('search', '')
        estado = request.args.get('estado')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        query = Diagnostico.query
        
        if search:
            query = query.join(Diagnostico.vehiculo).filter(
                db.or_(
                    Diagnostico.descripcion_fallo.ilike(f'%{search}%'),
                    db.text("vehiculos.matricula ILIKE :search").params(search=f'%{search}%')
                )
            )
        
        if estado and estado != 'todos':
            query = query.filter_by(estado=estado)
        
        diagnosticos = query.order_by(Diagnostico.fecha_diagnostico.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [diagnostico.to_dict() for diagnostico in diagnosticos.items],
            'pagination': {
                'page': page,
                'pages': diagnosticos.pages,
                'per_page': per_page,
                'total': diagnosticos.total
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@diagnosticos_bp.route('/diagnosticos/<int:diagnostico_id>', methods=['PUT'])
def update_diagnostico_estado(diagnostico_id):
    """Actualizar estado de diagnóstico"""
    try:
        diagnostico = Diagnostico.query.get_or_404(diagnostico_id)
        data = request.get_json()
        
        if 'estado' in data:
            diagnostico.estado = data['estado']
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Estado actualizado exitosamente',
                'data': diagnostico.to_dict()
            })
        
        return jsonify({'success': False, 'error': 'Estado no proporcionado'}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

