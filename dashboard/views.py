from django.shortcuts import render
from .models import H_Shopping_Cart, D_Products, D_Customers, D_Orders
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from django.db.models import Sum
from collections import Counter
from django.db.models.functions import TruncMonth


def home(request):

# ----------Calcular la cantidad de ventas por género----------
    shopping_carts = H_Shopping_Cart.objects.all()
    generos = {}
    for cart in shopping_carts:
        if cart.gender in generos:
            generos[cart.gender] += 1
        else:
            generos[cart.gender] = 1

    # Crear el gráfico de pastel utilizando Plotly
    labels = list(generos.keys())
    values = list(generos.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div_genero = plot(fig, output_type='div', include_plotlyjs=False)


#  ----------Ventas por Tipo de Producto por Mes----------
    shopping_carts = H_Shopping_Cart.objects.all()
    ventas_por_producto_por_mes = {}
    for cart in shopping_carts:
        # Obtener el mes y el año de la fecha de la orden
        mes_ano = cart.order_date.strftime('%Y-%m')

        # Obtener el producto asociado a la venta
        producto = D_Products.objects.get(pk=cart.product_id)

        # Obtener o crear una entrada para el producto en el diccionario
        if producto.product_type not in ventas_por_producto_por_mes:
            ventas_por_producto_por_mes[producto.product_type] = {}

        # Obtener o crear una entrada para el mes y año en el diccionario del producto
        if mes_ano not in ventas_por_producto_por_mes[producto.product_type]:
            ventas_por_producto_por_mes[producto.product_type][mes_ano] = 0

        # Incrementar las ventas para el producto y el mes correspondiente
        ventas_por_producto_por_mes[producto.product_type][mes_ano] += 1

    # Crear los datos necesarios para el gráfico de barras
    data = []
    for producto, ventas_por_mes in ventas_por_producto_por_mes.items():
        x = list(ventas_por_mes.keys())
        y = list(ventas_por_mes.values())
        data.append(go.Bar(name=producto, x=x, y=y))

    # Crear la figura del gráfico de barras
    fig = go.Figure(data=data)
    fig.update_layout(barmode='group', xaxis_title='Mes-Año', yaxis_title='Ventas')
    div_ventas_producto_por_mes = plot(fig, output_type='div', include_plotlyjs=False)


#  ----------Distribución de Edades de los Compradores----------
    shopping_carts = H_Shopping_Cart.objects.all()

    # Obtener una lista de IDs únicos de clientes
    customer_ids = shopping_carts.values_list('customer_id', flat=True).distinct()
    fecha_actual = datetime.now()

    # Crear una lista para almacenar las edades actuales de los clientes
    edades_actuales = []

    # Iterar sobre cada cliente
    for customer_id in customer_ids:
        # Obtener el cliente
        customer = D_Customers.objects.get(customer_id=customer_id)

        # Calcular la edad actual del cliente
        edad_actual = fecha_actual.year - customer.age

        # Agregar la edad actual a la lista
        edades_actuales.append(edad_actual)

    # Calcular la distribución de edades
    distribucion_edades = {}

    # Contar el número de clientes en cada edad
    for edad in edades_actuales:
        if edad not in distribucion_edades:
            distribucion_edades[edad] = 0
        distribucion_edades[edad] += 1

    # Ordenar el diccionario por claves (edades) en orden ascendente
    distribucion_edades = dict(sorted(distribucion_edades.items()))

    # Crear los datos necesarios para el gráfico de barras
    x = list(distribucion_edades.keys())
    y = list(distribucion_edades.values())

    # Crear el gráfico de barras
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(xaxis_title='Año de nacimiento', yaxis_title='Número de Clientes')

    # Generar el gráfico de barras como HTML
    div_distribucion_edades = plot(fig, output_type='div', include_plotlyjs=False)


#  ----------Ventas por Ubicación Geográfica----------
    shopping_carts = H_Shopping_Cart.objects.all()
    ubicaciones = []
    for cart in shopping_carts:
        # Obtener el cliente asociado a la venta
        customer = D_Customers.objects.get(customer_id=cart.customer_id)

        # Obtener la ubicación geográfica del cliente
        ubicacion = f"{customer.city}, {customer.country}"

        # Agregar la ubicación geográfica a la lista
        ubicaciones.append(ubicacion)

    # Crear el histograma de ventas por ubicación geográfica
    fig = go.Figure(data=[go.Histogram(x=ubicaciones)])
    fig.update_layout(xaxis_title='Ubicación', yaxis_title='Número de Ventas')
    div_histograma_ventas_por_ubicacion = plot(fig, output_type='div', include_plotlyjs=False)


#  ----------Tendencia de Compra----------
    shopping_carts = H_Shopping_Cart.objects.all()
    ventas_por_periodo = {}
    for cart in shopping_carts:
        # Obtener el mes y año de la fecha de la orden
        periodo = cart.order_date.strftime('%Y-%m')

        # Obtener o crear una entrada para el período en el diccionario
        if periodo not in ventas_por_periodo:
            ventas_por_periodo[periodo] = 0

        # Incrementar las ventas para el período correspondiente
        ventas_por_periodo[periodo] += 1

    # Ordenar el diccionario por claves (períodos) en orden ascendente
    ventas_por_periodo = dict(sorted(ventas_por_periodo.items()))

    # Crear los datos necesarios para el gráfico de líneas
    x = list(ventas_por_periodo.keys())
    y = list(ventas_por_periodo.values())

    # Crear el gráfico de líneas
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    fig.update_layout(xaxis_title='Período', yaxis_title='Número de Ventas')
    div_tendencia_compra = plot(fig, output_type='div', include_plotlyjs=False)


#------------Top 10 de Personas que Más Compras Han Realizado------------
    shopping_carts = H_Shopping_Cart.objects.all()

    # Obtener una lista de los nombres de las personas que han realizado compras
    nombres_compradores = [cart.customer_name for cart in shopping_carts]

    # Contar cuántas compras ha realizado cada persona y obtener el top 10
    top_nombres_compradores = Counter(nombres_compradores).most_common(10)

    # Separar los nombres y las cantidades en listas separadas
    nombres_top_10 = [nombre for nombre, cantidad in top_nombres_compradores]
    cantidades_top_10 = [cantidad for nombre, cantidad in top_nombres_compradores]

    # Crear el gráfico de barras
    fig = go.Figure([go.Bar(x=nombres_top_10, y=cantidades_top_10)])
    fig.update_layout(xaxis_title='Nombre del Comprador', yaxis_title='Número de Compras')
    div_top_10_compradores = plot(fig, output_type='div', include_plotlyjs=False)


    #----------Cantidad de Ventas por Nombre de Producto----------
    shopping_carts = H_Shopping_Cart.objects.all()
    product_ids = shopping_carts.values_list('product_id', flat=True).distinct()

    # Obtener los nombres de los productos vendidos
    nombres_productos = [D_Products.objects.get(product_id=product_id).product_name for product_id in product_ids]

    # Contar cuántas veces se ha vendido cada producto
    ventas_por_producto = Counter(nombres_productos)

    # Crear los datos necesarios para el gráfico de pastel
    labels = list(ventas_por_producto.keys())
    values = list(ventas_por_producto.values())

    # Crear el gráfico de pastel
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div_ventas_por_producto = plot(fig, output_type='div', include_plotlyjs=False)


#----------Cantidad de Productos por Talla----------
    shopping_carts = H_Shopping_Cart.objects.all()

    # Obtener una lista de todas las tallas de los productos vendidos
    tallas = [cart.product.size for cart in shopping_carts if cart.product]

    # Contar cuántos productos hay por talla
    productos_por_talla = Counter(tallas)

    # Crear una lista de colores para cada talla
    colores = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

    # Crear los datos necesarios para el gráfico de barras
    x = list(productos_por_talla.keys())
    y = list(productos_por_talla.values())

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=colores))])
    fig.update_layout(xaxis_title='Talla', yaxis_title='Cantidad')
    div_productos_por_talla = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'dashboards/home.html', {
        'div_genero': div_genero,
        'div_ventas_producto_por_mes': div_ventas_producto_por_mes,
        'div_distribucion_edades': div_distribucion_edades,
        'div_histograma_ventas_por_ubicacion': div_histograma_ventas_por_ubicacion,
        'div_tendencia_compra': div_tendencia_compra,
        'div_top_10_compradores': div_top_10_compradores,
        'div_ventas_por_producto':div_ventas_por_producto,
        'div_productos_por_talla': div_productos_por_talla,
        })