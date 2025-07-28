from flask import Blueprint, request, jsonify
from src.models import db
from src.models.vehiculo import Vehiculo
from src.models.cliente import Cliente

vehiculos_bp = Blueprint('vehiculos', __name__)

@vehiculos_bp.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    """Obtener lista de vehículos con filtros opcionales"""
    try:
        search = request.args.get('search', '')
        cliente_id = request.args.get('cliente_id')
        estado = request.args.get('estado')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        query = Vehiculo.query
        
        if search:
            query = query.filter(
                db.or_(
                    Vehiculo.matricula.ilike(f'%{search}%'),
                    Vehiculo.marca.ilike(f'%{search}%'),
                    Vehiculo.modelo.ilike(f'%{search}%'),
                    Vehiculo.numero_bastidor.ilike(f'%{search}%')
                )
            )
        
        if cliente_id:
            query = query.filter_by(cliente_id=cliente_id)
        
        if estado:
            query = query.filter_by(estado=estado)
        
        vehiculos = query.order_by(Vehiculo.fecha_registro.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [vehiculo.to_dict() for vehiculo in vehiculos.items],
            'pagination': {
                'page': page,
                'pages': vehiculos.pages,
                'per_page': per_page,
                'total': vehiculos.total
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@vehiculos_bp.route('/vehiculos', methods=['POST'])
def create_vehiculo():
    """Crear nuevo vehículo"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['cliente_id', 'marca', 'modelo', 'año', 'matricula', 'numero_bastidor', 'kilometraje']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo {field} es requerido'}), 400
        
        # Verificar que el cliente existe
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'success': False, 'error': 'Cliente no encontrado'}), 404
        
        # Verificar que la matrícula no exista
        if Vehiculo.query.filter_by(matricula=data['matricula']).first():
            return jsonify({'success': False, 'error': 'Ya existe un vehículo con esta matrícula'}), 400
        
        # Verificar que el número de bastidor no exista
        if Vehiculo.query.filter_by(numero_bastidor=data['numero_bastidor']).first():
            return jsonify({'success': False, 'error': 'Ya existe un vehículo con este número de bastidor'}), 400
        
        vehiculo = Vehiculo(
            cliente_id=data['cliente_id'],
            marca=data['marca'],
            modelo=data['modelo'],
            año=data['año'],
            matricula=data['matricula'],
            numero_bastidor=data['numero_bastidor'],
            kilometraje=data['kilometraje'],
            estado=data.get('estado', 'activo')
        )
        
        db.session.add(vehiculo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehículo creado exitosamente',
            'data': vehiculo.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@vehiculos_bp.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo(vehiculo_id):
    """Obtener vehículo por ID"""
    try:
        vehiculo = Vehiculo.query.get_or_404(vehiculo_id)
        
        # Incluir historial de diagnósticos
        vehiculo_data = vehiculo.to_dict()
        vehiculo_data['diagnosticos'] = [diagnostico.to_dict() for diagnostico in vehiculo.diagnosticos]
        
        return jsonify({
            'success': True,
            'data': vehiculo_data
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@vehiculos_bp.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def update_vehiculo(vehiculo_id):
    """Actualizar vehículo"""
    try:
        vehiculo = Vehiculo.query.get_or_404(vehiculo_id)
        data = request.get_json()
        
        # Verificar matrícula única si se está cambiando
        if data.get('matricula') and data['matricula'] != vehiculo.matricula:
            if Vehiculo.query.filter_by(matricula=data['matricula']).first():
                return jsonify({'success': False, 'error': 'Ya existe un vehículo con esta matrícula'}), 400
        
        # Verificar número de bastidor único si se está cambiando
        if data.get('numero_bastidor') and data['numero_bastidor'] != vehiculo.numero_bastidor:
            if Vehiculo.query.filter_by(numero_bastidor=data['numero_bastidor']).first():
                return jsonify({'success': False, 'error': 'Ya existe un vehículo con este número de bastidor'}), 400
        
        # Actualizar campos
        for field in ['marca', 'modelo', 'año', 'matricula', 'numero_bastidor', 'kilometraje', 'estado']:
            if field in data:
                setattr(vehiculo, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehículo actualizado exitosamente',
            'data': vehiculo.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@vehiculos_bp.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo(vehiculo_id):
    """Eliminar vehículo (cambiar estado a inactivo)"""
    try:
        vehiculo = Vehiculo.query.get_or_404(vehiculo_id)
        
        # Verificar si tiene diagnósticos activos
        from src.models.diagnostico import Diagnostico
        diagnosticos_activos = Diagnostico.query.filter_by(
            vehiculo_id=vehiculo_id
        ).filter(
            Diagnostico.estado.in_(['pendiente', 'en_proceso'])
        ).count()
        
        if diagnosticos_activos > 0:
            return jsonify({
                'success': False, 
                'error': 'No se puede eliminar el vehículo porque tiene diagnósticos activos'
            }), 400
        
        vehiculo.estado = 'inactivo'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehículo desactivado exitosamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

