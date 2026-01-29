# 🚀 DEPLOY RÁPIDO - 3 PASOS

## ✅ TU APP YA ESTÁ LISTA PARA SUBIR A LA NUBE

### 🎯 Resultado Final:
- URL pública (ej: https://neurocriticos.streamlit.app)
- Todos pueden acceder desde cualquier lugar
- Datos en Google Sheets (persistentes)
- Sin costo

---

## 📝 PASO 1: Subir Código a GitHub (5 min)

### Ya tienes el repo: `agus2894/NeurocriticosEstadisticas`

**Ejecuta estos comandos:**

```bash
cd /home/Agustin/Escritorio/UTI

# Agregar todos los archivos
git add .

# Guardar cambios
git commit -m "App lista para deploy"

# Subir a GitHub
git push origin main
```

Si te pide usuario/contraseña de GitHub, usa tu username y tu **Personal Access Token** (no tu contraseña normal).

---

## 🌐 PASO 2: Deploy en Streamlit Cloud (2 min)

### A. Ir a Streamlit Cloud
1. Abre: **https://share.streamlit.io**
2. Inicia sesión con tu cuenta de GitHub
3. Click en **"New app"**

### B. Configurar el Deploy
Completa el formulario:
- **Repository:** `agus2894/NeurocriticosEstadisticas`
- **Branch:** `main`
- **Main file path:** `app.py`

### C. Deploy
**POR AHORA NO HAGAS CLICK EN "DEPLOY" TODAVÍA**

---

## 📊 PASO 3: Configurar Google Sheets (10 min)

### ¿Por qué Google Sheets?
Sin esto, la app funciona PERO los datos se borran cada vez que Streamlit reinicia el servidor.

### A. Crear Google Sheet
1. Ve a: https://sheets.google.com
2. Click en **"+ Blank"** (hoja en blanco)
3. Nombra la hoja: **"Pacientes TEC UTI"**
4. Copia el **ID del Sheet** de la URL:
   ```
   https://docs.google.com/spreadsheets/d/AQUI_ESTA_EL_ID/edit
   ```
   Guárdalo, lo necesitarás después.

### B. Crear Service Account en Google Cloud

1. Ve a: **https://console.cloud.google.com**

2. **Crear proyecto:**
   - Click en el menú desplegable del proyecto (arriba)
   - Click en "New Project"
   - Nombre: `uti-tec-app`
   - Click "Create"

3. **Habilitar Google Sheets API:**
   - En el menú lateral: **APIs & Services** > **Library**
   - Busca: `Google Sheets API`
   - Click en la API
   - Click **"Enable"**

4. **Crear Service Account:**
   - En el menú lateral: **APIs & Services** > **Credentials**
   - Click **"+ CREATE CREDENTIALS"**
   - Selecciona **"Service Account"**
   - **Service account name:** `streamlit-sheets`
   - Click **"Create and Continue"**
   - **Role:** Selecciona `Editor` (o `Basic` > `Editor`)
   - Click **"Continue"**
   - Click **"Done"**

5. **Generar clave JSON:**
   - Click en el service account que acabas de crear
   - Ve a la pestaña **"Keys"**
   - Click **"Add Key"** > **"Create new key"**
   - Selecciona **JSON**
   - Click **"Create"**
   - **Se descargará un archivo JSON** → GUÁRDALO BIEN

### C. Compartir Google Sheet con Service Account

1. Abre el archivo JSON que descargaste
2. Busca el campo `"client_email"` - se ve así:
   ```
   streamlit-sheets@uti-tec-app.iam.gserviceaccount.com
   ```
3. Copia ese email completo

4. Abre tu Google Sheet (el que creaste en paso A)
5. Click en **"Share"** (Compartir)
6. Pega el email del service account
7. Dale permisos de **Editor**
8. **DESMARCA** "Notify people" (no enviar notificación)
9. Click **"Share"**

### D. Convertir JSON a formato TOML para Streamlit

Abre el archivo JSON descargado y conviértelo a este formato:

```toml
[gcp_service_account]
type = "service_account"
project_id = "uti-tec-app"
private_key_id = "abc123def..."
private_key = "-----BEGIN PRIVATE KEY-----\nTU_CLAVE_COMPLETA_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "streamlit-sheets@uti-tec-app.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

sheet_key = "EL_ID_QUE_COPIASTE_DEL_GOOGLE_SHEET"
```

**IMPORTANTE:** 
- Copia EXACTAMENTE como está en el JSON
- La `private_key` debe mantener los `\n` (saltos de línea)
- Agrega al final la línea `sheet_key` con el ID de tu Sheet

---

## 🎯 PASO 4: Pegar Secrets en Streamlit Cloud

1. Vuelve a la página de deploy de Streamlit: https://share.streamlit.io
2. En la configuración del deploy, click en **"Advanced settings"**
3. En la sección **"Secrets"**, pega TODO el contenido TOML que preparaste arriba
4. Ahora sí, click en **"Deploy"**

---

## ⏰ Esperar 2-5 minutos

Streamlit Cloud va a:
1. Instalar todas las dependencias
2. Conectarse a Google Sheets
3. Iniciar la app

---

## ✅ ¡LISTO!

Tu app estará disponible en una URL como:
```
https://agus2894-neurocriticosestadisticas-app-abc123.streamlit.app
```

### Comparte esa URL con tu equipo y:
- ✅ Todos pueden acceder desde cualquier lugar
- ✅ Los datos se guardan en Google Sheets
- ✅ Pueden trabajar simultáneamente
- ✅ Gratis para siempre
- ✅ Sin mantenimiento

---

## 🆘 Si algo sale mal:

### Error: "Module not found"
- Espera 5 minutos más, aún está instalando

### Error: "Permission denied" en Sheets
- Verifica que compartiste el Sheet con el email correcto
- El email debe tener permisos de Editor

### Error: "Invalid credentials"
- Verifica que copiaste bien el TOML
- La private_key debe tener `\n` exactamente como en el JSON

### Los datos no se guardan:
- Verifica el `sheet_key` en secrets
- Debe ser solo el ID, sin la URL completa

---

## 💡 Tips:

- **Ver los datos:** Abre tu Google Sheet para ver todo en tiempo real
- **Backup:** Google Sheets hace backup automático
- **Editar:** Puedes editar datos directamente en Sheets si necesitas
- **Exportar:** Desde Sheets puedes descargar CSV, Excel, etc.

---

## 📞 Necesitas ayuda?

Si te trabas en algún paso, avísame y te ayudo en vivo.

**¡Tu app estará en la nube en menos de 20 minutos!** 🚀
