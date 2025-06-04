import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Configuración global
sns.set_style("whitegrid")

# Carga del dataset
def cargar_datos(ruta):
    df = pd.read_csv(ruta, low_memory=False)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

def grafica_1_1(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    color_contratos = "#1f77b4"
    color_demandantes = "#E3962B"
    
    ax1.plot(df.groupby("fecha")["total_contratos"].sum(), color=color_contratos, linewidth=2.5, label="Contratos")
    ax1.set_xlabel("Fecha", fontsize=12)
    ax1.set_ylabel("Número de Contratos", color=color_contratos, fontsize=12)
    ax1.tick_params(axis="y", labelcolor=color_contratos)
    ax1.grid(True, linestyle="dotted", alpha=0.7)
    
    ax2 = ax1.twinx()
    ax2.plot(df.groupby("fecha")["total_dtes_empleo"].sum(), color=color_demandantes, linewidth=2.5, linestyle="dashed", label="Demandantes de Empleo")
    ax2.set_ylabel("Número de Demandantes de Empleo", color=color_demandantes, fontsize=12)
    ax2.tick_params(axis="y", labelcolor=color_demandantes)
    
    plt.title("Evolución Temporal de Contratos y Demandantes de Empleo", fontsize=14)
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95), fontsize=12)
    plt.tight_layout()
    plt.savefig("images/1_1.svg")
    plt.show()

def grafica_1_2(df):
    plt.figure(figsize=(12, 6))  

    meses_dict = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    df["mes_nombre"] = df["mes"].map(meses_dict)
    orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    df["total_contratos"] = pd.to_numeric(df["total_contratos"], errors="coerce")
    df["total_dtes_empleo"] = pd.to_numeric(df["total_dtes_empleo"], errors="coerce")

    df_grouped = df.groupby("mes_nombre").agg({"total_contratos": "mean", "total_dtes_empleo": "mean"})
    df_grouped = df_grouped.reindex(orden_meses)

    colores = ["#1f77b4", "#E3962B"]
    estilos = ["-", "--"]  

    leyendas_personalizadas = {
        "total_contratos": "Contratos",
        "total_dtes_empleo": "Demandantes de Empleo"
    }

    for i, columna in enumerate(df_grouped.columns):
        plt.plot(df_grouped.index, df_grouped[columna], estilos[i], 
                label=leyendas_personalizadas.get(columna, columna.replace("_", " ").title()),
                color=colores[i], linewidth=2.5, markersize=6)

        for j, valor in enumerate(df_grouped[columna]):
            plt.text(j, valor, f"{valor:.0f}", ha="center", va="bottom", fontsize=9, color=colores[i])

    plt.xlabel("Mes", fontsize=12)
    plt.ylabel("Promedio Mensual", fontsize=12)
    plt.title("Promedio Mensual de Contratos y Demandantes de Empleo", fontsize=14)
    plt.legend(loc="upper left", bbox_to_anchor=(0.75, 0.6), fontsize=12) 
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("images/1_2.svg")
    plt.show()

def grafica_2(df):
    plt.figure(figsize=(12, 6))

    df_grouped = df.groupby("año").agg({
        "contratos_iniciales_indefinidos_hombres": "sum",
        "contratos_iniciales_temporales_hombres": "sum",
        "contratos_convertidos_en_indefinidos_hombres": "sum",
        "contratos_iniciales_indefinidos_mujeres": "sum",
        "contratos_iniciales_temporales_mujeres": "sum",
        "contratos_convertidos_en_indefinidos_mujeres": "sum",
        "dtes_empleo_hombre_edad_<_25": "sum",
        "dtes_empleo_hombre_edad_25_-45": "sum",
        "dtes_empleo_hombre_edad_>=45": "sum",
        "dtes_empleo_mujer_edad_<_25": "sum",
        "dtes_empleo_mujer_edad_25_-45": "sum",
        "dtes_empleo_mujer_edad_>=45": "sum"
    })

    df_grouped["total_contratos_hombres"] = (df_grouped["contratos_iniciales_indefinidos_hombres"] +
                                            df_grouped["contratos_iniciales_temporales_hombres"] +
                                            df_grouped["contratos_convertidos_en_indefinidos_hombres"])

    df_grouped["total_contratos_mujeres"] = (df_grouped["contratos_iniciales_indefinidos_mujeres"] +
                                            df_grouped["contratos_iniciales_temporales_mujeres"] +
                                            df_grouped["contratos_convertidos_en_indefinidos_mujeres"])

    df_grouped["total_dtes_hombres"] = (df_grouped["dtes_empleo_hombre_edad_<_25"] +
                                        df_grouped["dtes_empleo_hombre_edad_25_-45"] +
                                        df_grouped["dtes_empleo_hombre_edad_>=45"])

    df_grouped["total_dtes_mujeres"] = (df_grouped["dtes_empleo_mujer_edad_<_25"] +
                                        df_grouped["dtes_empleo_mujer_edad_25_-45"] +
                                        df_grouped["dtes_empleo_mujer_edad_>=45"])

    colores = {"hombres": "#4574A1", "mujeres": "#E54923"}
    estilos = {"contratos": "-", "demandantes": "--"}
    plt.plot(df_grouped.index, df_grouped["total_contratos_hombres"], 
            label="Contratos Hombres", color=colores["hombres"], linestyle=estilos["contratos"], linewidth=2.5)

    plt.plot(df_grouped.index, df_grouped["total_contratos_mujeres"], 
            label="Contratos Mujeres", color=colores["mujeres"], linestyle=estilos["contratos"], linewidth=2.5)

    plt.plot(df_grouped.index, df_grouped["total_dtes_hombres"], 
            label="Demandantes Empleo Hombres", color=colores["hombres"], linestyle=estilos["demandantes"], linewidth=2.5)

    plt.plot(df_grouped.index, df_grouped["total_dtes_mujeres"], 
            label="Demandantes Empleo Mujeres", color=colores["mujeres"], linestyle=estilos["demandantes"], linewidth=2.5)

    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Cantidad", fontsize=12)
    plt.title("Evolución anual de Contratos y Demandantes de Empleo por Género (2010-2025)", fontsize=14)
    plt.legend(loc="upper left", bbox_to_anchor=(0.77, 0.95), fontsize=12)
    plt.tight_layout()
    plt.savefig("images/2.svg")
    plt.show()

def grafica_3(df):
    df_grouped = df.groupby("año").agg({
        "contratos_iniciales_indefinidos_hombres": "sum",
        "contratos_iniciales_temporales_hombres": "sum",
        "contratos_convertidos_en_indefinidos_hombres": "sum",
        "contratos_iniciales_indefinidos_mujeres": "sum",
        "contratos_iniciales_temporales_mujeres": "sum",
        "contratos_convertidos_en_indefinidos_mujeres": "sum",
        "dtes_empleo_hombre_edad_<_25": "sum",
        "dtes_empleo_hombre_edad_25_-45": "sum",
        "dtes_empleo_hombre_edad_>=45": "sum",
        "dtes_empleo_mujer_edad_<_25": "sum",
        "dtes_empleo_mujer_edad_25_-45": "sum",
        "dtes_empleo_mujer_edad_>=45": "sum"
    })

    df_grouped["total_contratos_hombres"] = (df_grouped["contratos_iniciales_indefinidos_hombres"] +
                                            df_grouped["contratos_iniciales_temporales_hombres"] +
                                            df_grouped["contratos_convertidos_en_indefinidos_hombres"])

    df_grouped["total_contratos_mujeres"] = (df_grouped["contratos_iniciales_indefinidos_mujeres"] +
                                            df_grouped["contratos_iniciales_temporales_mujeres"] +
                                            df_grouped["contratos_convertidos_en_indefinidos_mujeres"])

    df_grouped["total_dtes_hombres"] = (df_grouped["dtes_empleo_hombre_edad_<_25"] +
                                        df_grouped["dtes_empleo_hombre_edad_25_-45"] +
                                        df_grouped["dtes_empleo_hombre_edad_>=45"])

    df_grouped["total_dtes_mujeres"] = (df_grouped["dtes_empleo_mujer_edad_<_25"] +
                                        df_grouped["dtes_empleo_mujer_edad_25_-45"] +
                                        df_grouped["dtes_empleo_mujer_edad_>=45"])

    plot_data = pd.DataFrame({
        "Demandantes de Empleo": list(df_grouped["total_dtes_hombres"]) + list(df_grouped["total_dtes_mujeres"]),
        "Total Contratos": list(df_grouped["total_contratos_hombres"]) + list(df_grouped["total_contratos_mujeres"]),
        "Género": ["Hombres"] * len(df_grouped) + ["Mujeres"] * len(df_grouped)
    })

    jointplot = sns.jointplot(
        data=plot_data, x="Demandantes de Empleo", y="Total Contratos",
        kind="scatter", height=8
    )

    sns.scatterplot(
        data=plot_data, x="Demandantes de Empleo", y="Total Contratos",
        hue="Género", palette={"Hombres": "#4574A1", "Mujeres": "#E54923"}, ax=jointplot.ax_joint
    )

    for gender, color in zip(["Hombres", "Mujeres"], ["#4574A1", "#E54923"]):
        subset = plot_data[plot_data["Género"] == gender]
        jointplot.ax_marg_x.axvline(subset["Demandantes de Empleo"].mean(), color=color, linestyle="dashed", linewidth=2.5)
        jointplot.ax_marg_y.axhline(subset["Total Contratos"].mean(), color=color, linestyle="dashed", linewidth=2.5)

    plt.subplots_adjust(top=0.9)
    jointplot.fig.suptitle("Dispersión anual de Contratos y Demandantes de Empleo por Género (2010-2025)", fontsize=14)
    plt.tight_layout()
    plt.savefig("images/3.svg")
    plt.show()

def grafica_4_1(df):
    contratos = df.groupby("año")[
        ["contratos_iniciales_indefinidos_hombres", 
        "contratos_iniciales_temporales_hombres", 
        "contratos_convertidos_en_indefinidos_hombres", 
        "contratos_iniciales_indefinidos_mujeres", 
        "contratos_iniciales_temporales_mujeres", 
        "contratos_convertidos_en_indefinidos_mujeres"]
    ].sum()

    contratos["total_hombres"] = contratos["contratos_iniciales_indefinidos_hombres"] + \
                                contratos["contratos_iniciales_temporales_hombres"] + \
                                contratos["contratos_convertidos_en_indefinidos_hombres"]

    contratos["total_mujeres"] = contratos["contratos_iniciales_indefinidos_mujeres"] + \
                                contratos["contratos_iniciales_temporales_mujeres"] + \
                                contratos["contratos_convertidos_en_indefinidos_mujeres"]

    fig, ax = plt.subplots(figsize=(12, 6))
    años = contratos.index
    x = np.arange(len(años))

    ax.bar(x - 0.2, contratos["total_hombres"], width=0.4, label="Hombres", color="#4574A1", alpha=0.7)
    ax.bar(x + 0.2, contratos["total_mujeres"], width=0.4, label="Mujeres", color="#E54923", alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(años)
    ax.set_xlabel("Año", fontsize=12)
    ax.set_ylabel("Número de Contratos", fontsize=12)
    ax.set_title("Evolución anual de Contratos por Género (2010-2025)", fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig("images/4_1.svg")
    plt.show()

def grafica_4_2(df):
    contratos = df.groupby("año")[
        ["contratos_iniciales_indefinidos_hombres", 
        "contratos_iniciales_temporales_hombres", 
        "contratos_convertidos_en_indefinidos_hombres", 
        "contratos_iniciales_indefinidos_mujeres", 
        "contratos_iniciales_temporales_mujeres", 
        "contratos_convertidos_en_indefinidos_mujeres"]
    ].sum()

    fig, ax = plt.subplots(figsize=(12, 6))
    años = contratos.index
    x = np.arange(len(años))
    bar_width = 0.4

    ax.bar(x - bar_width/2, contratos["contratos_iniciales_indefinidos_hombres"], width=bar_width, label="Indefinidos Hombres", color="#4574A1")
    ax.bar(x - bar_width/2, contratos["contratos_iniciales_temporales_hombres"], width=bar_width, bottom=contratos["contratos_iniciales_indefinidos_hombres"], label="Temporales Hombres", color="lightblue")
    ax.bar(x - bar_width/2, contratos["contratos_convertidos_en_indefinidos_hombres"], width=bar_width, bottom=contratos["contratos_iniciales_indefinidos_hombres"] + contratos["contratos_iniciales_temporales_hombres"], label="Convertidos Indefinidos Hombres", color="navy")

    ax.bar(x + bar_width/2, contratos["contratos_iniciales_indefinidos_mujeres"], width=bar_width, label="Indefinidos Mujeres", color="#E54923")
    ax.bar(x + bar_width/2, contratos["contratos_iniciales_temporales_mujeres"], width=bar_width, bottom=contratos["contratos_iniciales_indefinidos_mujeres"], label="Temporales Mujeres", color="pink")
    ax.bar(x + bar_width/2, contratos["contratos_convertidos_en_indefinidos_mujeres"], width=bar_width, bottom=contratos["contratos_iniciales_indefinidos_mujeres"] + contratos["contratos_iniciales_temporales_mujeres"], label="Convertidos Indefinidos Mujeres", color="darkred")

    ax.set_xlabel("Año", fontsize=12)
    ax.set_ylabel("Número de Contratos", fontsize=12)
    ax.set_title("Evolución anual de Contratos por Tipo y Género (2010-2025)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(años)
    ax.legend(loc="upper left", bbox_to_anchor=(0.001, 0.99), fontsize=12)
    plt.tight_layout()
    plt.savefig("images/4_2.svg")
    plt.show()

def grafica_4_3(df):
    plt.figure(figsize=(12, 6)) 

    df_grouped = df.groupby("año")[[ 
        "contratos_iniciales_indefinidos_hombres",
        "contratos_iniciales_temporales_hombres",
        "contratos_convertidos_en_indefinidos_hombres",
        "contratos_iniciales_indefinidos_mujeres",
        "contratos_iniciales_temporales_mujeres",
        "contratos_convertidos_en_indefinidos_mujeres"
    ]].sum()

    colores_hombres = ["#4574A1", "lightblue", "navy"] 
    colores_mujeres = ["#E54923", "pink", "darkred"] 
    estilos = ["-", "--", ":"]

    etiquetas = {
        "contratos_iniciales_indefinidos_hombres": "Indefinidos Hombres",
        "contratos_iniciales_temporales_hombres": "Temporales Hombres",
        "contratos_convertidos_en_indefinidos_hombres": "Convertidos Indefinidos Hombres",
        "contratos_iniciales_indefinidos_mujeres": "Indefinidos Mujeres",
        "contratos_iniciales_temporales_mujeres": "Temporales Mujeres",
        "contratos_convertidos_en_indefinidos_mujeres": "Convertidos Indefinidos Mujeres"
    }

    for i, columna in enumerate([ 
        "contratos_iniciales_indefinidos_hombres",
        "contratos_iniciales_temporales_hombres",
        "contratos_convertidos_en_indefinidos_hombres"]):
        plt.plot(df_grouped.index, df_grouped[columna], 
                label=etiquetas[columna], 
                color=colores_hombres[i], linestyle=estilos[i], linewidth=2)

    for i, columna in enumerate([ 
        "contratos_iniciales_indefinidos_mujeres",
        "contratos_iniciales_temporales_mujeres",
        "contratos_convertidos_en_indefinidos_mujeres"]):
        plt.plot(df_grouped.index, df_grouped[columna], 
                label=etiquetas[columna], 
                color=colores_mujeres[i], linestyle=estilos[i], linewidth=2)

    plt.axvline(x=2021, color='#FACB20', linestyle=':', linewidth=3, label="Reforma Laboral entrada en vigor") 
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Número de Contratos", fontsize=12)
    plt.title("Evolución anual de Contratos por Tipo y Género (2010-2025)", fontsize=14)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1), fontsize=12)
    plt.xticks()
    plt.tight_layout()
    plt.savefig("images/4_3.svg")
    plt.show()

def grafica_5_1(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    df_grouped = df.groupby("año")[
        ["contratos__agricultura", "contratos__industria", "contratos_construcción", "contratos__servicios"]
    ].sum()

    colores = {
        "contratos__agricultura": "#2ca02c", 
        "contratos__industria": "#E3962B",  
        "contratos_construcción": "#d62728",  
        "contratos__servicios": "#1f77b4",    
    }

    for columna in df_grouped.columns:
        nombre_legible = columna.replace("__", " ").replace("_", " ").title()
        ax1.plot(df_grouped.index, df_grouped[columna], label=nombre_legible, 
                color=colores[columna], linewidth=2.5)

    ax1.set_xlabel("Año", fontsize=12)
    ax1.set_ylabel("Número de Contratos", fontsize=12)
    ax1.tick_params(axis="y")
    plt.title("Evolución anual de Contratos por Sector (2010-2025)", fontsize=14)
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95), fontsize=12)
    plt.xticks()
    plt.tight_layout()
    plt.savefig("images/5_1.svg")
    plt.show()


def grafica_5_2(df):
    fig, ax = plt.subplots(figsize=(18, 7))

    df_grouped_contratos = df.groupby("año")[
        ["contratos__agricultura", "contratos__industria", "contratos_construcción", "contratos__servicios"]
    ].sum()

    df_grouped_dtes = df.groupby("año")[
        ["dtes_empleoagricultura", "dtes_empleo_industria", "dtes_empleo_construcción", "dtes_empleo_servicios"]
    ].sum()

    colores_contratos = {
        "contratos__agricultura": "#2ca02c", 
        "contratos__industria": "#E3962B", 
        "contratos_construcción": "#d62728",
        "contratos__servicios": "#1f77b4", 
    }

    colores_dtes = {
        "dtes_empleoagricultura": "#a2d5a2",
        "dtes_empleo_industria": "#FAD887", 
        "dtes_empleo_construcción": "#FAA998", 
        "dtes_empleo_servicios": "#7ec8e3",  
    }

    bar_width = 0.20
    x = np.arange(len(df_grouped_contratos)) 
    offset = bar_width 

    for i, sector in enumerate(df_grouped_dtes.columns):
        ax.bar(x + i * offset, df_grouped_dtes[sector], bar_width, label=f"Demandantes {sector.replace('dtes_empleo', '').replace('_', ' ').title()}", color=colores_dtes[sector])

    for i, sector in enumerate(df_grouped_contratos.columns):
        ax.bar(x + i * offset, df_grouped_contratos[sector], bar_width, label=f"Contratos {sector.replace('__', ' ').title()}", color=colores_contratos[sector], alpha=0.7)

    ax.set_xlabel("Año", fontsize=14)
    ax.set_ylabel("Cantidad", fontsize=14)
    ax.set_title("Comparativa anual de Contratos y Demandantes de Empleo por Sector (2010-2025)", fontsize=18)
    ax.legend(loc="upper left", bbox_to_anchor=(0.8, 1), fontsize=12)
    ax.set_xticks(x + bar_width * 1.5)
    ax.set_xticklabels(df_grouped_contratos.index)
    plt.tight_layout()
    plt.savefig("images/5_2.svg")
    plt.show()

def grafica_6(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    df_grouped = df.groupby("año")[[
        "dtes_empleo_hombre_edad_<_25", "dtes_empleo_hombre_edad_25_-45", "dtes_empleo_hombre_edad_>=45",
        "dtes_empleo_mujer_edad_<_25", "dtes_empleo_mujer_edad_25_-45", "dtes_empleo_mujer_edad_>=45"
    ]].sum()

    df_grouped["edad_<_25"] = df_grouped["dtes_empleo_hombre_edad_<_25"] + df_grouped["dtes_empleo_mujer_edad_<_25"]
    df_grouped["edad_25_-45"] = df_grouped["dtes_empleo_hombre_edad_25_-45"] + df_grouped["dtes_empleo_mujer_edad_25_-45"]
    df_grouped["edad_>=45"] = df_grouped["dtes_empleo_hombre_edad_>=45"] + df_grouped["dtes_empleo_mujer_edad_>=45"]
    df_grouped = df_grouped[["edad_<_25", "edad_25_-45", "edad_>=45"]]
    colores = {
        "edad_<_25": "blue",
        "edad_25_-45": "royalblue",
        "edad_>=45": "navy"
    }

    estilos = ["-", "--", ":"]
    for i, columna in enumerate(df_grouped.columns):
        ax1.plot(df_grouped.index, df_grouped[columna], 
                label=columna.replace("_", " ").replace("<", "< ").replace(">=", ">= "), 
                color=colores[columna], linestyle=estilos[i], linewidth=2)

    ax1.set_xlabel("Año", fontsize=12)
    ax1.set_ylabel("Número de Demandantes de Empleo", fontsize=12)
    ax1.tick_params(axis="y")
    plt.title("Evolución anual de Demandantes de Empleo por Edad (2010-2025)", fontsize=14)
    fig.legend(loc="upper left", bbox_to_anchor=(0.85, 0.95), fontsize=12)
    plt.tight_layout()
    plt.savefig("images/6.svg")
    plt.show()


def grafica_7_1(df):
    df_contratos = df.groupby("comunidad_autónoma")["total_contratos"].sum().sort_values()
    df_dtes = df.groupby("comunidad_autónoma")["total_dtes_empleo"].sum().sort_values()

    plt.figure(figsize=(12, 6))

    bar_width = 0.4
    x_pos_contratos = range(len(df_contratos))
    color_contratos = "#1f77b4" 
    color_demandantes = "#E3962B" 

    plt.barh(x_pos_contratos, df_contratos.values, height=bar_width, label="Contratos", color=color_contratos)
    x_pos_dtes = [x + bar_width for x in x_pos_contratos]
    plt.barh(x_pos_dtes, df_dtes.values, height=bar_width, label="Demandantes de Empleo", color=color_demandantes)
    plt.xlabel("Cantidad", fontsize=12)
    plt.ylabel("Comunidad Autónoma", fontsize=12)
    plt.title("Total de Contratos y Demandantes de Empleo por Comunidad Autónoma entre 2010 y 2025", fontsize=14)
    plt.yticks(x_pos_contratos, df_contratos.index)
    plt.legend(loc="upper left", bbox_to_anchor=(0.7, 0.6), fontsize=12)
    plt.tight_layout()
    plt.savefig("images/7_1.svg")
    plt.show()

def grafica_7_2(df):
    # Carga del shapefile utilizado
    gdf = gpd.read_file('mapa/se89_3_admin_ccaa_a_x.shp')

    anios = sorted(df['año'].unique())[-4:]
    fig, axes = plt.subplots(1, 4, figsize=(20, 6))
    cmap='Blues' 

    for i, anio in enumerate(anios):
        ax = axes[i] 
        df_anio = df[df['año'] == anio]
        df_grouped = df_anio.groupby('comunidad_autónoma')['total_contratos'].sum().reset_index()
        merged = gdf.set_index('rotulo').join(df_grouped.set_index('comunidad_autónoma'))
        mapa = merged.plot(column='total_contratos', ax=ax, cmap=cmap, edgecolor='black')
        ax.set_title(f"Año {anio}", fontsize=10)
        ax.axis('off')

    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02]) 
    sm = plt.cm.ScalarMappable(cmap=cmap)
    fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="Índice de Contratos")
    plt.suptitle("Índice de Contratos por Comunidad Autónoma en los Últimos 4 Años", fontsize=16)
    plt.savefig("images/7_2.svg")
    plt.show()

def grafica_8_1(df):
    df_q1_2022 = df[(df['año'] == 2022) & (df['mes'].isin([1, 2, 3, 4]))]  # Primer cuatrimestre
    df_q2_2022 = df[(df['año'] == 2022) & (df['mes'].isin([5, 6, 7, 8]))]  # Segundo cuatrimestre
    df_q3_2022 = df[(df['año'] == 2022) & (df['mes'].isin([9, 10, 11, 12]))]  # Tercer cuatrimestre

    df_q1_comunidades_autonomas = df_q1_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()
    df_q2_comunidades_autonomas = df_q2_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()
    df_q3_comunidades_autonomas = df_q3_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()

    data_boxplot = {
        "Enero - Abril": df_q1_comunidades_autonomas,
        "Mayo - Agosto": df_q2_comunidades_autonomas,
        "Septiembre - Diciembre": df_q3_comunidades_autonomas
    }

    df_boxplot = pd.DataFrame(data_boxplot)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df_boxplot, palette=["blue", "orange", "green"], width=0.75, ax=ax)
    ax.set_xlabel("Cuatrimestres del Año 2022", fontsize=12)
    ax.set_ylabel("Total de Contratos por Comunidad Autónoma", fontsize=12)
    ax.set_title("Distribución de Contratos de Servicios por Comunidad Autónoma en 2022", fontsize=14)

    legend_labels = ["1º Cuatrimestre", 
                    "2º Cuatrimestre", 
                    "3º Cuatrimestre"]
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in ["#1f77b4", "#E3962B", "#2ca02c"]]
    ax.legend(handles, legend_labels, bbox_to_anchor=(1.05, 1), loc="upper right", fontsize=10)
    plt.tight_layout()
    plt.savefig("images/8_1.svg")
    plt.show()

def grafica_8_2(df):
    df_q1_2022 = df[(df['año'] == 2022) & (df['mes'].isin([1, 2, 3, 4]))]  # Primer cuatrimestre
    df_q2_2022 = df[(df['año'] == 2022) & (df['mes'].isin([5, 6, 7, 8]))]  # Segundo cuatrimestre
    df_q3_2022 = df[(df['año'] == 2022) & (df['mes'].isin([9, 10, 11, 12]))]  # Tercer cuatrimestre

    df_q1_comunidades_autonomas = df_q1_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()
    df_q2_comunidades_autonomas = df_q2_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()
    df_q3_comunidades_autonomas = df_q3_2022.groupby('comunidad_autónoma')['contratos__servicios'].sum()

    data_outliers = {
        "1º Cuatrimestre": df_q1_comunidades_autonomas,
        "2º Cuatrimestre": df_q2_comunidades_autonomas,
        "3º Cuatrimestre": df_q3_comunidades_autonomas
    }

    df_outliers = pd.DataFrame(data_outliers)

    def detectar_outliers(df):
        outliers_dict = {}
        for trimestre in df.columns:
            Q1 = df[trimestre].quantile(0.25)
            Q3 = df[trimestre].quantile(0.75)
            IQR = Q3 - Q1
            limite_superior = Q3 + 1.5 * IQR  
            outliers = df[df[trimestre] > limite_superior][trimestre]
            outliers_dict[trimestre] = outliers
        return outliers_dict

    outliers = detectar_outliers(df_outliers)
    df_outliers_plot = pd.concat(outliers, axis=1).reset_index()
    df_outliers_plot = df_outliers_plot.melt(id_vars="comunidad_autónoma", 
                                            var_name="Cuatrimestre", 
                                            value_name="Total de Contratos").dropna()

    sns.set(style="whitegrid")
    plt.figure(figsize=(9, 5))
    sns.barplot(data=df_outliers_plot, x="comunidad_autónoma", y="Total de Contratos", 
                hue="Cuatrimestre", palette=["blue", "orange", "green"])
    plt.xlabel("Comunidad Autónoma", fontsize=12)
    plt.ylabel("Total de Contratos", fontsize=12)
    plt.title("Comunidades Autónomas con Valores Atípicos en Contratos en 2022", fontsize=14)
    plt.savefig("images/8_2.svg")
    plt.show()

def grafica_8_3(df):
    df_q2_2022 = df[(df['año'] == 2022) & (df['mes'].isin([5, 6, 7, 8]))]  # Segundo cuatrimestre
    df_q2_2022_valenciana = df_q2_2022[df_q2_2022['comunidad_autónoma'] == 'Comunitat Valenciana']
    df_q2_2022_andalucia = df_q2_2022[df_q2_2022['comunidad_autónoma'] == 'Andalucía']

    df_grouped_contratos_valenciana = df_q2_2022_valenciana.groupby("año")[
        ["contratos__agricultura", "contratos__industria", "contratos_construcción", "contratos__servicios"]
    ].sum()

    df_grouped_contratos_andalucia = df_q2_2022_andalucia.groupby("año")[
        ["contratos__agricultura", "contratos__industria", "contratos_construcción", "contratos__servicios"]
    ].sum()

    year_to_display = 2022
    df_pastel_valenciana = df_grouped_contratos_valenciana.loc[year_to_display]
    df_pastel_andalucia = df_grouped_contratos_andalucia.loc[year_to_display]

    colores = ["#2ca02c", "#E3962B", "#d62728", "#1f77b4"]  
    labels_sectores = ["Agricultura", "Industria", "Construcción", "Servicios"]

    fig, ax = plt.subplots(1, 2, figsize=(9, 5))  

    fig.suptitle("Distribución de Contratos por Sectores en el 2º Cuatrimestre de 2022", 
                fontsize=14)

    ax[0].pie(df_pastel_valenciana, autopct='%1.1f%%', startangle=140, colors=colores, 
            pctdistance=0.8, labels=None, wedgeprops={"linewidth": 1, "edgecolor": "white"})
    ax[0].set_title("Comunitat Valenciana", fontsize=12)

    ax[1].pie(df_pastel_andalucia, autopct='%1.1f%%', startangle=140, colors=colores, 
            pctdistance=0.8, labels=None, wedgeprops={"linewidth": 1, "edgecolor": "white"})
    ax[1].set_title("Andalucía", fontsize=12)

    fig.legend(labels_sectores, loc="lower center", ncol=4, fontsize=10)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig("images/8_3.svg")
    plt.show()


def main():
    df = cargar_datos("dataset_final.csv")

    # 1.1 Evolución temporal de contratos y demandantes de empleo entre 2010 y 2025
    grafica_1_1(df)

    # 1.2 Promedio mensual de contratos y demandantes de empleo
    grafica_1_2(df)

    # 2. Evolución anual de contratos y demandantes de empleo por género entre 2010 y 2025
    grafica_2(df)

    # 3. Dispersión anual de contratos y demandantes de empleo por género entre 2010 y 2025
    grafica_3(df)

    # 4.1 Evolución anual de contratos por género entre 2010 y 2025
    grafica_4_1(df)

    # 4.2 Evolución anual de contratos por tipo y género entre 2010 y 2025 (barras apiladas)
    grafica_4_2(df)

    # 4.3 Evolución anual de contratos por tipo y género entre 2010 y 2025 (líneas con indicador de reforma laboral)
    grafica_4_3(df)

    # 5.1 Evolución anual de contratos por sector entre 2010 y 2025
    grafica_5_1(df)

    # 5.2 Comparativa anual de contratos y demandantes de empleo por sector entre 2010 y 2025
    grafica_5_2(df)

    # 6. Evolución anual de demandantes de empleo por edad entre 2010 y 2025
    grafica_6(df)

    # 7.1 Total de contratos y demandantes de empleo por comunidad autónoma entre 2010 y 2025
    grafica_7_1(df)

    # 7.2 Índice de contratos por comunidad autónoma en los últimos 4 años (Mapas)
    grafica_7_2(df)

    # 8.1 Distribución de contratos de servicios por comunidad autónoma en 2022 (Boxplot)
    grafica_8_1(df)

    # 8.2 Comunidades autónomas con valores atípicos en contratos en 2022
    grafica_8_2(df)

    # 8.3 Distribución de contratos por sectores en el 2º cuatrimestre de 2022 (Pastel)
    grafica_8_3(df)

if __name__ == "__main__":
    main()

