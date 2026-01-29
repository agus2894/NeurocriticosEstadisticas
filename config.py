"""
Configuración de conexión a base de datos
Soporta SQLite (local) y Google Sheets (cloud)
"""
import os

# Tipo de base de datos: 'sqlite' o 'sheets'
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')

# Configuración para SQLite
SQLITE_DB_NAME = "pacientes_tec.db"

# Configuración para Google Sheets
# Obtener credenciales desde secrets de Streamlit Cloud
SHEETS_CREDENTIALS = None
SHEET_KEY = None

try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # En Streamlit Cloud, usar secrets
        if 'gcp_service_account' in st.secrets:
            SHEETS_CREDENTIALS = dict(st.secrets["gcp_service_account"])
            SHEET_KEY = st.secrets.get("sheet_key", None)
            DB_TYPE = 'sheets'
        else:
            DB_TYPE = 'sqlite'
except:
    DB_TYPE = 'sqlite'

def get_db_type():
    """Retorna el tipo de BD configurado"""
    return DB_TYPE
