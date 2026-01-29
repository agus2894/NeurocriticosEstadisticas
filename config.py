"""
Configuración de conexión a base de datos
Soporta SQLite (local), Google Sheets y Supabase (cloud)
"""
import os

# Tipo de base de datos: 'sqlite', 'sheets' o 'supabase'
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')

# Configuración para SQLite
SQLITE_DB_NAME = "pacientes_tec.db"

# Configuración para Google Sheets
SHEETS_CREDENTIALS = None
SHEET_KEY = None

# Configuración para Supabase (MÁS SIMPLE)
SUPABASE_URL = None
SUPABASE_KEY = None

try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Prioridad: Supabase (más simple)
        if 'supabase_url' in st.secrets and 'supabase_key' in st.secrets:
            SUPABASE_URL = st.secrets["supabase_url"]
            SUPABASE_KEY = st.secrets["supabase_key"]
            DB_TYPE = 'supabase'
        # Opción 2: Google Sheets
        elif 'gcp_service_account' in st.secrets:
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
