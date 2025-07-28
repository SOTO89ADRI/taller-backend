from flask import Blueprint, jsonify
from src.models import db
from src.models.cliente import Cliente
from src.models.vehiculo import Vehiculo
from src.models.diagnostico import Diagnostico
from src.models.cita import Cita
from src.models.factura import Factura
from src.models.repuesto import SolicitudRepuesto
from datetime import datetime, timedelta
from sqlalchemy import func, extract

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Obtener estadísticas principales del dashboard"""
    try:
        # Estadísticas básicas
        vehiculos_en_taller = Vehiculo.query.filter_by(estado='en_taller').count()
        
        # Citas de hoy
        hoy = datetime.now().date()
        citas_hoy = Cita.query.filter(
            func.date(Cita.fecha_hora) == hoy
        ).count()
        
        # Facturas pendientes
        facturas_pendientes = Factura.query.filter_by(estado='enviada').count()
        
        # Ingresos del mes actual
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        ingresos_mes = db.session.query(func.sum(Factura.total)).filter(
            Factura.estado == 'pagada',
            extract('month', Factura.fecha_emision) == mes_actual,
            extract('year', Factura.fecha_emision) == año_actual
        ).scalar() or 0
        
        # Clientes activos
        clientes_activos = Cliente.query.filter_by(activo=True).count()
        
        # Repuestos pendientes
        repuestos_pendientes = SolicitudRepuesto.query.filter(
            SolicitudRepuesto.estado.in_(['solicitado', 'cotizado', 'pedido'])
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'vehiculos_en_taller': vehiculos_en_taller,
                'citas_hoy': citas_hoy,
                'facturas_pendientes': facturas_pendientes,
                'ingresos_mes': round(ingresos_mes, 2),
                'clientes_activos': clientes_activos,
                'repuestos_pendientes': repuestos_pendientes
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/dashboard/revenue-chart', methods=['GET'])
def get_revenue_chart():
    """Obtener datos para el gráfico de ingresos mensuales"""
    try:
        # Obtener ingresos de los últimos 6 meses
        meses = []
        año_actual = datetime.now().year
        mes_actual = datetime.now().month
        
        for i in range(6):
            mes = mes_actual - i
            año = año_actual
            
            if mes <= 0:
                mes += 12
                año -= 1
            
            ingresos = db.session.query(func.sum(Factura.total)).filter(
                Factura.estado == 'pagada',
                extract('month', Factura.fecha_emision) == mes,
                extract('year', Factura.fecha_emision) == año
            ).scalar() or 0
            
            # Nombres de meses en español
            nombres_meses = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                           'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            
            meses.append({
                'month': nombres_meses[mes],
                'revenue': round(ingresos, 2)
            })
        
        # Invertir para mostrar cronológicamente
        meses.reverse()
        
        return jsonify({
            'success': True,
            'data': meses
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/dashboard/repair-types', methods=['GET'])
def get_repair_types():
    """Obtener distribución de tipos de reparación"""
    try:
        # Simular datos de tipos de reparación
        # En una implementación real, esto vendría de categorías de diagnósticos
        repair_types = [
            {'name': 'Motor', 'value': 35, 'color': '#3b82f6'},
            {'name': 'Frenos', 'value': 25, 'color': '#ef4444'},
            {'name': 'Transmisión', 'value': 20, 'color': '#10b981'},
            {'name': 'Eléctrico', 'value': 15, 'color': '#f59e0b'},
            {'name': 'Otros', 'value': 5, 'color': '#8b5cf6'}
        ]
        
        return jsonify({
            'success': True,
            'data': repair_types
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/dashboard/recent-activity', methods=['GET'])
def get_recent_activity():
    """Obtener actividad reciente del taller"""
    try:
        activities = []
        
        # Diagnósticos recientes
        diagnosticos_recientes = Diagnostico.query.order_by(
            Diagnostico.fecha_diagnostico.desc()
        ).limit(5).all()
        
        for diagnostico in diagnosticos_recientes:
            activities.append({
                'id': f"diagnostico_{diagnostico.id}",
                'type': 'diagnostico',
                'description': f"Nuevo diagnóstico para {diagnostico.vehiculo.marca} {diagnostico.vehiculo.modelo} - {diagnostico.descripcion_fallo[:50]}...",
                'time': diagnostico.fecha_diagnostico.strftime('%H:%M'),
                'status': 'nuevo'
            })
        
        # Citas recientes
        citas_recientes = Cita.query.filter(
            Cita.fecha_hora >= datetime.now() - timedelta(days=1)
        ).order_by(Cita.fecha_hora.desc()).limit(3).all()
        
        for cita in citas_recientes:
            activities.append({
                'id': f"cita_{cita.id}",
                'type': 'cita',
                'description': f"Cita programada para {cita.diagnostico.vehiculo.marca} {cita.diagnostico.vehiculo.modelo}",
                'time': cita.fecha_hora.strftime('%H:%M'),
                'status': 'programada'
            })
        
        # Facturas recientes
        facturas_recientes = Factura.query.order_by(
            Factura.fecha_emision.desc()
        ).limit(3).all()
        
        for factura in facturas_recientes:
            activities.append({
                'id': f"factura_{factura.id}",
                'type': 'factura',
                'description': f"Factura {factura.numero_factura} generada - €{factura.total:.2f}",
                'time': factura.fecha_emision.strftime('%H:%M'),
                'status': 'completada'
            })
        
        # Ordenar por tiempo y limitar a 10
        activities.sort(key=lambda x: x['time'], reverse=True)
        activities = activities[:10]
        
        return jsonify({
            'success': True,
            'data': activities
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/dashboard/diagnosticos-stats', methods=['GET'])
def get_diagnosticos_stats():
    """Obtener estadísticas de diagnósticos por estado"""
    try:
        pendientes = Diagnostico.query.filter_by(estado='pendiente').count()
        en_proceso = Diagnostico.query.filter_by(estado='en_proceso').count()
        completados = Diagnostico.query.filter_by(estado='completado').count()
        total = Diagnostico.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'pendientes': pendientes,
                'en_proceso': en_proceso,
                'completados': completados,
                'total': total
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

