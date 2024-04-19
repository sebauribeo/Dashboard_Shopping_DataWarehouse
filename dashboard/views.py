from django.shortcuts import render
from .models import H_Shopping_Cart
import plotly.graph_objs as go
from plotly.offline import plot

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


#  ----------Ventas por categoría de producto por mes----------
#  ----------Ventas Semanales----------
#  ----------Distribución de Edades de los Compradores----------
#  ----------Ventas por Ubicación Geográfica----------
#  ----------Tendencia de Compra----------
#  ----------Distribución de Ventas por Método de Pago----------

    # Renderizar la plantilla y pasar el gráfico de Plotly
    return render(request, 'dashboards/home.html', {'div_genero': div_genero})