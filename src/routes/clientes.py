from flask import Blueprint, request, jsonify
from src.models import db
from src.models.cliente import Cliente
from src.models.vehiculo import Vehiculo
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtener lista de clientes con filtros opcionales"""
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        query = Cliente.query
        
        if search:
            query = query.filter(
                db.or_(
                    Cliente.nombre_completo.ilike(f'%{search}%'),
                    Cliente.dni.ilike(f'%{search}%'),
                    Cliente.telefono.ilike(f'%{search}%'),
                    Cliente.email.ilike(f'%{search}%')
                )
            )
        
        clientes = query.order_by(Cliente.fecha_registro.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes.items],
            'pagination': {
                'page': page,
                'pages': clientes.pages,
                'per_page': per_page,
                'total': clientes.total
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    """Crear nuevo cliente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre_completo', 'dni', 'telefono', 'email', 'direccion', 'persona_contacto']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo {field} es requerido'}), 400
        
        # Verificar que el DNI no exista
        if Cliente.query.filter_by(dni=data['dni']).first():
            return jsonify({'success': False, 'error': 'Ya existe un cliente con este DNI'}), 400
        
        cliente = Cliente(
            nombre_completo=data['nombre_completo'],
            dni=data['dni'],
            telefono=data['telefono'],
            email=data['email'],
            direccion=data['direccion'],
            persona_contacto=data['persona_contacto']
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'data': cliente.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Obtener cliente por ID"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Incluir vehículos del cliente
        cliente_data = cliente.to_dict()
        cliente_data['vehiculos'] = [vehiculo.to_dict() for vehiculo in cliente.vehiculos]
        
        return jsonify({
            'success': True,
            'data': cliente_data
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    """Actualizar cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        # Verificar DNI único si se está cambiando
        if data.get('dni') and data['dni'] != cliente.dni:
            if Cliente.query.filter_by(dni=data['dni']).first():
                return jsonify({'success': False, 'error': 'Ya existe un cliente con este DNI'}), 400
        
        # Actualizar campos
        for field in ['nombre_completo', 'dni', 'telefono', 'email', 'direccion', 'persona_contacto']:
            if field in data:
                setattr(cliente, field, data[field])
        
        if 'activo' in data:
            cliente.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente actualizado exitosamente',
            'data': cliente.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    """Eliminar cliente (soft delete)"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Verificar si tiene vehículos activos
        vehiculos_activos = Vehiculo.query.filter_by(cliente_id=cliente_id, estado='activo').count()
        if vehiculos_activos > 0:
            return jsonify({
                'success': False, 
                'error': 'No se puede eliminar el cliente porque tiene vehículos activos'
            }), 400
        
        cliente.activo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente desactivado exitosamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@clientes_bp.route('/clientes/<int:cliente_id>/historial', methods=['GET'])
def get_cliente_historial(cliente_id):
    """Obtener historial de reparaciones del cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Obtener todos los diagnósticos de los vehículos del cliente
        diagnosticos = []
        for vehiculo in cliente.vehiculos:
            for diagnostico in vehiculo.diagnosticos:
                diagnosticos.append({
                    'id': diagnostico.id,
                    'vehiculo': f"{vehiculo.marca} {vehiculo.modelo} - {vehiculo.matricula}",
                    'fecha': diagnostico.fecha_diagnostico.isoformat() if diagnostico.fecha_diagnostico else None,
                    'descripcion': diagnostico.descripcion_fallo,
                    'estado': diagnostico.estado,
                    'costo': diagnostico.costo_estimado,
                    'tecnico': diagnostico.tecnico.nombre if diagnostico.tecnico else None
                })
        
        # Ordenar por fecha descendente
        diagnosticos.sort(key=lambda x: x['fecha'] or '', reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'cliente': cliente.to_dict(),
                'historial': diagnosticos
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

