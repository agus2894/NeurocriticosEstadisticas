# 🏥 Sistema de Registro de Pacientes Neurocríticos - UTI

Sistema web colaborativo para el registro, seguimiento y análisis estadístico de pacientes con Traumatismo Encéfalo Craneano (TEC) en Unidad de Terapia Intensiva.

## 📋 Descripción General

Esta aplicación permite al equipo médico de la UTI:
- **Registrar** pacientes con TEC y sus características clínicas
- **Evolucionar** pacientes durante su estadía en UTI
- **Visualizar** estadísticas y tendencias en tiempo real
- **Exportar** datos para análisis externos
- **Colaborar** en la nube con acceso simultáneo de múltiples usuarios

### Tecnologías Utilizadas
- **Frontend**: Streamlit (Python)
- **Base de Datos**: Supabase (PostgreSQL en la nube)
- **Visualizaciones**: Plotly
- **Deploy**: Streamlit Cloud

---

## 🎯 Funcionalidades por Sección

### 1️⃣ Cargar Paciente

**Función**: Registro de nuevos pacientes con TEC que ingresan a la UTI.

**Características**:
- Datos de identificación (historia clínica, edad, sexo)
- Información del TEC (diagnóstico, origen, fecha de ingreso)
- Lesiones asociadas (fracturas, TEC abierto, politraumatismo, etc.)
- Intervenciones realizadas (PIC, ARM, craniectomía, drenajes)
- Glasgow al ingreso y actual
- Secuelas (motoras, neurológicas, cognitivas)
- Campo especial para accidentes en moto (uso de casco)
- Observaciones adicionales

**Captura de pantalla**:
<!-- Agregar captura aquí -->
```
[Imagen: formulario_cargar_paciente.png]
```

---

### 2️⃣ Evolucionar Paciente

**Función**: Actualizar el estado clínico de pacientes ya registrados durante su estadía en UTI.

**Características**:
- Selección de paciente por historia clínica
- Visualización de datos actuales del paciente
- Actualización de:
  - Días en UTI
  - Glasgow actual
  - Destino post-UTI (alta, fallecimiento, traslado)
  - Nueva intervención realizada
  - Observaciones evolutivas
- Historial de evoluciones con fechas y horas
- Cálculo automático de estadía

**Captura de pantalla**:
<!-- Agregar captura aquí -->
```
[Imagen: seccion_evolucionar.png]
```

---

### 3️⃣ Ver Estadísticas

**Función**: Visualización de datos agregados y análisis estadístico de todos los pacientes.

**Características**:

#### Métricas Generales
- Total de pacientes registrados
- Pacientes con PIC
- Pacientes con ARM
- Pacientes con craniectomía
- Edad promedio
- Días promedio en UTI

#### Gráficos Interactivos
1. **Origen del TEC** (pie chart): Accidente de tránsito, caída, agresión, etc.
2. **Distribución por Sexo** (bar chart): Masculino vs Femenino
3. **Intervenciones Realizadas** (bar chart): Comparación de PIC, ARM, craniectomía, drenajes
4. **Distribución por Edad** (histogram): Grupos etarios más afectados
5. **Glasgow al Ingreso vs Actual** (line chart): Evolución del estado neurológico
6. **Días de Estadía en UTI** (box plot): Análisis de tiempos de internación
7. **Destino Post-UTI** (pie chart): Alta, fallecimiento, traslado
8. **Uso de Casco en Accidentes de Moto** (pie chart): Análisis de factor protector

**Captura de pantalla**:
<!-- Agregar captura aquí -->
```
[Imagen: estadisticas_general.png]
```

---

### 4️⃣ Base de Datos

**Función**: Visualización tabular completa de todos los pacientes registrados.

**Características**:
- Tabla con todos los campos de cada paciente
- Filtros y búsqueda (nativa de Streamlit)
- Visualización de evoluciones por paciente
- Información de última actualización

**Captura de pantalla**:
<!-- Agregar captura aquí -->
```
[Imagen: base_datos.png]
```

---

### 5️⃣ Exportar Datos

**Función**: Descarga de datos en formato Excel para análisis externos.

**Características**:
- Exportación completa de tabla de pacientes
- Formato `.xlsx` compatible con Excel/Google Sheets
- Incluye todos los campos registrados
- Descarga instantánea desde el navegador

**Captura de pantalla**:
<!-- Agregar captura aquí -->
```
[Imagen: exportar_datos.png]
```

---

## 🚀 Instalación y Uso

### Acceso Web (Recomendado)
La aplicación está desplegada en la nube y accesible desde cualquier navegador:
```
https://[tu-url-streamlit-cloud].streamlit.app
```

### Ejecución Local (Opcional)
```bash
# Clonar repositorio
git clone https://github.com/agus2894/NeurocriticosEstadisticas.git
cd NeurocriticosEstadisticas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar secrets (crear .streamlit/secrets.toml)
# supabase_url = "tu_url"
# supabase_key = "tu_key"

# Ejecutar app
streamlit run app.py
```

---

## 📊 Estructura del Proyecto

```
NeurocriticosEstadisticas/
├── app.py                      # Aplicación principal
├── config.py                   # Configuración de Supabase
├── db_adapter.py               # Adaptador de base de datos
├── supabase_db.py              # Backend Supabase
├── supabase_rls_policies.sql   # Políticas de seguridad
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

---

## 🔒 Seguridad y Privacidad

- Base de datos en la nube con encriptación
- Row Level Security (RLS) habilitado en Supabase
- Acceso controlado mediante API keys
- Sin almacenamiento local de datos sensibles
- Cumple con estándares de privacidad médica

---

## 👥 Colaboradores

Sistema desarrollado para el equipo de Unidad de Terapia Intensiva.

**Modo Colaborativo**: Múltiples usuarios pueden cargar y consultar datos simultáneamente en tiempo real.

---

## 📝 Licencia

Uso interno exclusivo para fines médicos y de investigación clínica.

---

## 🆘 Soporte

Para reportar problemas o sugerir mejoras, contactar al administrador del sistema.

---

## 📅 Última Actualización

29 de enero de 2026
