
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np

plt.style.use('seaborn-muted')
sns.set_context('talk')


def grafico_contratos_por_comunidad(df, gdf):
    anios = sorted(df['año'].unique())[-4:]
    fig, axes = plt.subplots(1, 4, figsize=(22, 6))
    cmap = 'YlGnBu'

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('comunidad_autónoma')['total_contratos'].sum().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))
        merged.plot(column='total_contratos', ax=ax, cmap=cmap, edgecolor='grey', legend=False)
        ax.set_title(f"Año {anio}", fontsize=12)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.1, 0.4, 0.02])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(
        vmin=merged['total_contratos'].min(), vmax=merged['total_contratos'].max()))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Total de contratos")
    plt.suptitle("Contratos registrados por comunidad (últimos 4 años)", fontsize=16)
    plt.savefig("images/1_ccaa.svg")
    plt.show()

def grafico_demandantes_por_comunidad(df, gdf):
    anios = sorted(df['año'].unique())[-4:]
    fig, axes = plt.subplots(1, 4, figsize=(22, 6))
    cmap = 'OrRd' 

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('comunidad_autónoma')['total_dtes_empleo'].sum().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))

        merged.plot(column='total_dtes_empleo', ax=ax, cmap=cmap, edgecolor='grey', legend=False)
        ax.set_title(f"Año {anio}", fontsize=12)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.1, 0.4, 0.02])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(
        vmin=merged['total_dtes_empleo'].min(), vmax=merged['total_dtes_empleo'].max()))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Total de demandantes de empleo")
    plt.suptitle("Demandantes de empleo por comunidad (últimos 4 años)", fontsize=16)
    plt.savefig("images/1_1_ccaa.svg")
    plt.show()

def mapa_indice_insercion(df, gdf):
    anios = sorted(df['año'].unique())[-4:]
    fig, axes = plt.subplots(1, 4, figsize=(22, 6))
    cmap = 'viridis'

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[(df['año'] == anio) & (df['total_dtes_empleo'] > 0)].copy()
        df_anio['indice_insercion'] = df_anio['total_contratos'] / df_anio['total_dtes_empleo']
        df_grouped = df_anio.groupby('comunidad_autónoma')['indice_insercion'].mean().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))

        merged.plot(column='indice_insercion', ax=ax, cmap=cmap, edgecolor='black', legend=False)
        ax.set_title(f"Año {anio}")
        ax.axis('off')

    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.1, 0.4, 0.02])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(
        vmin=0, vmax=merged['indice_insercion'].max()))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Índice de Inserción (contratos/demandantes)")
    plt.suptitle("Índice de Inserción Laboral por comunidad (últimos 4 años)", fontsize=16)
    plt.savefig("images/1_1_1_ccaa.svg")
    plt.show()

def grafico_contratos_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024):
    df_anio = df[df['año'] == anio]
    df_grouped = df_anio.groupby('provincia')['total_contratos'].sum().reset_index()
    df_grouped['provincia_corr'] = df_grouped['provincia'].replace(equivalencias_provincias)
    merged = gdf_prov.set_index('NAMEUNIT').join(df_grouped.set_index('provincia_corr'))

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    cmap = 'YlGnBu'
    merged.plot(column='total_contratos', ax=ax, cmap=cmap, edgecolor='black', legend=True)
    ax.set_title(f"Total de Contratos por Provincia - {anio}", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("images/1_prov.svg")
    plt.savefig("images/1_prov.png")
    plt.show()

def grafico_demandantes_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024):
    df_anio = df[df['año'] == anio]
    df_grouped = df_anio.groupby('provincia')['total_dtes_empleo'].sum().reset_index()
    df_grouped['provincia_corr'] = df_grouped['provincia'].replace(equivalencias_provincias)
    merged = gdf_prov.set_index('NAMEUNIT').join(df_grouped.set_index('provincia_corr'))

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    cmap = 'OrRd'
    merged.plot(column='total_dtes_empleo', ax=ax, cmap=cmap, edgecolor='black', legend=True)
    ax.set_title(f"Demandantes de Empleo por Provincia - {anio}", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("images/1_1_prov.svg")
    plt.savefig("images/1_1_prov.png")
    plt.show()

def mapa_indice_insercion_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024):
    df_anio = df[(df['año'] == anio) & (df['total_dtes_empleo'] > 0)].copy()
    
    # Calcular el índice de inserción laboral
    df_anio['indice_insercion'] = df_anio['total_contratos'] / df_anio['total_dtes_empleo']
    df_grouped = df_anio.groupby('provincia')['indice_insercion'].mean().reset_index()
    df_grouped['provincia_corr'] = df_grouped['provincia'].replace(equivalencias_provincias)
    merged = gdf_prov.set_index('NAMEUNIT').join(df_grouped.set_index('provincia_corr'))

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    cmap = 'viridis'
    merged.plot(column='indice_insercion', ax=ax, cmap=cmap, edgecolor='black', legend=True)
    ax.set_title(f"Índice de Inserción Laboral por Provincia - {anio}", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("images/1_1_1_prov.svg")
    plt.savefig("images/1_1_1_prov.png")
    plt.show()

def grafico_contratos_por_municipio(df, gdf_mun, anio=2024):
    df_anio = df[df['año'] == anio].copy()
    df_grouped = df_anio.groupby('municipio_correspondiente')['total_contratos'].sum().reset_index()
    df_grouped['municipio_correspondiente'] = df_grouped['municipio_correspondiente'].str.strip().str.lower()
    gdf_mun['NAMEUNIT'] = gdf_mun['NAMEUNIT'].str.strip().str.lower()

    merged = gdf_mun.set_index('NAMEUNIT').join(df_grouped.set_index('municipio_correspondiente'))
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    cmap = 'YlOrRd'
    vmin = merged['total_contratos'].min()
    vmax = merged['total_contratos'].max()

    merged.plot(column='total_contratos', ax=ax, cmap=cmap, edgecolor='black', linewidth=0.2,
                legend=False, missing_kwds={"color": "white", "label": "Sin datos"})

    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar_ax = fig.add_axes([0.25, 0.12, 0.5, 0.02])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Total de contratos por municipio", fontsize=14)
    ax.set_title(f"Total de Contratos por Municipio ({anio})", fontsize=16)
    ax.axis('off')
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])
    plt.savefig("images/1_mun.svg")
    plt.savefig("images/1_mun.png")
    plt.show()

def grafico_contratos_por_municipio_mejorado(df, gdf_mun, anio=2024, capitales=None, top_n=10):
    df_anio = df[df['año'] == anio].copy()
    df_grouped = df_anio.groupby('municipio_correspondiente')['total_contratos'].sum().reset_index()
    df_grouped['municipio_correspondiente'] = df_grouped['municipio_correspondiente'].str.strip().str.lower()
    gdf_mun['NAMEUNIT'] = gdf_mun['NAMEUNIT'].str.strip().str.lower()

    merged = gdf_mun.set_index('NAMEUNIT').join(df_grouped.set_index('municipio_correspondiente'))
    capitales_norm = [c.strip().lower() for c in capitales] if capitales else []
    capitals_gdf = merged[merged.index.isin(capitales_norm)]
    top_municipios = df_grouped.sort_values(by='total_contratos', ascending=False).head(top_n)
    top_gdf = merged[merged.index.isin(top_municipios['municipio_correspondiente'])]

    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    cmap = 'YlOrRd'
    vmin = merged['total_contratos'].min()
    vmax = merged['total_contratos'].max()

    merged.plot(column='total_contratos', ax=ax, cmap=cmap, edgecolor='lightgrey', linewidth=0.2,
                legend=False, missing_kwds={"color": "white", "label": "Sin datos"})

    # Capitales
    if not capitals_gdf.empty:
        capitals_gdf.boundary.plot(ax=ax, edgecolor='black', linewidth=1.2)
        for idx, row in capitals_gdf.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(idx.title(), xy=(centroid.x, centroid.y), xytext=(3, 3),
                        textcoords="offset points", fontsize=8, color='black')

    # Top municipios
    if not top_gdf.empty:
        top_gdf.boundary.plot(ax=ax, edgecolor='red', linewidth=1.2, linestyle='--')

    ax.set_title(f"Contratos registrados por municipio ({anio})", fontsize=16)
    ax.axis('off')

    legend_elements = [
        Patch(facecolor='white', edgecolor='black', linewidth=1.2, label='Capital de provincia'),
        Patch(facecolor='white', edgecolor='red', linewidth=1.2, linestyle='--', label=f'Top {top_n} municipios'),
    ]

    ax.legend(
            handles=legend_elements,
            loc='upper left',
            bbox_to_anchor=(0.7, 0.3),
            fontsize=10,
            title_fontsize=11
        ) 
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar_ax = fig.add_axes([0.25, 0.12, 0.5, 0.02]) 
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Total de contratos por municipio", fontsize=12)
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])
    plt.savefig(f"images/1_mun_mejorado.svg")
    plt.savefig(f"images/1_mun_mejorado.png")
    plt.show()

def calcular_indice_estabilidad(df):
    df = df.copy()
    df['contratos_indefinidos'] = (
        df['contratos_iniciales_indefinidos_hombres'] +
        df['contratos_convertidos_en_indefinidos_hombres'] +
        df['contratos_iniciales_indefinidos_mujeres'] +
        df['contratos_convertidos_en_indefinidos_mujeres']
    )
    df['indice_estabilidad'] = df['contratos_indefinidos'] / df['total_contratos']
    df = df[df['total_contratos'] > 0]  # evitar divisiones por 0
    return df

def mapa_estabilidad_anual(df, gdf, anios=None):
    df = calcular_indice_estabilidad(df)
    if anios is None:
        anios = sorted(df['año'].unique())[-4:]

    fig, axes = plt.subplots(1, len(anios), figsize=(6 * len(anios), 6))
    cmap = 'viridis'

    vmin = 0
    vmax = 1

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('comunidad_autónoma')['indice_estabilidad'].mean().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))

        merged.plot(column='indice_estabilidad', ax=ax, cmap=cmap, edgecolor='black', legend=False)
        ax.set_title(f"Año {anio}")
        ax.axis('off')
    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.1, 0.4, 0.02])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Índice de Estabilidad (contratos indefinidos / total contratos)")
    plt.suptitle("Evolución del Índice de Estabilidad por Comunidad", fontsize=16)
    plt.savefig("images/2_ccaa.svg")
    plt.show()

def mapa_brecha_genero_relativa(df, gdf, anios=[2020, 2021, 2022, 2023]):
    df = df.copy()
    df['total_contratos_mujeres'] = (
        df['contratos_iniciales_indefinidos_mujeres'] +
        df['contratos_iniciales_temporales_mujeres'] +
        df['contratos_convertidos_en_indefinidos_mujeres']
    )
    df['total_contratos_hombres'] = (
        df['contratos_iniciales_indefinidos_hombres'] +
        df['contratos_iniciales_temporales_hombres'] +
        df['contratos_convertidos_en_indefinidos_hombres']
    )
    df['total_contratos'] = df['total_contratos_mujeres'] + df['total_contratos_hombres']
    df['brecha_relativa'] = (df['total_contratos_hombres'] - df['total_contratos_mujeres']) / df['total_contratos']
    fig, axes = plt.subplots(1, len(anios), figsize=(6 * len(anios), 7))
    if len(anios) == 1:
        axes = [axes]

    all_vals = []
    for anio in anios:
        df_anio = df[df['año'] == anio]
        grouped = df_anio.groupby('comunidad_autónoma')['brecha_relativa'].mean()
        all_vals.extend(grouped.values)
    absmax = max(abs(np.nanmin(all_vals)), abs(np.nanmax(all_vals)))

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('comunidad_autónoma')['brecha_relativa'].mean().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))

        merged.plot(column='brecha_relativa', ax=ax, cmap='bwr', edgecolor='black',
                    legend=False, vmin=-absmax, vmax=absmax)
        ax.set_title(f"Año {anio}", fontsize=12)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.1)
    cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.03])
    sm = plt.cm.ScalarMappable(cmap='bwr', norm=plt.Normalize(vmin=-absmax, vmax=absmax))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Brecha relativa (hombres - mujeres / total)")
    plt.suptitle("Brecha relativa de género en contratos por comunidad autónoma", fontsize=16)
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    plt.savefig("images/3_ccaa.svg")
    plt.show()

def mapa_brecha_genero_relativa_provincias(df, gdf_prov, equivalencias_provincias, anios=[2020, 2021, 2022, 2023]):
    df = df.copy()
    df['total_contratos_mujeres'] = (
        df['contratos_iniciales_indefinidos_mujeres'] +
        df['contratos_iniciales_temporales_mujeres'] +
        df['contratos_convertidos_en_indefinidos_mujeres']
    )
    df['total_contratos_hombres'] = (
        df['contratos_iniciales_indefinidos_hombres'] +
        df['contratos_iniciales_temporales_hombres'] +
        df['contratos_convertidos_en_indefinidos_hombres']
    )
    df['total_contratos'] = df['total_contratos_mujeres'] + df['total_contratos_hombres']
    df['brecha_relativa'] = (
        df['total_contratos_hombres'] - df['total_contratos_mujeres']
    ) / df['total_contratos']

    all_vals = []
    for anio in anios:
        df_anio = df[df['año'] == anio]
        grouped = df_anio.groupby('provincia')['brecha_relativa'].mean()
        all_vals.extend(grouped.values)
    absmax = max(abs(np.nanmin(all_vals)), abs(np.nanmax(all_vals)))
    fig, axes = plt.subplots(1, len(anios), figsize=(6 * len(anios), 7))
    if len(anios) == 1:
        axes = [axes]

    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('provincia')['brecha_relativa'].mean().reset_index()
        df_grouped['provincia_corr'] = df_grouped['provincia'].replace(equivalencias_provincias)
        merged = gdf_prov.set_index('NAMEUNIT').join(df_grouped.set_index('provincia_corr'))
        merged.plot(column='brecha_relativa', ax=ax, cmap='bwr', edgecolor='black',
                    legend=False, vmin=-absmax, vmax=absmax)
        ax.set_title(f"Año {anio}", fontsize=12)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.1)
    cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.03])
    sm = plt.cm.ScalarMappable(cmap='bwr', norm=plt.Normalize(vmin=-absmax, vmax=absmax))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Brecha relativa (hombres - mujeres / total)")
    plt.suptitle("Brecha relativa de género en contratos por provincia", fontsize=16)
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    plt.savefig("images/3_prov.svg")
    plt.savefig("images/3_prov.png")
    plt.show()

def mapa_brecha_genero_relativa_municipios(df, gdf_mun, anios=[2020, 2021, 2022, 2023]):
    df = df.copy()
    df['total_contratos_mujeres'] = (
        df['contratos_iniciales_indefinidos_mujeres'] +
        df['contratos_iniciales_temporales_mujeres'] +
        df['contratos_convertidos_en_indefinidos_mujeres']
    )
    df['total_contratos_hombres'] = (
        df['contratos_iniciales_indefinidos_hombres'] +
        df['contratos_iniciales_temporales_hombres'] +
        df['contratos_convertidos_en_indefinidos_hombres']
    )
    df['total_contratos'] = df['total_contratos_mujeres'] + df['total_contratos_hombres']
    df['brecha_relativa'] = (
        df['total_contratos_hombres'] - df['total_contratos_mujeres']
    ) / df['total_contratos']

    all_vals = []
    for anio in anios:
        df_anio = df[df['año'] == anio]
        grouped = df_anio.groupby('municipio_correspondiente')['brecha_relativa'].mean()
        all_vals.extend(grouped.values)
    absmax = max(abs(np.nanmin(all_vals)), abs(np.nanmax(all_vals)))
    fig, axes = plt.subplots(1, len(anios), figsize=(7 * len(anios), 10))
    if len(anios) == 1:
        axes = [axes]

    gdf_mun['NAMEUNIT'] = gdf_mun['NAMEUNIT'].str.strip().str.lower()
    df['municipio_correspondiente'] = df['municipio_correspondiente'].str.strip().str.lower()
    for i, anio in enumerate(anios):
        ax = axes[i]
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('municipio_correspondiente')['brecha_relativa'].mean().reset_index()
        merged = gdf_mun.set_index('NAMEUNIT').join(df_grouped.set_index('municipio_correspondiente'))
        merged.plot(column='brecha_relativa', ax=ax, cmap='bwr', edgecolor='black', linewidth=0.2,
                    legend=False, vmin=-absmax, vmax=absmax)
        ax.set_title(f"Año {anio}", fontsize=12)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.1)
    cbar_ax = fig.add_axes([0.25, 0.2, 0.5, 0.02])
    sm = plt.cm.ScalarMappable(cmap='bwr', norm=plt.Normalize(vmin=-absmax, vmax=absmax))
    sm._A = []
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Brecha relativa (hombres - mujeres / total)")
    plt.suptitle("Brecha relativa de género en contratos por municipio", fontsize=16, y=0.9)
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    plt.savefig("images/3_mun.svg")
    plt.savefig("images/3_mun.png")
    plt.show()

def mapa_sectores_absoluto(df, gdf, anio=2024):
    sectores = {
        'servicios': 'contratos__servicios',
        'agricultura': 'contratos__agricultura',
        'industria': 'contratos__industria',
        'construcción': 'contratos_construcción'
    }

    df_anio = df[df['año'] == anio].copy()

    fig, axes = plt.subplots(1, 4, figsize=(24, 6))
    cmap_abs = 'YlGnBu'

    for i, (sector, columna) in enumerate(sectores.items()):
        df_grouped = df_anio.groupby('comunidad_autónoma')[columna].sum().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))
        merged.plot(column=columna, ax=axes[i], cmap=cmap_abs, edgecolor='black', legend=False)
        axes[i].set_title(f"{sector.capitalize()}", fontsize=12)
        axes[i].axis('off')
    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
    all_vals = pd.concat([df_anio.groupby('comunidad_autónoma')[col].sum() for col in sectores.values()])
    sm = plt.cm.ScalarMappable(cmap=cmap_abs, norm=plt.Normalize(vmin=all_vals.min(), vmax=all_vals.max()))
    sm._A = []
    
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Contratos totales por comunidad")
    plt.suptitle(f"Contratos por sector en {anio}", fontsize=16)
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    plt.savefig("images/4_ccaa.svg")
    plt.show()


def mapa_sector_predominante(df, gdf_prov, equivalencias_provincias, anio=2024):
    sectores = {
        'Servicios': 'contratos__servicios',
        'Agricultura': 'contratos__agricultura',
        'Industria': 'contratos__industria',
        'Construcción': 'contratos_construcción'
    }

    colores = {
        'Servicios': '#1f77b4',
        'Agricultura': '#2ca02c',
        'Industria': '#ff7f0e',
        'Construcción': '#d62728'
    }

    df_anio = df[df['año'] == anio].copy()
    df_grouped = df_anio.groupby('provincia')[[v for v in sectores.values()]].sum().reset_index()
    df_grouped['sector_predominante'] = df_grouped[sectores.values()].idxmax(axis=1)
    reverse_map = {v: k for k, v in sectores.items()}
    df_grouped['sector_predominante'] = df_grouped['sector_predominante'].map(reverse_map)
    df_grouped['provincia_corr'] = df_grouped['provincia'].replace(equivalencias_provincias)
    merged = gdf_prov.set_index('NAMEUNIT').join(df_grouped.set_index('provincia_corr'))
    merged['color'] = merged['sector_predominante'].map(colores).fillna('lightgrey')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(color=merged['color'], ax=ax, edgecolor='black')
    legend_elements = [Line2D([0], [0], marker='o', color='w',
                              label=sector, markerfacecolor=color, markersize=10)
                       for sector, color in colores.items()]
    
    ax.legend(
            handles=legend_elements,
            title="Sector predominante",
            loc='upper left',
            bbox_to_anchor=(0.7, 0.3),
            fontsize=10,
            title_fontsize=11
        ) 
    ax.set_title(f"Sector con más contratos por provincia ({anio})", fontsize=16)
    ax.axis('off')
    plt.savefig("images/4_prov.svg")
    plt.savefig("images/4_prov.png")
    plt.show()

def mapa_sector_predominante_municipios(df, gdf_mun, anio=2024):
    sectores = {
        'Servicios': 'contratos__servicios',
        'Agricultura': 'contratos__agricultura',
        'Industria': 'contratos__industria',
        'Construcción': 'contratos_construcción'
    }

    colores = {
        'Servicios': '#1f77b4',
        'Agricultura': '#2ca02c',
        'Industria': '#ff7f0e',
        'Construcción': '#d62728'
    }
    df_anio = df[df['año'] == anio].copy()
    df_grouped = df_anio.groupby('municipio_correspondiente')[[v for v in sectores.values()]].sum().reset_index()
    df_grouped['sector_predominante'] = df_grouped[sectores.values()].idxmax(axis=1)
    reverse_map = {v: k for k, v in sectores.items()}
    df_grouped['sector_predominante'] = df_grouped['sector_predominante'].map(reverse_map)
    df_grouped['municipio_corr'] = df_grouped['municipio_correspondiente'].str.strip().str.lower()
    gdf_mun['NAMEUNIT'] = gdf_mun['NAMEUNIT'].str.strip().str.lower()
    merged = gdf_mun.set_index('NAMEUNIT').join(df_grouped.set_index('municipio_corr'))
    merged['color'] = merged['sector_predominante'].map(colores).fillna('#1f77b4')
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    merged.plot(color=merged['color'], ax=ax, edgecolor='black', linewidth=0.2)
    legend_elements = [Line2D([0], [0], marker='o', color='w',
                              label=sector, markerfacecolor=color, markersize=10)
                       for sector, color in colores.items()]
    ax.legend(
        handles=legend_elements,
        title="Sector predominante",
        loc='upper left',
        bbox_to_anchor=(0.7, 0.3),
        fontsize=10,
        title_fontsize=11
    )
    ax.set_title(f"Sector con más contratos por municipio ({anio})", fontsize=16)
    ax.axis('off')
    plt.savefig("images/4_mun.svg")
    plt.savefig("images/4_mun.png")
    plt.show()


def main():
    
    # Cargar dataset principal ya preprocesado
    df = pd.read_csv("dataset_final_formateado.csv")

    # Cargamos todos los shapefiles que vamos a utilizar
    gdf_ccaa = gpd.read_file("mapa/se89_3_admin_ccaa_a_x.shp")
    gdf_prov = gpd.read_file("mapa/recintos_provinciales_inspire_peninbal_etrs89.shp")
    gdf_mun = gpd.read_file("mapa/recintos_municipales_inspire_peninbal_etrs89.shp")

    equivalencias_provincias = {
        'Almería': 'Almería',
        'Cádiz': 'Cádiz',
        'Córdoba': 'Córdoba',
        'Granada': 'Granada',
        'Huelva': 'Huelva',
        'Jaén': 'Jaén',
        'Málaga': 'Málaga',
        'Sevilla': 'Sevilla',
        'Huesca': 'Huesca',
        'Teruel': 'Teruel',
        'Zaragoza': 'Zaragoza',
        'Asturias': 'Asturias',
        'Balears, Illes': 'Illes Balears',
        'Palmas, Las': 'Las Palmas',
        'Santa Cruz de Tenerife': 'Santa Cruz de Tenerife',
        'Cantabria': 'Cantabria',
        'Ávila': 'Ávila',
        'Burgos': 'Burgos',
        'León': 'León',
        'Palencia': 'Palencia',
        'Salamanca': 'Salamanca',
        'Segovia': 'Segovia',
        'Soria': 'Soria',
        'Valladolid': 'Valladolid',
        'Zamora': 'Zamora',
        'Albacete': 'Albacete',
        'Ciudad Real': 'Ciudad Real',
        'Cuenca': 'Cuenca',
        'Guadalajara': 'Guadalajara',
        'Toledo': 'Toledo',
        'Barcelona': 'Barcelona',
        'Girona': 'Girona',
        'Lleida': 'Lleida',
        'Tarragona': 'Tarragona',
        'Alicante/Alacant': 'Alacant/Alicante',
        'Castellón/Castelló': 'Castelló/Castellón',
        'Valencia/Valéncia': 'València/Valencia',
        'Badajoz': 'Badajoz',
        'Cáceres': 'Cáceres',
        'Coruña, A': 'A Coruña',
        'Lugo': 'Lugo',
        'Ourense': 'Ourense',
        'Pontevedra': 'Pontevedra',
        'Madrid': 'Madrid',
        'Murcia': 'Murcia',
        'Navarra': 'Navarra',
        'Araba/Álava': 'Araba/Álava',
        'Gipuzkoa': 'Gipuzkoa',
        'Bizkaia': 'Bizkaia',
        'Rioja, La': 'La Rioja',
        'Ceuta': 'Ceuta',
        'Melilla': 'Melilla'
    }
    capitales = [
        'albacete', 'alicante', 'almería', 'ávila', 'badajoz', 'barcelona', 'bilbao',
        'burgos', 'cáceres', 'cádiz', 'castelló de la plana', 'ceuta', 'ciudad real', 'córdoba',
        'cuenca', 'girona', 'granada', 'guadalajara', 'huelva', 'huesca', 'jaén',
        'uña', 'logroño', 'palma', 'león', 'lleida', 'lugo', 'madrid',
        'málaga', 'melilla', 'murcia', 'ourense', 'oviedo', 'palencia',
        'pontevedra', 'salamanca', 'santander', 'segovia',
        'sevilla', 'soria', 'tarragona', 'teruel', 'toledo', 'valència', 'valladolid',
        'vitoria-gasteiz', 'donostia/san sebastián', 'zamora', 'zaragoza'
        ]   

    # Generar gráficos
    grafico_contratos_por_comunidad(df, gdf_ccaa)
    print("Gráfico 1_ccaa.svg generado.")
    grafico_demandantes_por_comunidad(df, gdf_ccaa)
    print("Gráfico 1_1_ccaa.svg generado.")
    mapa_indice_insercion(df, gdf_ccaa)
    print("Gráfico 1_1_1_ccaa.svg generado.")

    grafico_contratos_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024)
    print("Gráfico 1_prov.svg generado.")
    grafico_demandantes_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024)
    print("Gráfico 1_1_prov.svg generado.")
    mapa_indice_insercion_por_provincia(df, gdf_prov, equivalencias_provincias, anio=2024) 
    print("Gráfico 1_1_1_prov.svg generado.")   

    grafico_contratos_por_municipio(df, gdf_mun, anio=2024)
    print("Gráfico 1_mun.svg generado.")
    grafico_contratos_por_municipio_mejorado(df, gdf_mun, anio=2024, capitales=capitales, top_n=10)
    print("Gráfico 1_mun_mejorado.svg generado.")

    mapa_estabilidad_anual(df, gdf_ccaa, anios=[2020, 2022])
    print("Gráfico 2_ccaa.svg generado.")

    mapa_brecha_genero_relativa(df, gdf_ccaa, anios=[2015, 2020, 2024])
    print("Gráfico 3_ccaa.svg generado.")
    mapa_brecha_genero_relativa_provincias(df, gdf_prov, equivalencias_provincias, anios=[2015, 2020, 2024])
    print("Gráfico 3_prov.svg generado.")
    mapa_brecha_genero_relativa_municipios(df, gdf_mun, anios=[2015, 2024])
    print("Gráfico 3_mun.svg generado.")

    mapa_sectores_absoluto(df, gdf_ccaa, anio=2024)
    print("Gráfico 4_ccaa.svg generado.")
    mapa_sector_predominante(df, gdf_prov, equivalencias_provincias, anio=2024)
    print("Gráfico 4_prov.svg generado.")
    mapa_sector_predominante_municipios(df, gdf_mun, anio=2024)
    print("Gráfico 4_mun.svg generado.")

    print("Todos los gráficos han sido generados y guardados en la carpeta 'images'.")

main()











