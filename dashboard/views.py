from django.shortcuts import render
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot

def home(request):
    # Datos aleatorios para simular las ventas por género
    generos = ['Masculino', 'Femenino']
    ventas_por_genero = np.random.randint(100, 1000, size=2)

    # Gráfico de pastel para las ventas por género
    fig_genero = go.Figure(data=[go.Pie(labels=generos, values=ventas_por_genero)])
    div_genero = plot(fig_genero, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular las ventas por categoría de producto por mes
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
    categorias_productos_mes = ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E']
    ventas_por_categoria_mes = np.random.randint(100, 1000, size=(len(meses), len(categorias_productos_mes)))

    # Gráfico de barras apiladas para las ventas por categoría de producto por mes
    fig_categoria_mes = go.Figure()
    for i, mes in enumerate(meses):
        fig_categoria_mes.add_trace(go.Bar(name=mes, x=categorias_productos_mes, y=ventas_por_categoria_mes[i]))

    fig_categoria_mes.update_layout(barmode='stack')
    div_categoria_mes = plot(fig_categoria_mes, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular las ventas semanales
    semanas = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
    ventas_semanales = np.random.randint(100, 1000, size=len(semanas))

    # Gráfico de barras para las ventas semanales
    fig_semanal = go.Figure([go.Bar(x=semanas, y=ventas_semanales)])
    div_semanal = plot(fig_semanal, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular las edades de los compradores
    edades = np.random.randint(18, 70, size=100)

    # Histograma para la edad de los compradores
    fig_edad = go.Figure(data=[go.Histogram(x=edades)])
    div_edad = plot(fig_edad, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular ubicaciones geográficas de los clientes
    ubicaciones = ['Ciudad A', 'Ciudad B', 'Ciudad C', 'Ciudad D', 'Ciudad E']
    ventas_por_ubicacion = np.random.randint(100, 1000, size=len(ubicaciones))

    # Gráfico de barras para las ventas por ubicación geográfica
    fig_ubicacion = go.Figure([go.Bar(x=ubicaciones, y=ventas_por_ubicacion)])
    div_ubicacion = plot(fig_ubicacion, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular tendencias de compra
    fechas = np.arange('2024-01-01', '2024-12-31', dtype='datetime64[D]')
    ventas_diarias = np.random.randint(100, 1000, size=len(fechas))

    # Gráfico de líneas para la tendencia de compra
    fig_tendencia = go.Figure(data=[go.Scatter(x=fechas, y=ventas_diarias)])
    div_tendencia = plot(fig_tendencia, output_type='div', include_plotlyjs=False)

    # Datos aleatorios para simular la distribución de ventas por método de pago
    metodos_pago = ['Efectivo', 'Tarjeta de Crédito', 'Transferencia Bancaria']
    ventas_por_metodo_pago = np.random.randint(100, 1000, size=len(metodos_pago))

    # Gráfico de barras para la distribución de ventas por método de pago
    fig_metodo_pago = go.Figure([go.Bar(x=metodos_pago, y=ventas_por_metodo_pago)])
    div_metodo_pago = plot(fig_metodo_pago, output_type='div', include_plotlyjs=False)

    return render(request, 'dashboards/home.html', {
        'div_genero': div_genero,
        'div_categoria_mes': div_categoria_mes,
        'div_semanal': div_semanal,
        'div_edad': div_edad,
        'div_ubicacion': div_ubicacion,
        'div_tendencia': div_tendencia,
        'div_metodo_pago': div_metodo_pago,
    })