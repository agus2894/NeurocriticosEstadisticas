"""
Backend de Google Sheets para persistencia en Streamlit Cloud
"""
import pandas as pd
from datetime import datetime
import streamlit as st

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

class SheetsDB:
    def __init__(self, credentials_dict, sheet_key):
        """Inicializa conexión con Google Sheets"""
        if not SHEETS_AVAILABLE:
            raise ImportError("Google Sheets libraries not available. Install: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet_key = sheet_key
        self.sheet = self.service.spreadsheets()
    
    def init_db(self):
        """Inicializa las hojas si no existen"""
        try:
            # Verificar si existe la hoja de pacientes
            result = self.sheet.get(spreadsheetId=self.sheet_key).execute()
            sheet_names = [s['properties']['title'] for s in result['sheets']]
            
            # Crear hoja de pacientes si no existe
            if 'pacientes' not in sheet_names:
                requests = [{
                    'addSheet': {
                        'properties': {
                            'title': 'pacientes'
                        }
                    }
                }]
                self.sheet.batchUpdate(
                    spreadsheetId=self.sheet_key,
                    body={'requests': requests}
                ).execute()
                
                # Agregar encabezados
                headers = [[
                    'numero_historia', 'edad', 'sexo', 'fecha_ingreso', 'diagnostico',
                    'origen_tec', 'lesiones_asociadas', 'requiere_pic', 'requiere_arm',
                    'requiere_cranectomia', 'dias_uti', 'glasgow_ingreso', 'glasgow_actual',
                    'destino_post_uti', 'tiene_drenaje', 'tipo_drenaje', 'llevaba_casco',
                    'secuelas_motora', 'secuelas_neurologica', 'secuelas_cognitiva',
                    'observaciones', 'fecha_registro', 'fecha_ultima_actualizacion'
                ]]
                
                self.sheet.values().update(
                    spreadsheetId=self.sheet_key,
                    range='pacientes!A1:W1',
                    valueInputOption='RAW',
                    body={'values': headers}
                ).execute()
            
            # Crear hoja de evoluciones si no existe
            if 'evoluciones' not in sheet_names:
                requests = [{
                    'addSheet': {
                        'properties': {
                            'title': 'evoluciones'
                        }
                    }
                }]
                self.sheet.batchUpdate(
                    spreadsheetId=self.sheet_key,
                    body={'requests': requests}
                ).execute()
                
                headers = [[
                    'numero_historia', 'fecha_evolucion', 'dias_uti', 'glasgow_actual',
                    'requiere_pic', 'requiere_arm', 'requiere_cranectomia', 'observacion'
                ]]
                
                self.sheet.values().update(
                    spreadsheetId=self.sheet_key,
                    range='evoluciones!A1:H1',
                    valueInputOption='RAW',
                    body={'values': headers}
                ).execute()
            
            return True
        except Exception as e:
            print(f"Error al inicializar sheets: {e}")
            return False
    
    def insertar_paciente(self, **campos):
        """Inserta un nuevo paciente"""
        try:
            # Verificar si ya existe
            existing = self.obtener_paciente_por_historia(campos['numero_historia'])
            if not existing.empty:
                return False
            
            # Preparar valores
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            valores = [[
                campos['numero_historia'],
                campos['edad'],
                campos['sexo'],
                campos['fecha_ingreso'],
                campos['diagnostico'],
                campos['origen_tec'],
                campos['lesiones_asociadas'],
                campos['requiere_pic'],
                campos['requiere_arm'],
                campos['requiere_cranectomia'],
                campos['dias_uti'],
                campos['glasgow_ingreso'],
                campos['glasgow_actual'],
                campos.get('destino_post_uti', ''),
                campos.get('tiene_drenaje', False),
                campos.get('tipo_drenaje', ''),
                campos.get('llevaba_casco', None),
                campos.get('secuelas_motora', False),
                campos.get('secuelas_neurologica', False),
                campos.get('secuelas_cognitiva', False),
                campos.get('observaciones', ''),
                fecha_registro,
                fecha_registro
            ]]
            
            self.sheet.values().append(
                spreadsheetId=self.sheet_key,
                range='pacientes!A:W',
                valueInputOption='RAW',
                body={'values': valores}
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error al insertar paciente: {e}")
            return False
    
    def obtener_todos_pacientes(self):
        """Obtiene todos los pacientes"""
        try:
            result = self.sheet.values().get(
                spreadsheetId=self.sheet_key,
                range='pacientes!A:W'
            ).execute()
            
            values = result.get('values', [])
            if len(values) <= 1:  # Solo headers o vacío
                return pd.DataFrame()
            
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Convertir tipos de datos
            if not df.empty:
                for col in ['requiere_pic', 'requiere_arm', 'requiere_cranectomia', 
                           'tiene_drenaje', 'secuelas_motora', 'secuelas_neurologica', 
                           'secuelas_cognitiva', 'llevaba_casco']:
                    if col in df.columns:
                        df[col] = df[col].map({'TRUE': True, 'True': True, True: True, 
                                              'FALSE': False, 'False': False, False: False, 
                                              '': False, None: False})
                
                for col in ['edad', 'dias_uti', 'glasgow_ingreso', 'glasgow_actual']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            return df
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")
            return pd.DataFrame()
    
    def obtener_paciente_por_historia(self, numero_historia):
        """Obtiene un paciente específico"""
        df = self.obtener_todos_pacientes()
        if df.empty:
            return pd.DataFrame()
        return df[df['numero_historia'] == str(numero_historia)]
    
    def actualizar_paciente(self, numero_historia, **campos):
        """Actualiza un paciente existente"""
        try:
            df = self.obtener_todos_pacientes()
            if df.empty:
                return False
            
            # Buscar fila del paciente
            idx = df[df['numero_historia'] == str(numero_historia)].index
            if len(idx) == 0:
                return False
            
            row_number = idx[0] + 2  # +2 porque: 1 por headers, 1 por 1-indexed
            
            # Actualizar campos
            campos['fecha_ultima_actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Preparar actualizaciones
            col_map = {
                'dias_uti': 'K',
                'glasgow_actual': 'M',
                'requiere_pic': 'H',
                'requiere_arm': 'I',
                'requiere_cranectomia': 'J',
                'destino_post_uti': 'N',
                'tiene_drenaje': 'O',
                'tipo_drenaje': 'P',
                'llevaba_casco': 'Q',
                'secuelas_motora': 'R',
                'secuelas_neurologica': 'S',
                'secuelas_cognitiva': 'T',
                'observaciones': 'U',
                'fecha_ultima_actualizacion': 'W'
            }
            
            data = []
            for campo, valor in campos.items():
                if campo in col_map:
                    col = col_map[campo]
                    data.append({
                        'range': f'pacientes!{col}{row_number}',
                        'values': [[valor]]
                    })
            
            if data:
                self.sheet.values().batchUpdate(
                    spreadsheetId=self.sheet_key,
                    body={'valueInputOption': 'RAW', 'data': data}
                ).execute()
            
            # Registrar evolución
            if any(k in campos for k in ['dias_uti', 'glasgow_actual', 'requiere_pic', 'requiere_arm', 'requiere_cranectomia']):
                evolucion = [[
                    numero_historia,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    campos.get('dias_uti', ''),
                    campos.get('glasgow_actual', ''),
                    campos.get('requiere_pic', ''),
                    campos.get('requiere_arm', ''),
                    campos.get('requiere_cranectomia', ''),
                    campos.get('observaciones', '')
                ]]
                
                self.sheet.values().append(
                    spreadsheetId=self.sheet_key,
                    range='evoluciones!A:H',
                    valueInputOption='RAW',
                    body={'values': evolucion}
                ).execute()
            
            return True
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            return False
    
    def obtener_evoluciones_paciente(self, numero_historia):
        """Obtiene el historial de evoluciones"""
        try:
            result = self.sheet.values().get(
                spreadsheetId=self.sheet_key,
                range='evoluciones!A:H'
            ).execute()
            
            values = result.get('values', [])
            if len(values) <= 1:
                return pd.DataFrame()
            
            df = pd.DataFrame(values[1:], columns=values[0])
            return df[df['numero_historia'] == str(numero_historia)]
        except Exception as e:
            print(f"Error al obtener evoluciones: {e}")
            return pd.DataFrame()
