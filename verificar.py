#!/usr/bin/env python3
"""
Script de verificación para comprobar que todos los cambios estén correctos
"""

import os
import sqlite3

def verificar_sistema():
    print("=" * 70)
    print("🔍 VERIFICACIÓN DEL SISTEMA - Versión 2.0")
    print("=" * 70)
    print()
    
    errores = []
    warnings = []
    
    # 1. Verificar archivos principales
    print("📁 Verificando archivos...")
    archivos_requeridos = [
        'app.py',
        'database.py',
        'migrar_db.py',
        'actualizar.sh',
        'iniciar.sh',
        'requirements.txt'
    ]
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            errores.append(f"Falta el archivo {archivo}")
    
    print()
    
    # 2. Verificar permisos de ejecución
    print("🔐 Verificando permisos...")
    scripts_ejecutables = ['migrar_db.py', 'actualizar.sh', 'iniciar.sh']
    
    for script in scripts_ejecutables:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"   ✅ {script} es ejecutable")
            else:
                print(f"   ⚠️  {script} no tiene permisos de ejecución")
                warnings.append(f"Ejecutar: chmod +x {script}")
    
    print()
    
    # 3. Verificar estructura de BD
    print("🗄️  Verificando estructura de base de datos...")
    
    if os.path.exists('pacientes_tec.db'):
        print("   ℹ️  Base de datos existente encontrada")
        
        conn = sqlite3.connect('pacientes_tec.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(pacientes)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        nuevas_columnas = [
            'destino_post_uti',
            'tiene_drenaje',
            'tipo_drenaje',
            'llevaba_casco',
            'secuelas_motora',
            'secuelas_neurologica',
            'secuelas_cognitiva'
        ]
        
        print(f"   📊 Total de columnas: {len(columnas)}")
        
        for col in nuevas_columnas:
            if col in columnas:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ {col} - FALTA")
                errores.append(f"Columna {col} no encontrada. Ejecutar migrar_db.py")
        
        conn.close()
    else:
        print("   ℹ️  No hay base de datos previa (se creará al iniciar)")
    
    print()
    
    # 4. Verificar sintaxis de Python
    print("🐍 Verificando sintaxis Python...")
    import py_compile
    
    archivos_python = ['app.py', 'database.py', 'migrar_db.py']
    
    for archivo in archivos_python:
        try:
            py_compile.compile(archivo, doraise=True)
            print(f"   ✅ {archivo} - sintaxis correcta")
        except py_compile.PyCompileError as e:
            print(f"   ❌ {archivo} - ERROR DE SINTAXIS")
            errores.append(f"Error de sintaxis en {archivo}")
    
    print()
    
    # Resumen
    print("=" * 70)
    print("📋 RESUMEN")
    print("=" * 70)
    
    if not errores and not warnings:
        print("✅ ¡TODO PERFECTO! El sistema está listo para usar.")
        print()
        print("🚀 Para iniciar la aplicación ejecute:")
        print("   ./iniciar.sh")
        print("   o")
        print("   streamlit run app.py")
    else:
        if errores:
            print("❌ ERRORES ENCONTRADOS:")
            for error in errores:
                print(f"   • {error}")
            print()
        
        if warnings:
            print("⚠️  ADVERTENCIAS:")
            for warning in warnings:
                print(f"   • {warning}")
            print()
        
        if errores:
            print("⚠️  Corrija los errores antes de usar el sistema")
            return False
    
    print("=" * 70)
    return True

if __name__ == "__main__":
    try:
        exito = verificar_sistema()
        exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        exit(1)
