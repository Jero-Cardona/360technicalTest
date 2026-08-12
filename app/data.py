import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PATH_SRC = os.path.join(os.getcwd(), "app/media/")
path_productos = os.path.join(PATH_SRC, "data_productos.xlsx")
path_pedidos = os.path.join(PATH_SRC, "data_pedidos.xlsx")

# columnas de los archivos
# data_productos.xlsx:
# PLU, descripcion, codigo, coduni1, nomuni1, codpro, nompro, coduni2, tipo_inv
# -> "codigo" es el identificador de producto (hace match con pedidos.codpro)
# -> "descripcion" es el texto sobre el que se busca similitud
#
# data_pedidos.xlsx:

# codemp, codvend, tipoped, numped, nitcli, succli, fecped, codpro, refer,
# descrip, cantped, vlrbruped, ivabruped, vlrnetoped, estado, tipo, obsped
# -> "nitcli" es el CLIENTE (NIT). "codvend" es el VENDEDOR, no el cliente.
# -> "codpro" enlaza con productos.codigo


COL_ID_PRODUCTO = "codigo"
COL_DESCRIPCION_PRODUCTO = "descripcion"
COL_CATEGORIA_PRODUCTO = "nompro"

COL_CLIENTE_PEDIDO = "nitcli"
COL_PRODUCTO_PEDIDO = "codpro"
COL_CANTIDAD_PEDIDO = "cantped"
COL_ESTADO_PEDIDO = "estado"

ESTADOS_VALIDOS = {"Aprobado", "Cumplido", "Comprometido", "En elaboración"}


def conver_data_productos(target_value):
    """
    Busca los 5 productos cuya 'descripcion' es más similar a target_value,
    usando TF-IDF + similitud de coseno (100% local, sin API externa).
    """
    df_productos = pd.read_excel(path_productos)
    df_productos[COL_DESCRIPCION_PRODUCTO] = df_productos[COL_DESCRIPCION_PRODUCTO].astype(str)

    textos = df_productos[COL_DESCRIPCION_PRODUCTO].tolist()
    corpus = textos + [target_value]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    target_vector = tfidf_matrix[-1]
    productos_vectors = tfidf_matrix[:-1]

    similitudes = cosine_similarity(target_vector, productos_vectors).flatten()

    top5_idx = similitudes.argsort()[::-1][:5]

    resultado = df_productos.iloc[top5_idx][
        ["PLU", COL_ID_PRODUCTO, COL_DESCRIPCION_PRODUCTO, "nompro", "coduni1"]
    ].copy()
    resultado["similitud"] = similitudes[top5_idx].round(4)

    return resultado.to_dict(orient="records")


def conver_data_pedidos(target_value):
    """
    Dado un cliente (nitcli), devuelve el producto que más ha comprado (como una venta sugerida)
    (por cantidad total pedida), con su valores tomados de productos.xlsx.
    """
    df_pedidos = pd.read_excel(path_pedidos)
    df_productos = pd.read_excel(path_productos)

    df_pedidos = df_pedidos.drop_duplicates()

    # limipiar dataframe en base a los estados y el cliente seleccionado
    filtro_cliente = df_pedidos[COL_CLIENTE_PEDIDO].astype(str) == target_value
    filtro_estado = df_pedidos[COL_ESTADO_PEDIDO].isin(ESTADOS_VALIDOS)
    pedidos_cliente = df_pedidos[filtro_cliente & filtro_estado]

    if pedidos_cliente.empty:
        return {}

    top_product = (
        pedidos_cliente
        .groupby(COL_PRODUCTO_PEDIDO)[COL_CANTIDAD_PEDIDO]
        .sum()
        .sort_values(ascending=False)
        .head(1) # esto devuelve el producto con mayor cantidades pedidas por el cliente
    )
    
    productos_map_des = df_productos.set_index(COL_ID_PRODUCTO)[COL_DESCRIPCION_PRODUCTO]
    productos_map_cat = df_productos.set_index(COL_ID_PRODUCTO)[COL_CATEGORIA_PRODUCTO]

    sugerencias = []
    for codpro, cantidad_total in top_product.items():
        sugerencias.append({
            "codigo": int(codpro),
            "categoria": productos_map_cat.get(codpro, "Producto no encontrado en catálogo"),
            "descripcion": productos_map_des.get(codpro, "Producto no encontrado en catálogo"),
            "cantidad_total_pedida": int(cantidad_total),
        })

    return sugerencias