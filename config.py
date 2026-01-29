"""
Configuración de conexión a Supabase
"""
import streamlit as st

# Configuración para Supabase
SUPABASE_URL = st.secrets.get("supabase_url", None)
SUPABASE_KEY = st.secrets.get("supabase_key", None)
