# 🏥 Sistema de Registro de Pacientes con TEC - UTI

Sistema web para el registro y análisis estadístico de pacientes neurocríticos con Traumatismo Encéfalo Craneal (TEC) en Unidad de Terapia Intensiva.

## 📋 Características

- **Registro de pacientes**: Formulario completo para capturar todos los datos relevantes
- **Base de datos**: Almacenamiento persistente con SQLite
- **Dashboard estadístico**: Gráficos interactivos y análisis en tiempo real
- **Exportación de datos**: Descarga de datos en formato CSV/Excel
- **Multi-usuario**: Acceso web para múltiples colaboradores
- **Responsive**: Funciona en computadoras, tablets y móviles

## 📊 Datos Capturados

### Información del Paciente
- Número de Historia Clínica
- Edad y Sexo
- Fecha de Ingreso

### Información del TEC
- Diagnóstico principal
- Origen del TEC (accidente, caída, agresión, etc.)
- Lesiones asociadas
- Glasgow al ingreso y actual

### Intervenciones
- PIC (Presión Intracraneal)
- ARM (Asistencia Respiratoria Mecánica)
- Craniectomía

### Evolución
- Días de evolución en UTI
- Observaciones adicionales

## 🚀 Instalación Local

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd /home/Agustin/Escritorio/UTI
   ```

2. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

4. **Abrir en el navegador**
   La aplicación se abrirá automáticamente en `http://localhost:8501`

## ☁️ Deploy en Streamlit Cloud (GRATIS)

Para que varios colaboradores puedan acceder desde internet:

### Paso 1: Crear cuenta en GitHub
1. Ve a [github.com](https://github.com) y crea una cuenta gratuita
2. Crea un nuevo repositorio llamado `uti-tec-registro`
3. Sube estos archivos al repositorio

### Paso 2: Deploy en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona tu repositorio `uti-tec-registro`
5. Archivo principal: `app.py`
6. Haz clic en "Deploy"

### Paso 3: Compartir con Colaboradores
Una vez desplegado, obtendrás una URL como:
```
https://tuusuario-uti-tec-registro.streamlit.app
```

Comparte esta URL con tus colaboradores. ¡Todos podrán acceder desde cualquier dispositivo!

## 📖 Guía de Uso

### Cargar un Paciente
1. Selecciona "Cargar Paciente" en el menú lateral
2. Completa todos los campos obligatorios (marcados con *)
3. Haz clic en "Guardar Paciente"

### Ver Estadísticas
1. Selecciona "Ver Estadísticas" en el menú lateral
2. Explora los diferentes gráficos:
   - Origen del TEC
   - Intervenciones realizadas
   - Distribución por edad y sexo
   - Evolución temporal
   - Estadísticas descriptivas

### Consultar Base de Datos
1. Selecciona "Base de Datos" en el menú lateral
2. Usa los filtros para buscar pacientes específicos
3. Selecciona una historia clínica para ver el detalle completo

### Exportar Datos
1. Selecciona "Exportar Datos" en el menú lateral
2. Haz clic en "Descargar CSV"
3. Abre el archivo en Excel o cualquier software estadístico

## 💾 Base de Datos

Los datos se almacenan en un archivo SQLite (`pacientes_tec.db`) que se crea automáticamente al ejecutar la aplicación.

**Importante**: Si haces deploy en Streamlit Cloud, la base de datos se reiniciará cada vez que la app se reinicie. Para producción, se recomienda usar una base de datos externa como:
- **PostgreSQL** (recomendado para producción)
- **MongoDB Atlas** (opción NoSQL)
- **Google Sheets** (opción simple)

## 🔒 Seguridad

Para agregar autenticación (control de usuarios):
1. Instalar: `pip install streamlit-authenticator`
2. Configurar usuarios y contraseñas
3. Proteger el acceso a la aplicación

## 📱 Capturas de Pantalla

La aplicación incluye:
- ✅ Formulario de registro intuitivo
- ✅ Dashboard con gráficos interactivos
- ✅ Tabla de datos con filtros
- ✅ Exportación a CSV/Excel
- ✅ Diseño responsive

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework de aplicación web
- **Pandas**: Análisis y manipulación de datos
- **Plotly**: Gráficos interactivos
- **SQLite**: Base de datos

## 📧 Soporte

Para dudas o problemas:
1. Verifica que todos los archivos estén en la carpeta
2. Asegúrate de tener instaladas todas las dependencias
3. Revisa los mensajes de error en la terminal

## 📄 Licencia

Este proyecto es de uso libre para fines médicos y académicos.

---

**Desarrollado para el seguimiento estadístico de pacientes neurocríticos con TEC en UTI**
# NeurocriticosEstadisticas
