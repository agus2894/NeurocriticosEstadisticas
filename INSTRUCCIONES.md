# 📖 Instrucciones de Uso - Sistema TEC

## 🚀 Iniciar la Aplicación

Desde la carpeta UTI, ejecutar:
```bash
./iniciar.sh
```

O manualmente:
```bash
source venv/bin/activate
streamlit run app.py
```

La aplicación se abrirá en: **http://localhost:8501**

---

## 📋 Funcionalidades

### 1️⃣ Cargar Paciente
**Usar para:** Registrar un nuevo paciente con TEC

**Pasos:**
1. Completar datos del paciente (HC, edad, sexo)
2. Ingresar diagnóstico y origen del TEC
3. Seleccionar lesiones asociadas
4. Marcar intervenciones necesarias (PIC, ARM, Craniectomía)
5. Ingresar Glasgow de ingreso y actual
6. Agregar observaciones
7. Hacer clic en "Guardar Paciente"

**Campos obligatorios:** Marcados con (*)

---

### 2️⃣ Evolucionar Paciente
**Usar para:** Actualizar la evolución de un paciente existente

**Pasos:**
1. Seleccionar el paciente de la lista desplegable
2. Revisar la información actual
3. Actualizar:
   - Días de evolución en UTI
   - Glasgow actual (muestra si mejoró o deterioró)
   - Intervenciones actuales (PIC, ARM, Craniectomía)
4. **IMPORTANTE:** Agregar observación de la evolución actual
5. Hacer clic en "Actualizar Evolución"

**Ventajas:**
- ✅ Muestra cambios en Glasgow (mejoría/deterioro)
- ✅ Mantiene historial completo de observaciones
- ✅ Registra evolución con fecha y hora automática
- ✅ Actualiza estadísticas en tiempo real

---

### 3️⃣ Ver Estadísticas
**Usar para:** Analizar datos y tendencias

**Incluye:**
- 📊 Total de pacientes, con PIC, ARM, Craniectomía
- 🥧 Gráfico circular: Origen del TEC
- 📈 Gráfico de barras: Intervenciones realizadas
- 👥 Distribución por sexo y edad
- 🧠 Distribución de Glasgow al ingreso
- 📅 Evolución temporal de ingresos
- 📊 Estadísticas descriptivas (media, mediana, rangos)

**Ideal para:** Presentación de resultados fin de año

---

### 4️⃣ Base de Datos
**Usar para:** Consultar registros individuales

**Funciones:**
- Ver tabla completa de pacientes
- Filtrar por sexo, PIC, ARM
- Ver detalle completo de cada paciente
- Consultar historia clínica específica

---

### 5️⃣ Exportar Datos
**Usar para:** Descargar datos para análisis externo

**Formato:** CSV (compatible con Excel, SPSS, R, Python)

**Incluye:** Todos los campos de todos los pacientes

---

## 💡 Consejos de Uso

### Para Cargar Pacientes:
- ✅ Usar número de HC como identificador único
- ✅ Ser específico en el diagnóstico
- ✅ Seleccionar todas las lesiones aplicables
- ✅ Actualizar observaciones regularmente

### Para Evolucionar Pacientes:
- ✅ Siempre agregar observación al actualizar
- ✅ Revisar cambios en Glasgow (código de colores)
- ✅ Actualizar días de UTI diariamente
- ✅ Modificar intervenciones según evolución

### Para Estadísticas:
- ✅ Cargar mínimo 5-10 pacientes para gráficos significativos
- ✅ Exportar datos periódicamente como respaldo
- ✅ Tomar capturas de gráficos para presentaciones

---

## 🔐 Datos Seguros

- Los datos se guardan en `pacientes_tec.db`
- Se recomienda hacer backup periódico de este archivo
- Para respaldar: Copiar `pacientes_tec.db` a otro lugar

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo editar un paciente cargado por error?**
R: Sí, use "Evolucionar Paciente" para actualizar datos. Los datos de ingreso (HC, edad, sexo, fecha ingreso) no se modifican.

**P: ¿Cómo veo el historial de evoluciones?**
R: En "Base de Datos" > Seleccionar paciente > Ver observaciones completas

**P: ¿Puedo eliminar un paciente?**
R: Actualmente no desde la interfaz. Contactar al administrador si es necesario.

**P: ¿Los datos se pierden al cerrar?**
R: No, quedan guardados en la base de datos local.

**P: ¿Varios usuarios pueden cargar a la vez?**
R: En modo local, un usuario a la vez. Para multi-usuario, se debe hacer deploy en la nube.

---

## 🆘 Soporte

**Problema:** No inicia la aplicación
- Verificar que esté en la carpeta UTI
- Ejecutar: `./iniciar.sh`

**Problema:** Error al guardar
- Verificar que el número de HC no exista
- Completar todos los campos obligatorios

**Problema:** No se ven los gráficos
- Cargar más pacientes (mínimo 3-5)
- Verificar conexión a internet (para librerías de gráficos)

---

**Desarrollado para UTI - Registro de pacientes neurocríticos con TEC**
