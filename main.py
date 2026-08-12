from fastapi import FastAPI
from data import conver_data_pedidos, conver_data_productos, path_pedidos, pd

app = FastAPI()

# @app.get('/')
# def get_root():
#     return {'Hellow': 'World'}

# construccion de endpoint principal
@app.get('/consulta/{categoria}/{target_value}', tags=['Productos'])
def get_producto(categoria: str, target_value: str):
    
    cat_value = categoria.lower()
    tar_value = target_value.lower()
    
    if cat_value == 'productos':
        response = conver_data_productos(tar_value)
    
    if cat_value == 'pedidos':
        response = conver_data_pedidos(tar_value)

# endpoitn de consulta de clientes
@app.get('/clientes')
def get_clientes():
    
    # leer dataframe pedidos
    df_pedidos = pd.read_excel(path_pedidos)
    clients =  df_pedidos['codvend'].astype(str).to_list()
    
    # limpiar lista y valores duplicados
    clients_array = []    
    for c in clients:
        if c not in clients_array:
            clients_array.append(c)
    return clients_array


