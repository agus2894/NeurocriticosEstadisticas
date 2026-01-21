import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "pacientes_tec.db"

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_historia TEXT UNIQUE NOT NULL,
            edad INTEGER NOT NULL,
            sexo TEXT NOT NULL,
            fecha_ingreso DATE NOT NULL,
            diagnostico TEXT NOT NULL,
            origen_tec TEXT NOT NULL,
            lesiones_asociadas TEXT,
            requiere_pic BOOLEAN NOT NULL,
            requiere_arm BOOLEAN NOT NULL,
            requiere_cranectomia BOOLEAN NOT NULL,
            dias_uti INTEGER NOT NULL,
            glasgow_ingreso INTEGER NOT NULL,
            glasgow_actual INTEGER NOT NULL,
            destino_post_uti TEXT,
            tiene_drenaje BOOLEAN DEFAULT 0,
            tipo_drenaje TEXT,
            llevaba_casco BOOLEAN,
            secuelas_motora BOOLEAN DEFAULT 0,
            secuelas_neurologica BOOLEAN DEFAULT 0,
            secuelas_cognitiva BOOLEAN DEFAULT 0,
            observaciones TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de evoluciones (historial de cambios)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evoluciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_historia TEXT NOT NULL,
            fecha_evolucion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            dias_uti INTEGER,
            glasgow_actual INTEGER,
            requiere_pic BOOLEAN,
            requiere_arm BOOLEAN,
            requiere_cranectomia BOOLEAN,
            observacion TEXT,
            FOREIGN KEY (numero_historia) REFERENCES pacientes(numero_historia)
        )
    ''')
    
    conn.commit()
    conn.close()

def insertar_paciente(numero_historia, edad, sexo, fecha_ingreso, diagnostico, 
                     origen_tec, lesiones_asociadas, requiere_pic, requiere_arm, 
                     requiere_cranectomia, dias_uti, glasgow_ingreso, glasgow_actual, 
                     destino_post_uti, tiene_drenaje, tipo_drenaje, llevaba_casco,
                     secuelas_motora, secuelas_neurologica, secuelas_cognitiva,
                     observaciones):
    """Inserta un nuevo paciente en la base de datos"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pacientes (
                numero_historia, edad, sexo, fecha_ingreso, diagnostico, origen_tec,
                lesiones_asociadas, requiere_pic, requiere_arm, requiere_cranectomia,
                dias_uti, glasgow_ingreso, glasgow_actual, destino_post_uti, tiene_drenaje,
                tipo_drenaje, llevaba_casco, secuelas_motora, secuelas_neurologica,
                secuelas_cognitiva, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_historia, edad, sexo, fecha_ingreso, diagnostico, origen_tec,
              lesiones_asociadas, requiere_pic, requiere_arm, requiere_cranectomia,
              dias_uti, glasgow_ingreso, glasgow_actual, destino_post_uti, tiene_drenaje,
              tipo_drenaje, llevaba_casco, secuelas_motora, secuelas_neurologica,
              secuelas_cognitiva, observaciones))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Ya existe un paciente con ese número de historia
        return False
    except Exception as e:
        print(f"Error al insertar paciente: {e}")
        return False

def obtener_todos_pacientes():
    """Obtiene todos los pacientes de la base de datos"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM pacientes ORDER BY fecha_ingreso DESC", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return pd.DataFrame()

def obtener_paciente_por_historia(numero_historia):
    """Obtiene un paciente específico por su número de historia"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(
            "SELECT * FROM pacientes WHERE numero_historia = ?", 
            conn, 
            params=(numero_historia,)
        )
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener paciente: {e}")
        return pd.DataFrame()

def actualizar_paciente(numero_historia, **campos):
    """Actualiza los datos de un paciente existente y registra la evolución"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Agregar timestamp de última actualización
        campos['fecha_ultima_actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construir la query de actualización dinámicamente
        set_clause = ", ".join([f"{campo} = ?" for campo in campos.keys()])
        valores = list(campos.values()) + [numero_historia]
        
        query = f"UPDATE pacientes SET {set_clause} WHERE numero_historia = ?"
        cursor.execute(query, valores)
        
        # Registrar en la tabla de evoluciones si hay cambios relevantes
        if any(key in campos for key in ['dias_uti', 'glasgow_actual', 'requiere_pic', 'requiere_arm', 'requiere_cranectomia']):
            cursor.execute('''
                INSERT INTO evoluciones (
                    numero_historia, dias_uti, glasgow_actual, requiere_pic, 
                    requiere_arm, requiere_cranectomia, observacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                numero_historia,
                campos.get('dias_uti'),
                campos.get('glasgow_actual'),
                campos.get('requiere_pic'),
                campos.get('requiere_arm'),
                campos.get('requiere_cranectomia'),
                campos.get('observaciones', '')
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar paciente: {e}")
        return False

def eliminar_paciente(numero_historia):
    """Elimina un paciente de la base de datos"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM pacientes WHERE numero_historia = ?", (numero_historia,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar paciente: {e}")
        return False

def obtener_estadisticas():
    """Obtiene estadísticas generales de los pacientes"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de pacientes
        cursor.execute("SELECT COUNT(*) FROM pacientes")
        stats['total_pacientes'] = cursor.fetchone()[0]
        
        # Pacientes con PIC
        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE requiere_pic = 1")
        stats['con_pic'] = cursor.fetchone()[0]
        
        # Pacientes con ARM
        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE requiere_arm = 1")
        stats['con_arm'] = cursor.fetchone()[0]
        
        # Pacientes con craniectomía
        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE requiere_cranectomia = 1")
        stats['con_cranectomia'] = cursor.fetchone()[0]
        
        # Edad promedio
        cursor.execute("SELECT AVG(edad) FROM pacientes")
        stats['edad_promedio'] = cursor.fetchone()[0]
        
        # Días promedio en UTI
        cursor.execute("SELECT AVG(dias_uti) FROM pacientes")
        stats['dias_uti_promedio'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {}

def obtener_evoluciones_paciente(numero_historia):
    """Obtiene el historial de evoluciones de un paciente"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(
            "SELECT * FROM evoluciones WHERE numero_historia = ? ORDER BY fecha_evolucion DESC", 
            conn, 
            params=(numero_historia,)
        )
        conn.close()
        return df
    except Exception as e:
        print(f"Error al obtener evoluciones: {e}")
        return pd.DataFrame()
