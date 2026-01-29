# 🚀 DEPLOY SÚPER FÁCIL CON SUPABASE

## ⚡ 2 Minutos de Configuración vs 20 de Google Sheets

---

## 📝 PASO 1: Crear Cuenta en Supabase (2 min)

### A. Ir a Supabase
1. Abre: **https://supabase.com**
2. Click en **"Start your project"**
3. Sign up con GitHub (usa tu cuenta `agus2894`)

### B. Crear Proyecto
1. Click en **"New project"**
2. Nombre del proyecto: `uti-tec`
3. Database Password: **crea una contraseña** (guárdala, aunque no la necesitarás después)
4. Region: Selecciona **South America (São Paulo)**
5. Click **"Create new project"**
6. Espera 1-2 minutos mientras se crea

---

## 🗄️ PASO 2: Crear Tablas (3 min)

### A. Ir al SQL Editor
1. En el menú lateral, click en **"SQL Editor"**
2. Click en **"+ New query"**

### B. Copiar y Pegar este SQL

```sql
-- Tabla de pacientes
CREATE TABLE pacientes (
    id BIGSERIAL PRIMARY KEY,
    numero_historia TEXT UNIQUE NOT NULL,
    edad INTEGER NOT NULL,
    sexo TEXT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    diagnostico TEXT NOT NULL,
    origen_tec TEXT NOT NULL,
    lesiones_asociadas TEXT,
    requiere_pic BOOLEAN NOT NULL DEFAULT FALSE,
    requiere_arm BOOLEAN NOT NULL DEFAULT FALSE,
    requiere_cranectomia BOOLEAN NOT NULL DEFAULT FALSE,
    dias_uti INTEGER NOT NULL DEFAULT 0,
    glasgow_ingreso INTEGER NOT NULL,
    glasgow_actual INTEGER NOT NULL,
    destino_post_uti TEXT,
    tiene_drenaje BOOLEAN DEFAULT FALSE,
    tipo_drenaje TEXT,
    llevaba_casco BOOLEAN,
    secuelas_motora BOOLEAN DEFAULT FALSE,
    secuelas_neurologica BOOLEAN DEFAULT FALSE,
    secuelas_cognitiva BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    fecha_registro TIMESTAMPTZ DEFAULT NOW(),
    fecha_ultima_actualizacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de evoluciones
CREATE TABLE evoluciones (
    id BIGSERIAL PRIMARY KEY,
    numero_historia TEXT NOT NULL,
    fecha_evolucion TIMESTAMPTZ DEFAULT NOW(),
    dias_uti INTEGER,
    glasgow_actual INTEGER,
    requiere_pic BOOLEAN,
    requiere_arm BOOLEAN,
    requiere_cranectomia BOOLEAN,
    observacion TEXT,
    FOREIGN KEY (numero_historia) REFERENCES pacientes(numero_historia)
);

-- Índices para mejor performance
CREATE INDEX idx_pacientes_historia ON pacientes(numero_historia);
CREATE INDEX idx_evoluciones_historia ON evoluciones(numero_historia);
```

### C. Ejecutar
1. Click en **"Run"** (o Ctrl+Enter)
2. Debe decir "Success. No rows returned"

---

## 🔑 PASO 3: Obtener Credenciales (1 min)

### A. Ir a Settings
1. En el menú lateral, click en **⚙️ Project Settings**
2. Click en **"API"**

### B. Copiar 2 valores:

1. **Project URL:**
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```
   Copia toda la URL

2. **anon public key:**
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey...
   ```
   Copia toda la clave (es larga, asegúrate de copiarla completa)

---

## 🌐 PASO 4: Deploy en Streamlit Cloud (3 min)

### A. Ir a Streamlit Cloud
1. Ve a: **https://share.streamlit.io**
2. Login con GitHub
3. Click **"New app"**

### B. Configurar
- **Repository:** `agus2894/NeurocriticosEstadisticas`
- **Branch:** `main`
- **Main file path:** `app.py`

### C. Configurar Secrets (SUPER SIMPLE)

Click en **"Advanced settings"**, en la sección **"Secrets"** pega esto:

```toml
supabase_url = "https://xxxxxxxxxxxxx.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey..."
```

**IMPORTANTE:** Reemplaza con TUS valores copiados en el Paso 3

### D. Deploy
1. Click **"Deploy"**
2. Espera 2-3 minutos

---

## ✅ ¡LISTO!

Tu app estará en:
```
https://agus2894-neurocriticosestadisticas-app-abc123.streamlit.app
```

### Verifica:
- Sidebar debe mostrar: **"☁️ Base de Datos: Supabase (PostgreSQL)"**
- ✅ Modo colaborativo activo
- Carga un paciente de prueba
- Los datos se guardan en Supabase (no se pierden nunca)

---

## 📊 Ver tus Datos en Supabase

1. Ve a Supabase Dashboard
2. Click en **"Table Editor"**
3. Selecciona tabla **"pacientes"**
4. Verás todos los datos en tiempo real
5. Puedes editar, exportar, etc.

---

## 🎯 Ventajas de Supabase vs Google Sheets

| Característica | Supabase | Google Sheets |
|---------------|----------|---------------|
| Configuración | 2 minutos | 20 minutos |
| Complejidad | ⭐ Muy fácil | ⭐⭐⭐ Complejo |
| Secrets | 2 líneas | 20 líneas |
| Velocidad | ⚡ Muy rápido | 🐢 Lento |
| Base de datos | PostgreSQL real | Hoja de cálculo |
| Límite gratis | 500 MB | Sin límite técnico |
| Ver datos | Dashboard pro | Google Sheets |

---

## 🆘 Si algo sale mal:

### Error: "relation 'pacientes' does not exist"
- Ve a Supabase SQL Editor
- Ejecuta el SQL del Paso 2 de nuevo

### Error: "Invalid API key"
- Verifica que copiaste la clave `anon public` (no la `service_role`)
- Debe empezar con `eyJ...`

### No se conecta:
- Verifica el URL en secrets
- Debe terminar en `.supabase.co`

---

## 💰 Costo

**TODO GRATIS:**
- ✅ 500 MB de base de datos
- ✅ 2 GB de transferencia/mes
- ✅ Suficiente para miles de pacientes
- ✅ Para siempre

---

## 🎉 Resumen

**Total: 8 minutos** para tener tu app en la nube con base de datos real.

1. ✅ Crear cuenta Supabase (2 min)
2. ✅ Crear tablas con SQL (3 min)
3. ✅ Copiar 2 valores (1 min)
4. ✅ Deploy con 2 líneas de secrets (2 min)

**¡Y LISTO! App en producción.**

Comparte la URL con tu equipo y todos pueden trabajar simultáneamente. Los datos están seguros en PostgreSQL.

---

**¿Necesitas ayuda?** Avísame en qué paso te trabaste.
