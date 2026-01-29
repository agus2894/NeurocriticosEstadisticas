import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import db_adapter as db

# Configuración de la página
st.set_page_config(
    page_title="Registro de Pacientes Neurocriticos - UTI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar base de datos
db.init_db()

# CSS personalizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<p class="main-header">🏥 Registro de Pacientes neurocriticos - UTI</p>', unsafe_allow_html=True)

# Mostrar tipo de base de datos
db_nombre, db_tipo = db.get_db_info()
st.sidebar.markdown(f"**Base de Datos:** {db_nombre}")
st.sidebar.markdown("---")

# Menú lateral
menu = st.sidebar.selectbox(
    "📋 Menú",
    ["Cargar Paciente", "Evolucionar Paciente", "Ver Estadísticas", "Base de Datos", "Exportar Datos"]
)

# ==================== CARGAR PACIENTE ====================
if menu == "Cargar Paciente":
    st.header("📝 Registro de Nuevo Paciente")
    
    with st.form("formulario_paciente"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Datos del Paciente")
            
            # Identificación
            numero_historia = st.text_input("Número de Historia Clínica*", help="Identificador único del paciente")
            edad = st.number_input("Edad*", min_value=0, max_value=120, value=30)
            sexo = st.selectbox("Sexo*", ["Masculino", "Femenino"])
            
            # Datos del TEC
            st.markdown("---")
            st.subheader("Información del TEC")
            
            fecha_ingreso = st.date_input("Fecha de Ingreso*", value=date.today(), max_value=date.today())
            
            diagnostico = st.text_area("Diagnóstico Principal*", 
                                      placeholder="Ej: TEC grave con HSD agudo...",
                                      help="Descripción detallada del diagnóstico")
            
            origen_tec = st.selectbox("Origen del TEC*", [
                "Accidente de tránsito (moto)",
                "Accidente de tránsito (auto)",
                "Accidente de tránsito (peatón)",
                "Caída de altura",
                "Caída mismo nivel",
                "Agresión",
                "Accidente laboral",
                "Otro"
            ])
            
            # Campo de casco - solo para accidentes de moto
            llevaba_casco = None
            if origen_tec == "Accidente de tránsito (moto)":
                st.markdown("**Uso de casco**")
                llevaba_casco = st.radio(
                    "¿Llevaba casco al momento del accidente?",
                    options=[True, False],
                    format_func=lambda x: "Sí, llevaba casco" if x else "No llevaba casco",
                    horizontal=True
                )
            
            if origen_tec == "Otro":
                origen_tec_otro = st.text_input("Especificar origen")
                origen_tec = origen_tec_otro if origen_tec_otro else "Otro"
        
        with col2:
            st.subheader("Lesiones Asociadas")
            
            lesiones = st.multiselect("Otras lesiones/heridas", [
                "Hematoma subdural",
                "Hematoma epidural",
                "Contusión cerebral",
                "Hemorragia subaracnoidea",
                "Fractura de cráneo",
                "Trauma torácico",
                "Trauma abdominal",
                "Fracturas de extremidades",
                "Trauma facial",
                "Lesión medular",
                "Sin otras lesiones"
            ])
            
            otras_lesiones = st.text_area("Otras lesiones no listadas", 
                                         placeholder="Especificar otras lesiones...")
            
            st.markdown("---")
            st.subheader("Intervenciones y Evolución")
            
            # Intervenciones
            requiere_pic = st.checkbox("Requiere PIC (Presión Intracraneal)")
            
            # Drenajes
            tiene_drenaje = st.checkbox("¿Se colocó algún drenaje además de PIC?")
            tipo_drenaje = None
            if tiene_drenaje:
                tipo_drenaje = st.selectbox("Tipo de drenaje*", [
                    "DVE (Drenaje Ventricular Externo)",
                    "Aspirativo"
                ])
            
            requiere_arm = st.checkbox("Requiere ARM (Asistencia Respiratoria Mecánica)")
            requiere_cranectomia = st.checkbox("Requiere Craniectomía")
            
            # Evolución
            dias_uti = st.number_input("Días de evolución en UTI*", min_value=0, value=1, 
                                      help="Días transcurridos en la unidad")
            
            # Glasgow
            glasgow_ingreso = st.slider("Glasgow al ingreso", min_value=3, max_value=15, value=8)
            glasgow_actual = st.slider("Glasgow actual", min_value=3, max_value=15, value=8)
            
            # Destino post-UTI
            st.markdown("---")
            st.subheader("Destino después de UTI")
            destino_post_uti = st.selectbox("¿A dónde fue derivado el paciente?", [
                "Aún en UTI",
                "Cuidados Generales",
                "UTIM",
                "Derivado a otro centro",
                "Óbito"
            ])
            
            # Secuelas
            st.markdown("---")
            st.subheader("Secuelas del Paciente")
            secuelas_motora = st.checkbox("Secuelas motoras")
            secuelas_neurologica = st.checkbox("Secuelas neurológicas")
            secuelas_cognitiva = st.checkbox("Secuelas cognitivas")
            
            # Observaciones
            observaciones = st.text_area("Observaciones adicionales", 
                                        placeholder="Notas adicionales del caso...")
        
        st.markdown("---")
        
        # Botón de envío
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            submitted = st.form_submit_button("💾 Guardar Paciente", use_container_width=True)
        
        if submitted:
            # Validar campos obligatorios
            if not numero_historia or not diagnostico:
                st.error("⚠️ Por favor complete todos los campos obligatorios (*)")
            else:
                # Preparar datos
                lesiones_str = ", ".join(lesiones) if lesiones else ""
                if otras_lesiones:
                    lesiones_str += f" | {otras_lesiones}" if lesiones_str else otras_lesiones
                
                # Guardar en la base de datos
                exito = db.insertar_paciente(
                    numero_historia=numero_historia,
                    edad=edad,
                    sexo=sexo,
                    fecha_ingreso=fecha_ingreso.strftime("%Y-%m-%d"),
                    diagnostico=diagnostico,
                    origen_tec=origen_tec,
                    lesiones_asociadas=lesiones_str,
                    requiere_pic=requiere_pic,
                    requiere_arm=requiere_arm,
                    requiere_cranectomia=requiere_cranectomia,
                    dias_uti=dias_uti,
                    glasgow_ingreso=glasgow_ingreso,
                    glasgow_actual=glasgow_actual,
                    destino_post_uti=destino_post_uti,
                    tiene_drenaje=tiene_drenaje,
                    tipo_drenaje=tipo_drenaje,
                    llevaba_casco=llevaba_casco,
                    secuelas_motora=secuelas_motora,
                    secuelas_neurologica=secuelas_neurologica,
                    secuelas_cognitiva=secuelas_cognitiva,
                    observaciones=observaciones
                )
                
                if exito:
                    st.success("✅ Paciente registrado exitosamente!")
                    st.info("👉 Recargando formulario para nuevo paciente...")
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Error: Ya existe un paciente con ese número de historia clínica")

# ==================== EVOLUCIONAR PACIENTE ====================
elif menu == "Evolucionar Paciente":
    st.header("📈 Evolución de Paciente")
    
    # Obtener lista de pacientes
    df = db.obtener_todos_pacientes()
    
    if df.empty:
        st.warning("⚠️ No hay pacientes registrados aún.")
    else:
        # Seleccionar paciente
        st.subheader("Seleccionar Paciente")
        
        # Crear lista de opciones con HC y nombre para mejor identificación
        opciones_pacientes = [f"{row['numero_historia']} - {row['diagnostico'][:50]}" for _, row in df.iterrows()]
        paciente_seleccionado = st.selectbox(
            "Historia Clínica",
            opciones_pacientes,
            help="Seleccione el paciente a evolucionar"
        )
        
        if paciente_seleccionado:
            # Extraer número de historia
            numero_historia = paciente_seleccionado.split(" - ")[0]
            paciente_df = db.obtener_paciente_por_historia(numero_historia)
            
            if not paciente_df.empty:
                paciente = paciente_df.iloc[0]
                
                # Mostrar información actual del paciente
                st.markdown("---")
                st.subheader("📋 Información Actual")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Edad", f"{paciente['edad']} años")
                with col2:
                    st.metric("Días en UTI", paciente['dias_uti'])
                with col3:
                    st.metric("Glasgow Actual", paciente['glasgow_actual'])
                with col4:
                    st.metric("Glasgow Ingreso", paciente['glasgow_ingreso'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**PIC:** {'✅ Sí' if paciente['requiere_pic'] else '❌ No'}")
                with col2:
                    st.write(f"**ARM:** {'✅ Sí' if paciente['requiere_arm'] else '❌ No'}")
                with col3:
                    st.write(f"**Craniectomía:** {'✅ Sí' if paciente['requiere_cranectomia'] else '❌ No'}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Drenaje:** {'✅ ' + str(paciente.get('tipo_drenaje', 'N/A')) if paciente.get('tiene_drenaje') else '❌ No'}")
                with col2:
                    st.write(f"**Destino:** {paciente.get('destino_post_uti', 'No especificado')}")
                with col3:
                    if "moto" in str(paciente['origen_tec']).lower() and paciente.get('llevaba_casco') is not None:
                        st.write(f"**Casco:** {'✅ Sí' if paciente.get('llevaba_casco') else '❌ No'}")
                
                st.write("**Secuelas:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Motora: {'✅' if paciente.get('secuelas_motora') else '❌'}")
                with col2:
                    st.write(f"Neurológica: {'✅' if paciente.get('secuelas_neurologica') else '❌'}")
                with col3:
                    st.write(f"Cognitiva: {'✅' if paciente.get('secuelas_cognitiva') else '❌'}")
                
                # Formulario de evolución
                st.markdown("---")
                st.subheader("🔄 Actualizar Evolución")
                
                with st.form("formulario_evolucion"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Días en UTI
                        nuevos_dias_uti = st.number_input(
                            "Días de evolución en UTI*",
                            min_value=0,
                            value=int(paciente['dias_uti']),
                            help="Actualizar días totales en UTI"
                        )
                        
                        # Glasgow actual
                        nuevo_glasgow = st.slider(
                            "Glasgow actual*",
                            min_value=3,
                            max_value=15,
                            value=int(paciente['glasgow_actual']),
                            help="Puntaje Glasgow actual del paciente"
                        )
                        
                        # Cambio en Glasgow
                        cambio_glasgow = nuevo_glasgow - paciente['glasgow_actual']
                        if cambio_glasgow > 0:
                            st.success(f"📈 Mejoría de {cambio_glasgow} puntos en Glasgow")
                        elif cambio_glasgow < 0:
                            st.error(f"📉 Deterioro de {abs(cambio_glasgow)} puntos en Glasgow")
                        else:
                            st.info("➡️ Sin cambios en Glasgow")
                    
                    with col2:
                        # Intervenciones
                        st.markdown("**Intervenciones Actuales**")
                        
                        nueva_pic = st.checkbox(
                            "Requiere PIC",
                            value=bool(paciente['requiere_pic'])
                        )
                        
                        # Drenaje
                        nueva_tiene_drenaje = st.checkbox(
                            "¿Tiene drenaje además de PIC?",
                            value=bool(paciente.get('tiene_drenaje', False))
                        )
                        
                        nuevo_tipo_drenaje = None
                        if nueva_tiene_drenaje:
                            tipo_actual = paciente.get('tipo_drenaje', 'DVE (Drenaje Ventricular Externo)')
                            opciones_drenaje = [
                                "DVE (Drenaje Ventricular Externo)",
                                "Aspirativo"
                            ]
                            indice_tipo = 0 if tipo_actual and "DVE" in tipo_actual else 1 if tipo_actual else 0
                            nuevo_tipo_drenaje = st.selectbox(
                                "Tipo de drenaje",
                                opciones_drenaje,
                                index=indice_tipo
                            )
                        
                        nueva_arm = st.checkbox(
                            "Requiere ARM",
                            value=bool(paciente['requiere_arm'])
                        )
                        
                        nueva_cranectomia = st.checkbox(
                            "Requiere Craniectomía",
                            value=bool(paciente['requiere_cranectomia'])
                        )
                        
                        # Destino post-UTI
                        st.markdown("---")
                        st.markdown("**Destino después de UTI**")
                        opciones_destino = [
                            "Aún en UTI",
                            "Cuidados Generales",
                            "UTIM",
                            "Derivado a otro centro",
                            "Óbito"
                        ]
                        destino_actual = paciente.get('destino_post_uti', 'Aún en UTI')
                        indice_destino = opciones_destino.index(destino_actual) if destino_actual in opciones_destino else 0
                        nuevo_destino = st.selectbox(
                            "Destino",
                            opciones_destino,
                            index=indice_destino
                        )
                        
                        # Casco (solo para moto)
                        nuevo_llevaba_casco = None
                        if "moto" in str(paciente['origen_tec']).lower():
                            st.markdown("---")
                            nuevo_llevaba_casco = st.checkbox(
                                "¿Llevaba casco?",
                                value=bool(paciente.get('llevaba_casco', False))
                            )
                        
                        # Secuelas
                        st.markdown("---")
                        st.markdown("**Secuelas del Paciente**")
                        nueva_secuela_motora = st.checkbox(
                            "Secuelas motoras",
                            value=bool(paciente.get('secuelas_motora', False))
                        )
                        nueva_secuela_neurologica = st.checkbox(
                            "Secuelas neurológicas",
                            value=bool(paciente.get('secuelas_neurologica', False))
                        )
                        nueva_secuela_cognitiva = st.checkbox(
                            "Secuelas cognitivas",
                            value=bool(paciente.get('secuelas_cognitiva', False))
                        )
                    
                    # Observaciones de evolución
                    st.markdown("---")
                    st.markdown("**Observaciones de Evolución**")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.text_area(
                            "Observaciones anteriores (Solo lectura)",
                            value=paciente['observaciones'] if paciente['observaciones'] else "Sin observaciones previas",
                            disabled=True,
                            height=100
                        )
                    
                    with col2:
                        nueva_observacion = st.text_area(
                            "Nueva observación*",
                            placeholder="Ej: Paciente presenta mejoría clínica, disminución de sedación...",
                            help="Agregue notas sobre la evolución actual",
                            height=100
                        )
                    
                    st.markdown("---")
                    
                    # Botón de actualización
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    with col_btn2:
                        actualizar = st.form_submit_button(
                            "💾 Actualizar Evolución",
                            use_container_width=True
                        )
                    
                    if actualizar:
                        if not nueva_observacion:
                            st.error("⚠️ Por favor agregue una observación de la evolución")
                        else:
                            # Preparar observaciones actualizadas
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            observaciones_actualizadas = paciente['observaciones'] if paciente['observaciones'] else ""
                            observaciones_actualizadas += f"\n\n[{timestamp}] {nueva_observacion}"
                            
                            # Actualizar en base de datos
                            exito = db.actualizar_paciente(
                                numero_historia=numero_historia,
                                dias_uti=nuevos_dias_uti,
                                glasgow_actual=nuevo_glasgow,
                                requiere_pic=nueva_pic,
                                requiere_arm=nueva_arm,
                                requiere_cranectomia=nueva_cranectomia,
                                tiene_drenaje=nueva_tiene_drenaje,
                                tipo_drenaje=nuevo_tipo_drenaje,
                                destino_post_uti=nuevo_destino,
                                llevaba_casco=nuevo_llevaba_casco,
                                secuelas_motora=nueva_secuela_motora,
                                secuelas_neurologica=nueva_secuela_neurologica,
                                secuelas_cognitiva=nueva_secuela_cognitiva,
                                observaciones=observaciones_actualizadas
                            )
                            
                            if exito:
                                st.success("✅ Evolución actualizada exitosamente!")
                                st.rerun()
                            else:
                                st.error("❌ Error al actualizar la evolución")

# ==================== ESTADÍSTICAS ====================
elif menu == "Ver Estadísticas":
    st.header("📊 Estadísticas y Análisis")
    
    # Obtener datos
    df = db.obtener_todos_pacientes()
    
    if df.empty:
        st.warning("⚠️ No hay datos registrados aún. Comience cargando pacientes.")
    else:
        # Métricas principales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Pacientes", len(df))
        with col2:
            st.metric("Con PIC", df['requiere_pic'].sum())
        with col3:
            st.metric("Con ARM", df['requiere_arm'].sum())
        with col4:
            st.metric("Craniectomía", df['requiere_cranectomia'].sum())
        with col5:
            drenajes = df['tiene_drenaje'].sum() if 'tiene_drenaje' in df.columns else 0
            st.metric("Con Drenaje", drenajes)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Origen del TEC
            st.subheader("Origen del TEC")
            origen_counts = df['origen_tec'].value_counts()
            fig1 = px.pie(values=origen_counts.values, names=origen_counts.index, 
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
            
            # Distribución por sexo
            st.subheader("Distribución por Sexo")
            sexo_counts = df['sexo'].value_counts()
            fig3 = px.bar(x=sexo_counts.index, y=sexo_counts.values,
                         labels={'x': 'Sexo', 'y': 'Cantidad'},
                         color=sexo_counts.index,
                         color_discrete_map={'Masculino': '#1f77b4', 'Femenino': '#ff7f0e'})
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Intervenciones
            st.subheader("Intervenciones Realizadas")
            intervenciones = {
                'PIC': df['requiere_pic'].sum(),
                'ARM': df['requiere_arm'].sum(),
                'Craniectomía': df['requiere_cranectomia'].sum()
            }
            if 'tiene_drenaje' in df.columns:
                intervenciones['Drenaje'] = df['tiene_drenaje'].sum()
            
            fig2 = px.bar(x=list(intervenciones.keys()), y=list(intervenciones.values()),
                         labels={'x': 'Intervención', 'y': 'Cantidad de Pacientes'},
                         color=list(intervenciones.keys()),
                         color_discrete_sequence=['#2ca02c', '#d62728', '#9467bd', '#8c564b'])
            st.plotly_chart(fig2, use_container_width=True)
            
            # Distribución de edad
            st.subheader("Distribución por Edad")
            fig4 = px.histogram(df, x='edad', nbins=20,
                              labels={'edad': 'Edad', 'count': 'Frecuencia'},
                              color_discrete_sequence=['#17becf'])
            st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("---")
        
        # Gráficos adicionales
        col1, col2 = st.columns(2)
        
        with col1:
            # Glasgow al ingreso
            st.subheader("Glasgow al Ingreso")
            fig5 = px.histogram(df, x='glasgow_ingreso', nbins=13,
                              labels={'glasgow_ingreso': 'Puntaje Glasgow', 'count': 'Frecuencia'},
                              color_discrete_sequence=['#bcbd22'])
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # Días en UTI
            st.subheader("Días de Evolución en UTI")
            fig6 = px.box(df, y='dias_uti',
                         labels={'dias_uti': 'Días'},
                         color_discrete_sequence=['#e377c2'])
            st.plotly_chart(fig6, use_container_width=True)
        
        st.markdown("---")
        
        # Evolución temporal
        st.subheader("Ingresos a lo largo del tiempo")
        df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'])
        ingresos_tiempo = df.groupby(df['fecha_ingreso'].dt.to_period('M')).size().reset_index()
        ingresos_tiempo.columns = ['Mes', 'Cantidad']
        ingresos_tiempo['Mes'] = ingresos_tiempo['Mes'].astype(str)
        
        fig7 = px.line(ingresos_tiempo, x='Mes', y='Cantidad',
                      labels={'Mes': 'Mes', 'Cantidad': 'Número de Ingresos'},
                      markers=True)
        st.plotly_chart(fig7, use_container_width=True)
        
        # Nuevos gráficos para campos agregados
        st.markdown("---")
        st.subheader("📊 Análisis de Nuevos Indicadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Destino post-UTI
            if 'destino_post_uti' in df.columns:
                st.subheader("Destino después de UTI")
                destino_counts = df['destino_post_uti'].value_counts()
                fig8 = px.pie(values=destino_counts.values, names=destino_counts.index,
                            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig8.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig8, use_container_width=True)
            
            # Tipos de drenaje
            if 'tipo_drenaje' in df.columns:
                st.subheader("Tipos de Drenaje Utilizados")
                df_con_drenaje = df[df['tiene_drenaje'] == True]
                if len(df_con_drenaje) > 0:
                    drenaje_counts = df_con_drenaje['tipo_drenaje'].value_counts()
                    fig9 = px.bar(x=drenaje_counts.index, y=drenaje_counts.values,
                                labels={'x': 'Tipo de Drenaje', 'y': 'Cantidad'},
                                color=drenaje_counts.index,
                                color_discrete_sequence=['#ff9999', '#66b3ff'])
                    st.plotly_chart(fig9, use_container_width=True)
                else:
                    st.info("No hay pacientes con drenaje registrado")
        
        with col2:
            # Uso de casco en accidentes de moto
            if 'llevaba_casco' in df.columns:
                st.subheader("Uso de Casco en Accidentes de Moto")
                df_motos = df[df['origen_tec'].str.contains('moto', case=False, na=False)]
                
                if len(df_motos) > 0:
                    # Contar casos con y sin casco
                    casco_counts = df_motos['llevaba_casco'].value_counts()
                    
                    # Crear labels personalizados
                    labels = []
                    values = []
                    colors = []
                    
                    if True in casco_counts.index:
                        labels.append(f'Con casco ({casco_counts[True]})')
                        values.append(casco_counts[True])
                        colors.append('#2ecc71')  # Verde
                    
                    if False in casco_counts.index:
                        labels.append(f'Sin casco ({casco_counts[False]})')
                        values.append(casco_counts[False])
                        colors.append('#e74c3c')  # Rojo
                    
                    fig_casco = px.pie(
                        values=values, 
                        names=labels,
                        title=f"Total accidentes de moto: {len(df_motos)}",
                        color_discrete_sequence=colors
                    )
                    fig_casco.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_casco, use_container_width=True)
                    
                    # Métricas adicionales
                    col_a, col_b = st.columns(2)
                    with col_a:
                        pct_con_casco = (casco_counts.get(True, 0) / len(df_motos) * 100)
                        st.metric("% Con casco", f"{pct_con_casco:.1f}%")
                    with col_b:
                        pct_sin_casco = (casco_counts.get(False, 0) / len(df_motos) * 100)
                        st.metric("% Sin casco", f"{pct_sin_casco:.1f}%")
                else:
                    st.info("No hay accidentes de moto registrados")
            
            # Secuelas
            if all(col in df.columns for col in ['secuelas_motora', 'secuelas_neurologica', 'secuelas_cognitiva']):
                st.subheader("Secuelas Presentadas")
                secuelas_data = {
                    'Motora': df['secuelas_motora'].sum(),
                    'Neurológica': df['secuelas_neurologica'].sum(),
                    'Cognitiva': df['secuelas_cognitiva'].sum()
                }
                fig10 = px.bar(x=list(secuelas_data.keys()), y=list(secuelas_data.values()),
                             labels={'x': 'Tipo de Secuela', 'y': 'Cantidad de Pacientes'},
                             color=list(secuelas_data.keys()),
                             color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1'])
                st.plotly_chart(fig10, use_container_width=True)
            
            # Uso de casco en accidentes de moto
            if 'llevaba_casco' in df.columns:
                st.subheader("Uso de Casco en Accidentes de Moto")
                df_motos = df[df['origen_tec'].str.contains('moto', case=False, na=False)]
                if len(df_motos) > 0 and df_motos['llevaba_casco'].notna().any():
                    casco_counts = df_motos['llevaba_casco'].value_counts()
                    labels_casco = ['Con Casco' if x else 'Sin Casco' for x in casco_counts.index]
                    fig11 = px.pie(values=casco_counts.values, names=labels_casco,
                                 color_discrete_map={'Con Casco': '#2ecc71', 'Sin Casco': '#e74c3c'})
                    fig11.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig11, use_container_width=True)
                else:
                    st.info("No hay datos de uso de casco registrados")
        
        # Estadísticas descriptivas
        st.markdown("---")
        st.subheader("📈 Estadísticas Descriptivas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Edad**")
            st.write(f"Media: {df['edad'].mean():.1f} años")
            st.write(f"Mediana: {df['edad'].median():.1f} años")
            st.write(f"Rango: {df['edad'].min()}-{df['edad'].max()} años")
        
        with col2:
            st.write("**Días en UTI**")
            st.write(f"Media: {df['dias_uti'].mean():.1f} días")
            st.write(f"Mediana: {df['dias_uti'].median():.1f} días")
            st.write(f"Máximo: {df['dias_uti'].max()} días")
        
        with col3:
            st.write("**Glasgow al Ingreso**")
            st.write(f"Media: {df['glasgow_ingreso'].mean():.1f}")
            st.write(f"Mediana: {df['glasgow_ingreso'].median():.1f}")
            st.write(f"Moda: {df['glasgow_ingreso'].mode()[0]}")

# ==================== BASE DE DATOS ====================
elif menu == "Base de Datos":
    st.header("🗃️ Base de Datos de Pacientes")
    
    df = db.obtener_todos_pacientes()
    
    if df.empty:
        st.info("ℹ️ No hay pacientes registrados aún.")
    else:
        st.write(f"**Total de registros:** {len(df)}")
        
        # Filtros
        with st.expander("🔍 Filtros"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filtro_sexo = st.multiselect("Sexo", df['sexo'].unique())
            with col2:
                filtro_pic = st.selectbox("PIC", ["Todos", "Sí", "No"])
            with col3:
                filtro_arm = st.selectbox("ARM", ["Todos", "Sí", "No"])
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if filtro_sexo:
            df_filtrado = df_filtrado[df_filtrado['sexo'].isin(filtro_sexo)]
        
        if filtro_pic != "Todos":
            df_filtrado = df_filtrado[df_filtrado['requiere_pic'] == (filtro_pic == "Sí")]
        
        if filtro_arm != "Todos":
            df_filtrado = df_filtrado[df_filtrado['requiere_arm'] == (filtro_arm == "Sí")]
        
        # Mostrar tabla
        st.dataframe(df_filtrado, use_container_width=True, height=400)
        
        # Ver detalle de un paciente
        st.markdown("---")
        st.subheader("Ver Detalle del Paciente")
        
        historias = df_filtrado['numero_historia'].tolist()
        if historias:
            historia_seleccionada = st.selectbox("Seleccionar Historia Clínica", historias)
            
            paciente = df_filtrado[df_filtrado['numero_historia'] == historia_seleccionada].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Historia Clínica:** {paciente['numero_historia']}")
                st.write(f"**Edad:** {paciente['edad']} años")
                st.write(f"**Sexo:** {paciente['sexo']}")
                st.write(f"**Fecha Ingreso:** {paciente['fecha_ingreso']}")
                st.write(f"**Diagnóstico:** {paciente['diagnostico']}")
                st.write(f"**Origen TEC:** {paciente['origen_tec']}")
            
            with col2:
                st.write(f"**Lesiones Asociadas:** {paciente['lesiones_asociadas']}")
                st.write(f"**PIC:** {'Sí' if paciente['requiere_pic'] else 'No'}")
                st.write(f"**ARM:** {'Sí' if paciente['requiere_arm'] else 'No'}")
                st.write(f"**Craniectomía:** {'Sí' if paciente['requiere_cranectomia'] else 'No'}")
                st.write(f"**Días en UTI:** {paciente['dias_uti']}")
                st.write(f"**Glasgow Ingreso:** {paciente['glasgow_ingreso']}")
                st.write(f"**Glasgow Actual:** {paciente['glasgow_actual']}")
            
            # Nueva información agregada
            st.markdown("---")
            st.subheader("Información Adicional")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'destino_post_uti' in paciente.index and paciente['destino_post_uti']:
                    st.write(f"**Destino post-UTI:** {paciente['destino_post_uti']}")
                
                if 'tiene_drenaje' in paciente.index:
                    drenaje_info = "No"
                    if paciente['tiene_drenaje']:
                        tipo = paciente.get('tipo_drenaje', 'No especificado')
                        drenaje_info = f"Sí - {tipo}"
                    st.write(f"**Drenaje:** {drenaje_info}")
                
                if 'llevaba_casco' in paciente.index and paciente['llevaba_casco'] is not None:
                    st.write(f"**Llevaba casco:** {'Sí' if paciente['llevaba_casco'] else 'No'}")
            
            with col2:
                if any(col in paciente.index for col in ['secuelas_motora', 'secuelas_neurologica', 'secuelas_cognitiva']):
                    st.write("**Secuelas:**")
                    secuelas = []
                    if paciente.get('secuelas_motora'):
                        secuelas.append("Motora")
                    if paciente.get('secuelas_neurologica'):
                        secuelas.append("Neurológica")
                    if paciente.get('secuelas_cognitiva'):
                        secuelas.append("Cognitiva")
                    
                    if secuelas:
                        for s in secuelas:
                            st.write(f"  • {s}")
                    else:
                        st.write("  • Sin secuelas registradas")
            
            if paciente['observaciones']:
                st.write(f"**Observaciones:** {paciente['observaciones']}")

# ==================== EXPORTAR ====================
elif menu == "Exportar Datos":
    st.header("📥 Exportar Datos")
    
    df = db.obtener_todos_pacientes()
    
    if df.empty:
        st.warning("⚠️ No hay datos para exportar.")
    else:
        st.write(f"**Total de registros:** {len(df)}")
        
        # Exportar a CSV
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📊 Descargar CSV",
            data=csv,
            file_name=f"pacientes_tec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.info("💡 El archivo CSV se puede abrir en Excel, Google Sheets o cualquier software de análisis estadístico.")
        
        # Vista previa
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head(10), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Sistema de Registro de Pacientes con TEC - UTI</p>
        <p style='font-size: 0.9rem;'>Desarrollado para el seguimiento estadístico de pacientes neurocríticos 2026</p>
        <p style='font-size: 0.8rem;'>© Desarrollador Lamas Gonzalo - Todos los derechos reservados</p>
    </div>
""", unsafe_allow_html=True)
