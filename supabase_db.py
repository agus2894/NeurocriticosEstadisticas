"""
Backend de Supabase para persistencia en cloud
Mucho más simple que Google Sheets
"""
import pandas as pd
from datetime import datetime
import os

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class SupabaseDB:
    def __init__(self, url, key):
        """Inicializa conexión con Supabase"""
        if not SUPABASE_AVAILABLE:
            raise ImportError("Supabase library not available. Install: pip install supabase")
        
        self.supabase: Client = create_client(url, key)
    
    def init_db(self):
        """Las tablas se crean desde el dashboard de Supabase"""
        # Verificar que existan las tablas
        try:
            self.supabase.table('pacientes').select("*").limit(1).execute()
            return True
        except Exception as e:
            print(f"Tablas no encontradas. Créalas desde Supabase Dashboard:")
            print(f"Error: {e}")
            return True  # Retornar True para que la app no falle
    
    def insertar_paciente(self, **campos):
        """Inserta un nuevo paciente"""
        try:
            # Verificar si ya existe
            existing = self.supabase.table('pacientes')\
                .select("*")\
                .eq('numero_historia', campos['numero_historia'])\
                .execute()
            
            if existing.data:
                return False
            
            # Preparar datos
            datos = {
                'numero_historia': campos['numero_historia'],
                'edad': campos['edad'],
                'sexo': campos['sexo'],
                'fecha_ingreso': campos['fecha_ingreso'],
                'diagnostico': campos['diagnostico'],
                'origen_tec': campos['origen_tec'],
                'lesiones_asociadas': campos['lesiones_asociadas'],
                'requiere_pic': campos['requiere_pic'],
                'requiere_arm': campos['requiere_arm'],
                'requiere_cranectomia': campos['requiere_cranectomia'],
                'dias_uti': campos['dias_uti'],
                'glasgow_ingreso': campos['glasgow_ingreso'],
                'glasgow_actual': campos['glasgow_actual'],
                'destino_post_uti': campos.get('destino_post_uti', ''),
                'tiene_drenaje': campos.get('tiene_drenaje', False),
                'tipo_drenaje': campos.get('tipo_drenaje', ''),
                'llevaba_casco': campos.get('llevaba_casco'),
                'secuelas_motora': campos.get('secuelas_motora', False),
                'secuelas_neurologica': campos.get('secuelas_neurologica', False),
                'secuelas_cognitiva': campos.get('secuelas_cognitiva', False),
                'observaciones': campos.get('observaciones', '')
            }
            
            self.supabase.table('pacientes').insert(datos).execute()
            return True
        except Exception as e:
            print(f"Error al insertar paciente: {e}")
            return False
    
    def obtener_todos_pacientes(self):
        """Obtiene todos los pacientes"""
        try:
            response = self.supabase.table('pacientes')\
                .select("*")\
                .order('fecha_ingreso', desc=True)\
                .execute()
            
            if not response.data:
                return pd.DataFrame()
            
            df = pd.DataFrame(response.data)
            
            # Convertir tipos de datos
            if not df.empty:
                for col in ['requiere_pic', 'requiere_arm', 'requiere_cranectomia', 
                           'tiene_drenaje', 'secuelas_motora', 'secuelas_neurologica', 
                           'secuelas_cognitiva', 'llevaba_casco']:
                    if col in df.columns:
                        df[col] = df[col].fillna(False)
                
                for col in ['edad', 'dias_uti', 'glasgow_ingreso', 'glasgow_actual']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            return df
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")
            return pd.DataFrame()
    
    def obtener_paciente_por_historia(self, numero_historia):
        """Obtiene un paciente específico"""
        try:
            response = self.supabase.table('pacientes')\
                .select("*")\
                .eq('numero_historia', str(numero_historia))\
                .execute()
            
            if not response.data:
                return pd.DataFrame()
            
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error al obtener paciente: {e}")
            return pd.DataFrame()
    
    def actualizar_paciente(self, numero_historia, **campos):
        """Actualiza un paciente existente"""
        try:
            # Preparar datos para actualizar
            datos = {}
            for key, value in campos.items():
                if key != 'numero_historia':
                    datos[key] = value
            
            if 'fecha_ultima_actualizacion' not in datos:
                datos['fecha_ultima_actualizacion'] = datetime.now().isoformat()
            
            # Actualizar
            self.supabase.table('pacientes')\
                .update(datos)\
                .eq('numero_historia', numero_historia)\
                .execute()
            
            # Registrar evolución si hay cambios relevantes
            if any(k in campos for k in ['dias_uti', 'glasgow_actual', 'requiere_pic', 'requiere_arm', 'requiere_cranectomia']):
                evolucion = {
                    'numero_historia': numero_historia,
                    'dias_uti': campos.get('dias_uti'),
                    'glasgow_actual': campos.get('glasgow_actual'),
                    'requiere_pic': campos.get('requiere_pic'),
                    'requiere_arm': campos.get('requiere_arm'),
                    'requiere_cranectomia': campos.get('requiere_cranectomia'),
                    'observacion': campos.get('observaciones', '')
                }
                
                self.supabase.table('evoluciones').insert(evolucion).execute()
            
            return True
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            return False
    
    def obtener_evoluciones_paciente(self, numero_historia):
        """Obtiene el historial de evoluciones"""
        try:
            response = self.supabase.table('evoluciones')\
                .select("*")\
                .eq('numero_historia', str(numero_historia))\
                .order('fecha_evolucion', desc=True)\
                .execute()
            
            if not response.data:
                return pd.DataFrame()
            
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error al obtener evoluciones: {e}")
            return pd.DataFrame()
