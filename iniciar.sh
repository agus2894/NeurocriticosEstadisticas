#!/bin/bash

# Script para iniciar la aplicación de registro TEC

echo "🏥 Iniciando Sistema de Registro de Pacientes con TEC..."
echo ""

# Verificar si existe el entorno virtual
if [ -d "venv" ]; then
    echo "🔄 Activando entorno virtual..."
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
    
    # Verificar si streamlit está instalado
    if ! python -c "import streamlit" 2>/dev/null; then
        echo "📥 Instalando dependencias (primera vez)..."
        pip install -r requirements.txt
        echo "✅ Dependencias instaladas"
    fi
else
    echo "ℹ️  No se encontró entorno virtual"
    echo "💡 Usando Python del sistema"
fi

echo ""
echo "🚀 Iniciando aplicación..."
echo "📍 La aplicación se abrirá en tu navegador"
echo "⏹️  Para detener: Presiona Ctrl+C"
echo ""

# Ejecutar Streamlit
streamlit run app.py
