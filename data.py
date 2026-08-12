import os
import pandas as pd

PATH_SRC = os.path.join(os.getcwd(), "src/")
path_productos = os.path.join(PATH_SRC, "data_productos.xlsx")
path_pedidos = os.path.join(PATH_SRC, "data_pedidos.xlsx")


def conver_data_productos(target_value):
    
    similar_products = {}
    
    # leer el dataframe de productos
    df_productos = pd.read_excel(path_productos)
    return similar_products


def conver_data_pedidos(target_value):
    
    suggested_sale = {}
    
    # leer el dataframe de pedidos
    df_pedidos = pd.read_excel(path_pedidos)
    return suggested_sale

