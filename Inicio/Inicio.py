import streamlit as st
from streamlit.logger import get_logger
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st
from PIL import Image
import base64


LOGGER = get_logger(__name__)


def create_stats_card(title, value, icon, color, description=""):
    """Crear tarjeta de estadística moderna"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}15, {color}08);
        padding: 30px;
        border-radius: 15px;
        border-left: 4px solid {color};
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        text-align: center;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 12px;">{icon}</div>
        <h3 style="color: {color}; margin: 0; font-size: 1.8rem; font-weight: 600;">{value}</h3>
        <h4 style="margin: 8px 0; color: #2c3e50; font-size: 1.1rem;">{title}</h4>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.95rem; line-height: 1.4;">{description}</p>
    </div>
    """

def create_module_card(title, description, icon, color):
    """Crear tarjeta compacta para módulos"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}12, {color}06);
        padding: 25px 20px;
        border-radius: 12px;
        margin: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid {color}20;
        text-align: center;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s ease;
    " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
        <div style="font-size: 2.2rem; margin-bottom: 12px;">{icon}</div>
        <h4 style="color: {color}; margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 600;">{title}</h4>
        <p style="color: #5a6c7d; margin: 0; font-size: 0.9rem; line-height: 1.3;">{description}</p>
    </div>
    """

def run():
    st.set_page_config(
        page_title="Empleo España - Dashboard Analítico",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Cargar y codificar la imagen en base64
    imagen_path = "Inicio/data/header.jpg"
    with open(imagen_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #e0f7fa 0%, #fff3e0 100%);
        padding: 35px 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #ffe0b2;
        ">
        <h1 style="color: #333333; margin: 0; font-size: 2.5rem; font-weight: 600;">
            Dashboard Analítico del Empleo en España
        </h1>
        <h3 style="color: #555555; margin: 12px 0 0 0; font-weight: 400; font-size: 1.2rem;">
            Análisis Integral del Mercado Laboral | Período 2010-2025
        </h3>
    </div>
    """, unsafe_allow_html=True)

    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 30px;
        background: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        ">
        <img src="data:image/jpeg;base64,{encoded}" 
            style="width: 660px; height: auto; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);" />
        <div style="flex: 1;">
            <h3 style="color: #28a745; margin: 0 0 12px 0;">Sobre este Proyecto:</h3>
            <p style="margin: 0; line-height: 1.7; color: #495057; font-size: 1.05rem;">
                Esta plataforma presenta un <strong>análisis exhaustivo de los datos del mercado laboral español</strong> 
                basado en información oficial del SEPE. El dataset procesado contiene <strong>1.405.700 registros</strong> 
                que abarcan demandantes de empleo y contratos registrados, desagregados por múltiples dimensiones: 
                geográfica (municipio, provincia, comunidad autónoma), demográfica (sexo, edad) y sectorial.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("### Características del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_stats_card(
            "Registros", "1.4M+", "📊", "#5d4e75", "Filas de datos procesados"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_stats_card(
            "Período", "16 años", "📅", "#2980b9", "2010 - 2025"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_stats_card(
            "Variables", "32", "🔢", "#d68910", "Columnas analíticas"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_stats_card(
            "Fuente", "SEPE", "🏛️", "#7d3c98", "Datos oficiales"
        ), unsafe_allow_html=True)

    st.markdown("""
    <div style="
        height: 2px;
        background: linear-gradient(90deg, #e8eaf6 0%, #f3e5f5 100%);
        margin: 30px 0;
        border-radius: 1px;
    "></div>
    """, unsafe_allow_html=True)

    st.markdown("### Páginas Disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_module_card(
            "Evolución Temporal",
            "Tendencias generales del mercado laboral español",
            "📈",
            "#28a745"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_module_card(
            "Análisis por Género",
            "Perspectiva de género en el empleo español",
            "👥",
            "#6c757d"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_module_card(
            "Análisis Sectorial",
            "Distribución y evolución sectorial del empleo",
            "🏭",
            "#fd7e14"
        ), unsafe_allow_html=True)

    with st.sidebar:        
        # Información técnica
        with st.expander("🔧 Información Técnica"):
            st.markdown("""
            **Dataset procesado:**
            - 📊 1.405.700 registros
            - 📅 Período: 2010-2025
            - 🗂️ 32 variables analíticas
            - 🏛️ Fuente: SEPE (Servicio Público de Empleo Estatal)
            
            **Dimensiones de análisis:**
            - 🗺️ Geográfica: Municipio → Provincia → CC.AA.
            - 👤 Demográfica: Sexo y grupos de edad
            - 🏢 Sectorial: 4 sectores económicos principales
            """)
        
        # Metadatos del proyecto
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
            <small>
                <strong>Desarrollado por:</strong><br>
                Ana Gutiérrez Mandingorra<br>
                <em>Análisis de Datos - SEPE</em>
                <em>Trabajo Visualización de Datos - MIARFID</em>
            </small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()

def run2():
    st.set_page_config(
        page_title="Empleo España",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Visualización de Empleo en España (2010–2025)")
    st.write("""
    Esta aplicación permite analizar y visualizar datos laborales en España a nivel de comunidad autónoma, provincia y municipio.

    Utiliza las opciones del menú lateral izquierdo para navegar entre las diferentes páginas temáticas:
    - Evolución general
    - Género y empleo
    - Sectores económicos
    """)
    st.sidebar.success("Selecciona una página")


