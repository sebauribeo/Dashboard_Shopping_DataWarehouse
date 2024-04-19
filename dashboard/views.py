from django.shortcuts import render
from .models import H_Shopping_Cart, D_Products, D_Customers, D_Orders
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from django.db.models import Sum



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
    customer_ids = shopping_carts.values_list('customer_id', flat=True).distinct()
    fecha_actual = datetime.now()
    edades = []
    for customer_id in customer_ids:
        # Obtener el cliente
        customer = D_Customers.objects.get(customer_id=customer_id)
        
        # Calcular la edad del cliente
        edad = fecha_actual.year - customer.age
        edades.append(edad)

    # Calcular la distribución de edades
    distribucion_edades = {}
    for edad in edades:
        if edad not in distribucion_edades:
            distribucion_edades[edad] = 0
        
        # Incrementar el contador de la edad
        distribucion_edades[edad] += 1

    # Ordenar el diccionario por claves (edades) en orden ascendente
    distribucion_edades = dict(sorted(distribucion_edades.items()))

    # Crear los datos necesarios para el gráfico de barras
    x = list(distribucion_edades.keys())
    y = list(distribucion_edades.values())

    # Crear el gráfico de barras
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(xaxis_title='Edad', yaxis_title='Número de clientes')
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

    return render(request, 'dashboards/home.html', {
        'div_genero': div_genero,
        'div_ventas_producto_por_mes': div_ventas_producto_por_mes,
        'div_distribucion_edades': div_distribucion_edades,
        'div_histograma_ventas_por_ubicacion': div_histograma_ventas_por_ubicacion,
        'div_tendencia_compra': div_tendencia_compra,
        
        })