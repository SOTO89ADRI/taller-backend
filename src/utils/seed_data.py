from src.models import db
from src.models.cliente import Cliente
from src.models.vehiculo import Vehiculo
from src.models.tecnico import Tecnico
from src.models.diagnostico import Diagnostico
from src.models.repuesto import Repuesto, SolicitudRepuesto, CotizacionRepuesto
from src.models.proveedor import Proveedor
from src.models.cita import Cita
from src.models.factura import Factura
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Crear datos de ejemplo para el sistema"""
    
    # Crear técnicos
    tecnicos_data = [
        {
            'nombre': 'Carlos Rodríguez',
            'telefono': '666123456',
            'email': 'carlos@taller.com',
            'especialidades': ['Motor', 'Transmisión'],
            'tarifa_hora': 35.0
        },
        {
            'nombre': 'Ana García',
            'telefono': '666234567',
            'email': 'ana@taller.com',
            'especialidades': ['Frenos', 'Suspensión'],
            'tarifa_hora': 30.0
        },
        {
            'nombre': 'Miguel López',
            'telefono': '666345678',
            'email': 'miguel@taller.com',
            'especialidades': ['Eléctrico', 'Aire Acondicionado'],
            'tarifa_hora': 32.0
        }
    ]
    
    tecnicos = []
    for data in tecnicos_data:
        tecnico = Tecnico(
            nombre=data['nombre'],
            telefono=data['telefono'],
            email=data['email'],
            tarifa_hora=data['tarifa_hora']
        )
        tecnico.set_especialidades(data['especialidades'])
        tecnicos.append(tecnico)
        db.session.add(tecnico)
    
    # Crear proveedores
    proveedores_data = [
        {
            'nombre': 'Repuestos Nuevos S.L.',
            'email': 'ventas@repuestosnuevos.com',
            'telefono': '912345678',
            'tipo': 'nuevo',
            'tiempo_respuesta_promedio': '2-4h'
        },
        {
            'nombre': 'Desguace El Rayo',
            'email': 'info@desguaceelrayo.com',
            'telefono': '913456789',
            'tipo': 'usado',
            'tiempo_respuesta_promedio': '4-8h'
        },
        {
            'nombre': 'AutoPartes Premium',
            'email': 'pedidos@autopartespremium.com',
            'telefono': '914567890',
            'tipo': 'nuevo',
            'tiempo_respuesta_promedio': '1-2h'
        }
    ]
    
    proveedores = []
    for data in proveedores_data:
        proveedor = Proveedor(**data)
        proveedores.append(proveedor)
        db.session.add(proveedor)
    
    # Crear repuestos
    repuestos_data = [
        {'nombre': 'Pastillas de freno delanteras', 'categoria': 'Frenos', 'precio_referencia': 45.0},
        {'nombre': 'Filtro de aceite', 'categoria': 'Motor', 'precio_referencia': 12.0},
        {'nombre': 'Amortiguador delantero', 'categoria': 'Suspensión', 'precio_referencia': 85.0},
        {'nombre': 'Batería 12V 60Ah', 'categoria': 'Eléctrico', 'precio_referencia': 120.0},
        {'nombre': 'Correa de distribución', 'categoria': 'Motor', 'precio_referencia': 35.0},
        {'nombre': 'Discos de freno', 'categoria': 'Frenos', 'precio_referencia': 65.0},
        {'nombre': 'Bujías', 'categoria': 'Motor', 'precio_referencia': 8.0},
        {'nombre': 'Filtro de aire', 'categoria': 'Motor', 'precio_referencia': 15.0}
    ]
    
    repuestos = []
    for data in repuestos_data:
        repuesto = Repuesto(
            nombre=data['nombre'],
            categoria=data['categoria'],
            precio_referencia=data['precio_referencia'],
            proveedor_preferido_id=random.choice(proveedores).id
        )
        repuestos.append(repuesto)
        db.session.add(repuesto)
    
    # Crear clientes
    clientes_data = [
        {
            'nombre_completo': 'Juan Pérez García',
            'dni': '12345678A',
            'telefono': '666111222',
            'email': 'juan.perez@email.com',
            'direccion': 'Calle Mayor, 123, Madrid',
            'persona_contacto': 'Juan Pérez'
        },
        {
            'nombre_completo': 'María González López',
            'dni': '23456789B',
            'telefono': '666222333',
            'email': 'maria.gonzalez@email.com',
            'direccion': 'Avenida de la Paz, 45, Madrid',
            'persona_contacto': 'María González'
        },
        {
            'nombre_completo': 'Carlos Martín Ruiz',
            'dni': '34567890C',
            'telefono': '666333444',
            'email': 'carlos.martin@email.com',
            'direccion': 'Plaza España, 12, Madrid',
            'persona_contacto': 'Carlos Martín'
        },
        {
            'nombre_completo': 'Ana Fernández Silva',
            'dni': '45678901D',
            'telefono': '666444555',
            'email': 'ana.fernandez@email.com',
            'direccion': 'Calle Alcalá, 200, Madrid',
            'persona_contacto': 'Ana Fernández'
        },
        {
            'nombre_completo': 'Luis Sánchez Torres',
            'dni': '56789012E',
            'telefono': '666555666',
            'email': 'luis.sanchez@email.com',
            'direccion': 'Gran Vía, 78, Madrid',
            'persona_contacto': 'Luis Sánchez'
        }
    ]
    
    clientes = []
    for data in clientes_data:
        cliente = Cliente(**data)
        clientes.append(cliente)
        db.session.add(cliente)
    
    # Crear vehículos
    vehiculos_data = [
        {'marca': 'Toyota', 'modelo': 'Corolla', 'año': 2018, 'matricula': '1234ABC', 'numero_bastidor': 'JT123456789012345', 'kilometraje': 85000},
        {'marca': 'Volkswagen', 'modelo': 'Golf', 'año': 2019, 'matricula': '2345BCD', 'numero_bastidor': 'WV234567890123456', 'kilometraje': 72000},
        {'marca': 'Ford', 'modelo': 'Focus', 'año': 2017, 'matricula': '3456CDE', 'numero_bastidor': 'FD345678901234567', 'kilometraje': 95000},
        {'marca': 'Seat', 'modelo': 'León', 'año': 2020, 'matricula': '4567DEF', 'numero_bastidor': 'ST456789012345678', 'kilometraje': 45000},
        {'marca': 'Renault', 'modelo': 'Clio', 'año': 2016, 'matricula': '5678EFG', 'numero_bastidor': 'RN567890123456789', 'kilometraje': 110000},
        {'marca': 'BMW', 'modelo': 'Serie 3', 'año': 2019, 'matricula': '6789FGH', 'numero_bastidor': 'BM678901234567890', 'kilometraje': 68000},
        {'marca': 'Audi', 'modelo': 'A4', 'año': 2018, 'matricula': '7890GHI', 'numero_bastidor': 'AU789012345678901', 'kilometraje': 78000},
        {'marca': 'Mercedes', 'modelo': 'Clase C', 'año': 2020, 'matricula': '8901HIJ', 'numero_bastidor': 'MB890123456789012', 'kilometraje': 35000}
    ]
    
    # Commit para obtener IDs de clientes
    db.session.commit()
    
    vehiculos = []
    for i, data in enumerate(vehiculos_data):
        vehiculo = Vehiculo(
            cliente_id=clientes[i % len(clientes)].id,
            marca=data['marca'],
            modelo=data['modelo'],
            año=data['año'],
            matricula=data['matricula'],
            numero_bastidor=data['numero_bastidor'],
            kilometraje=data['kilometraje'],
            estado=random.choice(['activo', 'en_taller', 'activo', 'activo'])  # Más probabilidad de activo
        )
        vehiculos.append(vehiculo)
        db.session.add(vehiculo)
    
    # Commit para obtener IDs de vehículos
    db.session.commit()
    
    # Crear diagnósticos
    descripciones_fallo = [
        'Ruido extraño en el motor al acelerar',
        'Frenos que chirrían al frenar',
        'Problema con el aire acondicionado',
        'Batería que se descarga rápidamente',
        'Vibración en el volante a alta velocidad',
        'Pérdida de potencia en subidas',
        'Luces que parpadean intermitentemente',
        'Problema con la transmisión automática',
        'Escape que hace ruido excesivo',
        'Sistema de dirección asistida con problemas'
    ]
    
    diagnosticos = []
    for i in range(15):
        diagnostico = Diagnostico(
            vehiculo_id=random.choice(vehiculos).id,
            tecnico_id=random.choice(tecnicos).id,
            descripcion_fallo=random.choice(descripciones_fallo),
            fecha_diagnostico=datetime.now() - timedelta(days=random.randint(0, 30)),
            estado=random.choice(['pendiente', 'en_proceso', 'completado', 'pendiente', 'en_proceso']),
            prioridad=random.choice(['baja', 'media', 'alta']),
            tiempo_estimado=random.choice(['2-3h', '4-6h', '1 día', '2-3 días']),
            costo_estimado=random.uniform(150, 800)
        )
        diagnosticos.append(diagnostico)
        db.session.add(diagnostico)
    
    # Commit para obtener IDs de diagnósticos
    db.session.commit()
    
    # Crear algunas solicitudes de repuestos
    for i in range(8):
        solicitud = SolicitudRepuesto(
            diagnostico_id=random.choice(diagnosticos).id,
            repuesto_id=random.choice(repuestos).id,
            cantidad=random.randint(1, 3),
            estado=random.choice(['solicitado', 'cotizado', 'pedido', 'recibido']),
            fecha_solicitud=datetime.now() - timedelta(days=random.randint(0, 15))
        )
        db.session.add(solicitud)
    
    # Crear algunas citas
    for i in range(10):
        fecha_base = datetime.now() + timedelta(days=random.randint(-5, 15))
        hora = random.randint(8, 17)
        fecha_hora = fecha_base.replace(hour=hora, minute=0, second=0, microsecond=0)
        
        cita = Cita(
            diagnostico_id=random.choice(diagnosticos).id,
            tecnico_id=random.choice(tecnicos).id,
            fecha_hora=fecha_hora,
            duracion_estimada=random.choice([120, 180, 240, 360, 480]),  # en minutos
            estado=random.choice(['programada', 'en_curso', 'completada']),
            tipo=random.choice(['reparacion', 'mantenimiento', 'diagnostico'])
        )
        db.session.add(cita)
    
    # Crear algunas facturas
    for i in range(6):
        factura = Factura(
            diagnostico_id=random.choice([d for d in diagnosticos if d.estado == 'completado']).id,
            fecha_emision=datetime.now() - timedelta(days=random.randint(0, 60)),
            estado=random.choice(['borrador', 'enviada', 'pagada']),
            subtotal_repuestos=random.uniform(50, 300),
            margen_repuestos=random.uniform(10, 60),
            subtotal_mano_obra=random.uniform(100, 400),
            iva=random.uniform(30, 150),
            total=random.uniform(200, 900)
        )
        factura.generar_numero_factura()
        db.session.add(factura)
    
    # Commit final
    db.session.commit()
    
    print("Datos de ejemplo creados exitosamente!")
    print(f"- {len(clientes)} clientes")
    print(f"- {len(vehiculos)} vehículos")
    print(f"- {len(tecnicos)} técnicos")
    print(f"- {len(diagnosticos)} diagnósticos")
    print(f"- {len(repuestos)} repuestos")
    print(f"- {len(proveedores)} proveedores")

