"""
Adaptador universal de base de datos
Soporta SQLite y Google Sheets de forma transparente
"""
import config

# Determinar qué backend usar
if config.get_db_type() == 'sheets' and config.SHEETS_CREDENTIALS:
    # Usar Google Sheets
    from sheets_db import SheetsDB
    _db = SheetsDB(config.SHEETS_CREDENTIALS, config.SHEET_KEY)
    
    def init_db():
        return _db.init_db()
    
    def insertar_paciente(**kwargs):
        return _db.insertar_paciente(**kwargs)
    
    def obtener_todos_pacientes():
        return _db.obtener_todos_pacientes()
    
    def obtener_paciente_por_historia(numero_historia):
        return _db.obtener_paciente_por_historia(numero_historia)
    
    def actualizar_paciente(numero_historia, **campos):
        return _db.actualizar_paciente(numero_historia, **campos)
    
    def obtener_evoluciones_paciente(numero_historia):
        return _db.obtener_evoluciones_paciente(numero_historia)
    
    def eliminar_paciente(numero_historia):
        # No implementado para sheets
        return False
    
    def obtener_estadisticas():
        df = obtener_todos_pacientes()
        if df.empty:
            return {}
        
        return {
            'total_pacientes': len(df),
            'con_pic': df['requiere_pic'].sum() if 'requiere_pic' in df.columns else 0,
            'con_arm': df['requiere_arm'].sum() if 'requiere_arm' in df.columns else 0,
            'con_cranectomia': df['requiere_cranectomia'].sum() if 'requiere_cranectomia' in df.columns else 0,
            'edad_promedio': df['edad'].mean() if 'edad' in df.columns else 0,
            'dias_uti_promedio': df['dias_uti'].mean() if 'dias_uti' in df.columns else 0
        }

else:
    # Usar SQLite (importar el módulo original)
    from database import (
        init_db,
        insertar_paciente,
        obtener_todos_pacientes,
        obtener_paciente_por_historia,
        actualizar_paciente,
        eliminar_paciente,
        obtener_estadisticas,
        obtener_evoluciones_paciente
    )

# Función auxiliar para detectar el tipo de BD
def get_db_info():
    """Retorna información sobre el tipo de BD en uso"""
    if config.get_db_type() == 'sheets':
        return {
            'tipo': 'Google Sheets',
            'persistente': True,
            'multiusuario': True,
            'icono': '📊'
        }
    else:
        return {
            'tipo': 'SQLite (Local)',
            'persistente': True,
            'multiusuario': False,
            'icono': '💾'
        }
