import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PATH_SRC = os.path.join(os.getcwd(), "src/")
path_productos = os.path.join(PATH_SRC, "data_productos.xlsx")
path_pedidos = os.path.join(PATH_SRC, "data_pedidos.xlsx")


COL_DESCRIPCION_PRODUCTO = "descripcion"
COL_PRODUCTO_PEDIDO = "producto"
COL_CLIENTE_PEDIDO = "codvend"


def conver_data_productos(target_value):
    """
    Busca los 5 productos más parecidos a 'target_value' usando
    similitud de coseno sobre vectores TF-IDF (sin llamadas a APIs externas).
    """
    df_productos = pd.read_excel(path_productos)

    textos = df_productos[COL_DESCRIPCION_PRODUCTO].astype(str).tolist()

    # agregamos el término buscado al final del corpus para vectorizarlo junto al resto
    corpus = textos + [target_value]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    target_vector = tfidf_matrix[-1]
    productos_vectors = tfidf_matrix[:-1]

    similitudes = cosine_similarity(target_vector, productos_vectors).flatten()

    top5_idx = similitudes.argsort()[::-1][:5]

    resultado = df_productos.iloc[top5_idx].copy()
    resultado["similitud"] = similitudes[top5_idx].round(4)

    return resultado.to_dict(orient="records")


def conver_data_pedidos(target_value):
    """
    Dado un cliente (target_value), devuelve los 5 productos que más
    ha comprado ese cliente como venta sugerida.
    """
    df_pedidos = pd.read_excel(path_pedidos)

    filtro = df_pedidos[COL_CLIENTE_PEDIDO].astype(str).str.lower() == target_value
    pedidos_cliente = df_pedidos[filtro]

    if pedidos_cliente.empty:
        return {}

    ventas_sugeridas = (
        pedidos_cliente[COL_PRODUCTO_PEDIDO]
        .value_counts()
        .head(5)
    )

    return ventas_sugeridas.to_dict()