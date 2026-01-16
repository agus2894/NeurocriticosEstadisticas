#!/bin/bash

# Script para iniciar la aplicación de registro TEC

echo "🏥 Iniciando Sistema de Registro de Pacientes con TEC..."
echo ""

# Activar entorno virtual
source venv/bin/activate

# Ejecutar Streamlit
streamlit run app.py
