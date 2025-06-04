
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ---------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------
st.set_page_config(
    page_title="Evolución del Empleo",
    page_icon="📈", 
    layout="wide"
)

# ---------------------------
# CARGA DE DATOS CON INDICADOR
# ---------------------------
@st.cache_data
def cargar_datos():
    with st.spinner('📊 Cargando datos de empleo...'):
        return pd.read_csv("Inicio/data/dataset_final_formateado.csv", parse_dates=["fecha"])

@st.cache_data
def cargar_geodatos():
    with st.spinner('🗺️ Cargando datos geográficos...'):
        gdf_ccaa = gpd.read_file("Inicio/src/mapa/se89_3_admin_ccaa_a_x.shp")
        gdf_prov = gpd.read_file("Inicio/src/mapa/recintos_provinciales_inspire_peninbal_etrs89.shp")
        return gdf_ccaa, gdf_prov

# Cargar datos
df = cargar_datos()
gdf_ccaa, gdf_prov = cargar_geodatos()

# ---------------------------
# EQUIVALENCIAS DE PROVINCIAS
# ---------------------------
equivalencias_provincias = {
    'Almería': 'Almería', 'Cádiz': 'Cádiz', 'Córdoba': 'Córdoba', 'Granada': 'Granada',
    'Huelva': 'Huelva', 'Jaén': 'Jaén', 'Málaga': 'Málaga', 'Sevilla': 'Sevilla',
    'Huesca': 'Huesca', 'Teruel': 'Teruel', 'Zaragoza': 'Zaragoza', 'Asturias': 'Asturias',
    'Balears, Illes': 'Illes Balears', 'Palmas, Las': 'Las Palmas',
    'Santa Cruz de Tenerife': 'Santa Cruz de Tenerife', 'Cantabria': 'Cantabria',
    'Ávila': 'Ávila', 'Burgos': 'Burgos', 'León': 'León', 'Palencia': 'Palencia',
    'Salamanca': 'Salamanca', 'Segovia': 'Segovia', 'Soria': 'Soria', 'Valladolid': 'Valladolid',
    'Zamora': 'Zamora', 'Albacete': 'Albacete', 'Ciudad Real': 'Ciudad Real', 'Cuenca': 'Cuenca',
    'Guadalajara': 'Guadalajara', 'Toledo': 'Toledo', 'Barcelona': 'Barcelona',
    'Girona': 'Girona', 'Lleida': 'Lleida', 'Tarragona': 'Tarragona',
    'Alicante/Alacant': 'Alacant/Alicante', 'Castellón/Castelló': 'Castelló/Castellón',
    'Valencia/Valéncia': 'València/Valencia', 'Badajoz': 'Badajoz', 'Cáceres': 'Cáceres',
    'Coruña, A': 'A Coruña', 'Lugo': 'Lugo', 'Ourense': 'Ourense', 'Pontevedra': 'Pontevedra',
    'Madrid': 'Madrid', 'Murcia': 'Murcia', 'Navarra': 'Navarra', 'Araba/Álava': 'Araba/Álava',
    'Gipuzkoa': 'Gipuzkoa', 'Bizkaia': 'Bizkaia', 'Rioja, La': 'La Rioja',
    'Ceuta': 'Ceuta', 'Melilla': 'Melilla'
}

# ---------------------------
# TÍTULO Y DESCRIPCIÓN
# ---------------------------
st.title("📈 Análisis de la Evolución del Empleo en España")
st.markdown("### Período 2010-2025")

st.markdown("""
<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;">
    <h4>🎯 Objetivos a analizar</h4>
    <ul>
        <li><strong>Evolución temporal:</strong> Tendencias de contratos y demandantes de empleo a lo largo del tiempo</li>
        <li><strong>Análisis estacional:</strong> Patrones mensuales en el mercado laboral</li>
        <li><strong>Visualización geográfica:</strong> Comparativa entre comunidades autónomas y provincias</li>
        <li><strong>Indicadores avanzados:</strong> Índices de inserción laboral y estabilidad contractual</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)


# ---------------------------
# GRÁFICA TEMPORAL
# ---------------------------
st.subheader("Evolución Temporal: Contratos vs Demandantes de Empleo")

with st.spinner('Generando gráfica de evolución temporal...'):
    df_agg = df.groupby("fecha")[["total_contratos", "total_dtes_empleo"]].sum().reset_index()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_agg["fecha"], 
        y=df_agg["total_contratos"],
        mode='lines+markers', 
        name="Total Contratos", 
        line=dict(color="#1f77b4", width=3),
        hovertemplate="<b>Contratos</b><br>Fecha: %{x}<br>Cantidad: %{y:,.0f}<extra></extra>"
    ))
    fig1.add_trace(go.Scatter(
        x=df_agg["fecha"], 
        y=df_agg["total_dtes_empleo"],
        mode='lines+markers', 
        name="Demandantes de Empleo", 
        line=dict(color="#E3962B", dash="dot", width=3),
        hovertemplate="<b>Demandantes</b><br>Fecha: %{x}<br>Cantidad: %{y:,.0f}<extra></extra>"
    ))
    fig1.update_layout(
        title={
            'text': "Evolución Temporal del Mercado Laboral Español (2010-2025)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title="Período", 
        yaxis_title="Número de Personas",
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

st.plotly_chart(fig1, use_container_width=True)

col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)

with col_insight1:
    max_contratos = df_agg["total_contratos"].max()
    fecha_max_contratos = df_agg.loc[df_agg["total_contratos"].idxmax(), "fecha"].strftime("%B %Y")
    st.metric("🔝 Pico de Contratos", f"{max_contratos:,.0f}", f"en {fecha_max_contratos}")

with col_insight2:
    min_contratos = df_agg["total_contratos"].min()
    fecha_min_contratos = df_agg.loc[df_agg["total_contratos"].idxmin(), "fecha"].strftime("%B %Y")
    st.metric("📉 Mínimo de Contratos", f"{min_contratos:,.0f}", f"en {fecha_min_contratos}")

with col_insight3:
    min_demandantes = df_agg["total_dtes_empleo"].min()
    fecha_min_demandantes = df_agg.loc[df_agg["total_dtes_empleo"].idxmin(), "fecha"].strftime("%B %Y")
    st.metric("📉 Menor Demanda", f"{min_demandantes:,.0f}", f"en {fecha_min_demandantes}")

with col_insight4:
    max_demandantes = df_agg["total_dtes_empleo"].max()
    fecha_max_demandantes = df_agg.loc[df_agg["total_dtes_empleo"].idxmax(), "fecha"].strftime("%B %Y")
    st.metric("📈 Mayor Demanda", f"{max_demandantes:,.0f}", f"en {fecha_max_demandantes}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)


# ---------------------------
# PROMEDIO MENSUAL
# ---------------------------
st.subheader("Análisis Estacional: Patrones Mensuales del Empleo")

with st.spinner('Calculando promedios mensuales...'):
    df["mes_nombre"] = df["fecha"].dt.month_name()
    meses_espanol = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
        'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
        'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    
    orden_meses = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    df_mensual = df.groupby("mes_nombre")[["total_contratos", "total_dtes_empleo"]].mean().reindex(orden_meses)
    df_mensual.index = [meses_espanol[mes] for mes in df_mensual.index]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_mensual.index, 
        y=df_mensual["total_contratos"], 
        name="Contratos", 
        marker_color="#1f77b4",
        hovertemplate="<b>Contratos</b><br>Mes: %{x}<br>Promedio: %{y:,.0f}<extra></extra>"
    ))
    fig2.add_trace(go.Bar(
        x=df_mensual.index, 
        y=df_mensual["total_dtes_empleo"], 
        name="Demandantes", 
        marker_color="#E3962B",
        hovertemplate="<b>Demandantes</b><br>Mes: %{x}<br>Promedio: %{y:,.0f}<extra></extra>"
    ))
    fig2.update_layout(
        barmode="group", 
        title={
            'text': "Patrones Estacionales - Promedio Mensual (2010-2025)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title="Meses del Año", 
        yaxis_title="Promedio de Personas",
        height=500,
        showlegend=True
    )

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div style="background-color: #e8f4fd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4; margin: 1rem 0;">
    <h5>🔍 Insight Estacional</h5>
    <p>Los datos muestran un patrón estacional claro: <strong>los contratos tienden a caer en agosto</strong> debido al período vacacional, 
    para luego experimentar un <strong>repunte significativo en septiembre</strong> con la vuelta de las vacaciones y el inicio del curso escolar. 
    Este comportamiento refleja la fuerte influencia del período estival en el mercado laboral español, donde muchas empresas reducen 
    su actividad de contratación durante el mes de agosto.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)


# ---------------------------
# MAPAS INTERACTIVOS
# ---------------------------
st.subheader("🗺️ Análisis Geográfico")
st.markdown("<br><br>", unsafe_allow_html=True)


col_control1, col_control2, col_control3 = st.columns([2, 2, 1])

with col_control1:
    indicador = st.radio(
        "📊 Selecciona el indicador a visualizar:",
        ["Contratos", "Demandantes", "Índice Inserción", "Índice Estabilidad"],
        horizontal=True
    )

with col_control2:
    años_disponibles = sorted(df["año"].unique(), reverse=True)
    modo_comparacion = st.radio("🔍 Modo de análisis:", ["Un solo año", "Comparativa multi-año"])

with col_control3:
    if modo_comparacion == "Un solo año":
        años_seleccionados = [st.selectbox("Año:", años_disponibles)]
    else:
        años_seleccionados = st.multiselect(
            "Años a comparar:",
            años_disponibles,
            default=años_disponibles[:2] if len(años_disponibles) >= 2 else años_disponibles,
            max_selections=4,
            help="Selecciona entre 2 y 4 años para comparar (máximo 4 para mejor visualización)"
        )

with st.expander("¿Qué significan estos índices? - Haz clic para expandir"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Índice de Inserción Laboral**
        
        `Índice = Total Contratos ÷ Total Demandantes`
        
        - **Qué mide:** La capacidad del mercado laboral para absorber a los demandantes de empleo
        - **Interpretación:**
          - Valor > 1: Más contratos que demandantes (mercado favorable)
          - Valor = 1: Equilibrio perfecto
          - Valor < 1: Más demandantes que contratos (mercado tensionado)
        - **Ejemplo:** Un índice de 0.8 significa que por cada 10 demandantes, se generan 8 contratos
        """)
    
    with col2:
        st.markdown("""
        **Índice de Estabilidad Contractual**
        
        `Índice = Contratos Indefinidos ÷ Total Contratos`
        
        - **Qué mide:** La proporción de empleo estable vs temporal
        - **Interpretación:**
          - Valor alto (>0.5): Alta estabilidad laboral
          - Valor medio (0.3-0.5): Estabilidad moderada
          - Valor bajo (<0.3): Predominio de temporalidad
        - **Ejemplo:** Un índice de 0.4 significa que el 40% de los contratos son indefinidos
        """)

if not años_seleccionados:
    st.warning("Por favor, selecciona al menos un año para visualizar.")
    st.stop()

# ---------------------------
# PROCESAMIENTO DE DATOS PARA MAPAS
# ---------------------------
def procesar_datos_mapa(df, años, indicador):
    """Procesa los datos según el indicador seleccionado"""
    df_filtered = df[df["año"].isin(años)].copy()
    
    if indicador == "Contratos":
        color_col = "total_contratos"
        color_scale = "YlGnBu"
        titulo_base = "Total de Contratos"
        df_filtered[color_col] = df_filtered["total_contratos"]
        formato_hover = "{:,.0f} contratos"
        
    elif indicador == "Demandantes":
        color_col = "total_dtes_empleo"
        color_scale = "OrRd"
        titulo_base = "Total de Demandantes de Empleo"
        df_filtered[color_col] = df_filtered["total_dtes_empleo"]
        formato_hover = "{:,.0f} demandantes"
        
    elif indicador == "Índice Inserción":
        color_col = "indice_insercion"
        color_scale = "RdYlGn"
        titulo_base = "Índice de Inserción Laboral"
        df_filtered = df_filtered[df_filtered["total_dtes_empleo"] > 0]
        df_filtered[color_col] = df_filtered["total_contratos"] / df_filtered["total_dtes_empleo"]
        formato_hover = "{:.2f}"
        
    elif indicador == "Índice Estabilidad":
        color_col = "indice_estabilidad"
        color_scale = "RdYlGn"
        titulo_base = "Índice de Estabilidad Contractual"
        df_filtered = df_filtered[df_filtered["total_contratos"] > 0]
        indef = (
            df_filtered["contratos_iniciales_indefinidos_hombres"] +
            df_filtered["contratos_convertidos_en_indefinidos_hombres"] +
            df_filtered["contratos_iniciales_indefinidos_mujeres"] +
            df_filtered["contratos_convertidos_en_indefinidos_mujeres"]
        )
        df_filtered[color_col] = indef / df_filtered["total_contratos"]
        formato_hover = "{:.2%}"
    
    return df_filtered, color_col, color_scale, titulo_base, formato_hover

# ---------------------------
# VISUALIZACIÓN DE MAPAS
# ---------------------------
with st.spinner('Generando mapas interactivos...'):
    if modo_comparacion == "Un solo año":
        # Modo un solo año
        año = años_seleccionados[0]
        df_year, color_col, color_scale, titulo_base, formato_hover = procesar_datos_mapa(df, [año], indicador)
        
        # Datos para CCAA
        df_grouped_ccaa = df_year.groupby("comunidad_autónoma")[[color_col]].mean().reset_index()
        gdf_plot_ccaa = gdf_ccaa.set_index("rotulo").join(df_grouped_ccaa.set_index("comunidad_autónoma")).reset_index()
        
        # Datos para Provincias
        df_year["provincia_corr"] = df_year["provincia"].replace(equivalencias_provincias)
        df_grouped_prov = df_year.groupby("provincia_corr")[[color_col]].mean().reset_index()
        gdf_plot_prov = gdf_prov.set_index("NAMEUNIT").join(df_grouped_prov.set_index("provincia_corr")).reset_index()
        
        col_mapa1, col_mapa2 = st.columns(2)
        
        with col_mapa1:
            fig_map_ccaa = px.choropleth(
                gdf_plot_ccaa,
                geojson=gdf_plot_ccaa.geometry.__geo_interface__,
                locations=gdf_plot_ccaa.index,
                color=color_col,
                hover_name="rotulo",
                color_continuous_scale=color_scale,
                projection="mercator",
                title=f"{titulo_base} - {año}<br><sub>Por Comunidad Autónoma</sub>"
            )
            fig_map_ccaa.update_geos(fitbounds="locations", visible=False)
            fig_map_ccaa.update_layout(height=600)
            st.plotly_chart(fig_map_ccaa, use_container_width=True)
        
        with col_mapa2:
            fig_map_prov = px.choropleth(
                gdf_plot_prov,
                geojson=gdf_plot_prov.geometry.__geo_interface__,
                locations=gdf_plot_prov.index,
                color=color_col,
                hover_name="NAMEUNIT",
                color_continuous_scale=color_scale,
                projection="mercator",
                title=f"{titulo_base} - {año}<br><sub>Por Provincia</sub>"
            )
            fig_map_prov.update_geos(fitbounds="locations", visible=False)
            fig_map_prov.update_layout(height=600)
            st.plotly_chart(fig_map_prov, use_container_width=True)
    
    else:
        # Modo comparativa multi-año
        if len(años_seleccionados) > 4:
            st.warning("Por favor, selecciona máximo 4 años para una mejor visualización.")
            años_seleccionados = años_seleccionados[:4]
        
        st.markdown(f"#### Comparativa:")
        st.markdown(f"**Años seleccionados:** {', '.join(map(str, años_seleccionados))}")
        
        datos_ccaa_todos = []
        datos_prov_todos = []
        valores_min_max = []
        
        for año in años_seleccionados:
            df_year, color_col, color_scale, titulo_base_temp, formato_hover = procesar_datos_mapa(df, [año], indicador)
            
            # CCAA
            df_grouped_ccaa = df_year.groupby("comunidad_autónoma")[[color_col]].mean().reset_index()
            gdf_plot_ccaa = gdf_ccaa.set_index("rotulo").join(df_grouped_ccaa.set_index("comunidad_autónoma")).reset_index()
            datos_ccaa_todos.append((año, gdf_plot_ccaa, color_col))
            
            # Provincias
            df_year["provincia_corr"] = df_year["provincia"].replace(equivalencias_provincias)
            df_grouped_prov = df_year.groupby("provincia_corr")[[color_col]].mean().reset_index()
            gdf_plot_prov = gdf_prov.set_index("NAMEUNIT").join(df_grouped_prov.set_index("provincia_corr")).reset_index()
            datos_prov_todos.append((año, gdf_plot_prov, color_col))
            
            # Recoger valores para rango común
            valores_ccaa = gdf_plot_ccaa[color_col].dropna()
            valores_prov = gdf_plot_prov[color_col].dropna()
            if len(valores_ccaa) > 0:
                valores_min_max.extend([valores_ccaa.min(), valores_ccaa.max()])
            if len(valores_prov) > 0:
                valores_min_max.extend([valores_prov.min(), valores_prov.max()])
        
        if valores_min_max:
            rango_min = min(valores_min_max)
            rango_max = max(valores_min_max)
        else:
            rango_min, rango_max = 0, 1
        
        st.markdown("##### Por Comunidades Autónomas")
        cols_ccaa = st.columns(len(años_seleccionados))
        
        for i, (año, gdf_plot_ccaa, color_col) in enumerate(datos_ccaa_todos):
            with cols_ccaa[i]:
                fig_map_ccaa = px.choropleth(
                    gdf_plot_ccaa,
                    geojson=gdf_plot_ccaa.geometry.__geo_interface__,
                    locations=gdf_plot_ccaa.index,
                    color=color_col,
                    hover_name="rotulo",
                    color_continuous_scale=color_scale,
                    projection="mercator",
                    title=f"<b>{año}</b>",
                    range_color=[rango_min, rango_max] 
                )
                fig_map_ccaa.update_geos(fitbounds="locations", visible=False)
                fig_map_ccaa.update_layout(
                    height=450,
                    title_x=0.5,
                    title_font_size=16,
                    margin=dict(l=0, r=0, t=40, b=0),
                    coloraxis_showscale=(i == len(años_seleccionados) - 1) 
                )
                st.plotly_chart(fig_map_ccaa, use_container_width=True)
        
        st.markdown("##### Por Provincias")
        cols_prov = st.columns(len(años_seleccionados))
        
        for i, (año, gdf_plot_prov, color_col) in enumerate(datos_prov_todos):
            with cols_prov[i]:
                fig_map_prov = px.choropleth(
                    gdf_plot_prov,
                    geojson=gdf_plot_prov.geometry.__geo_interface__,
                    locations=gdf_plot_prov.index,
                    color=color_col,
                    hover_name="NAMEUNIT",
                    color_continuous_scale=color_scale,
                    projection="mercator",
                    title=f"<b>{año}</b>",
                    range_color=[rango_min, rango_max] 
                )
                fig_map_prov.update_geos(fitbounds="locations", visible=False)
                fig_map_prov.update_layout(
                    height=450,
                    title_x=0.5,
                    title_font_size=16,
                    margin=dict(l=0, r=0, t=40, b=0),
                    coloraxis_showscale=(i == len(años_seleccionados) - 1) 
                )
                st.plotly_chart(fig_map_prov, use_container_width=True)

# ---------------------------
# ESTADÍSTICAS RESUMEN
# ---------------------------

if modo_comparacion == "Un solo año":
    año = años_seleccionados[0]
    df_stats = df[df["año"] == año]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_contratos = df_stats["total_contratos"].sum()
        st.metric("📄 Total Contratos", f"{total_contratos:,.0f}")
    
    with col2:
        total_demandantes = df_stats["total_dtes_empleo"].sum()
        st.metric("👥 Total Demandantes", f"{total_demandantes:,.0f}")
    
    with col3:
        if total_demandantes > 0:
            indice_insercion_nacional = total_contratos / total_demandantes
            st.metric("🎯 Índice Inserción Nacional", f"{indice_insercion_nacional:.3f}")
        else:
            st.metric("🎯 Índice Inserción Nacional", "N/A")
    
    with col4:
        indef_total = (
            df_stats["contratos_iniciales_indefinidos_hombres"].sum() +
            df_stats["contratos_convertidos_en_indefinidos_hombres"].sum() +
            df_stats["contratos_iniciales_indefinidos_mujeres"].sum() +
            df_stats["contratos_convertidos_en_indefinidos_mujeres"].sum()
        )
        if total_contratos > 0:
            indice_estabilidad_nacional = indef_total / total_contratos
            st.metric("⚖️ Índice Estabilidad Nacional", f"{indice_estabilidad_nacional:.1%}")
        else:
            st.metric("⚖️ Índice Estabilidad Nacional", "N/A")

else:
    stats_comparativa = []
    for año in años_seleccionados:
        df_año = df[df["año"] == año]
        total_contratos = df_año["total_contratos"].sum()
        total_demandantes = df_año["total_dtes_empleo"].sum()
        
        stats_comparativa.append({
            "Año": año,
            "Contratos": total_contratos,
            "Demandantes": total_demandantes,
            "Índice Inserción": total_contratos / total_demandantes if total_demandantes > 0 else 0
        })
    
    df_comparativa = pd.DataFrame(stats_comparativa)
    
    st.dataframe(
        df_comparativa.style.format({
            "Contratos": "{:,.0f}",
            "Demandantes": "{:,.0f}",
            "Índice Inserción": "{:.3f}"
        }),
        use_container_width=True
    )

# ---------------------------
# FOOTER CON INFORMACIÓN
# ---------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
    <strong>Fuente de datos:</strong> Dataset de empleo español (2010-2025)<br>
    <strong>Última actualización:</strong> Los datos se actualizan automáticamente<br>
    <strong>Rendimiento:</strong> Los datos están optimizados en caché para una carga rápida
    </small>
</div>
""", unsafe_allow_html=True)