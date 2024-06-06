from django.shortcuts import render
from .models import H_Shopping_Cart, D_Products, D_Sales
from django.shortcuts import render
from .models import H_Shopping_Cart
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from datetime import datetime


def home(request):

# ----------¿EN QUÉ DÍAS SE GENERAN MÁS TRANSACCIONES?----------

    # Obtener los días con más transacciones
    top_days = (H_Shopping_Cart.objects
                .annotate(day=TruncDay('shopping_date'))
                .values('day')
                .annotate(count=Count('sales_id'))
                .order_by('-count')[:10])

    # Extraer los datos para el gráfico
    days = [entry['day'] for entry in top_days]
    counts = [entry['count'] for entry in top_days]
    
    # Formatear las fechas como cadenas legibles
    formatted_dates = [day.strftime('%Y-%m-%d') for day in days]

    # Crear el gráfico de líneas utilizando Plotly
    fig = go.Figure(data=[go.Scatter(x=counts, y=formatted_dates, mode='lines+markers')])
    fig.update_layout(
        title={
            'text': 'Días con Más Transacciones',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 24 
            }
        },
        xaxis_title='Cantidad de Transacciones',
        yaxis_title='Fechas',
        xaxis=dict(tickmode='linear')
    )

    div_transacciones = plot(fig, output_type='div', include_plotlyjs=False)

# ----------¿QUÉ ELEMENTOS SON LOS MÁS RECURRENTES?----------

    # Obtener los elementos más recurrentes
    most_common_elements = H_Shopping_Cart.objects.values('product_id').annotate(count=Count('product_id')).order_by('-count')[:10]
    
    # Extraer los datos para el gráfico
    element_ids = [entry['product_id'] for entry in most_common_elements]
    counts = [entry['count'] for entry in most_common_elements]
    
    # Obtener los nombres de los productos correspondientes a los IDs
    product_names = [D_Products.objects.get(product_id=product_id).product_name for product_id in element_ids]
    
    # Crear el gráfico de barras utilizando Plotly
    fig = go.Figure(data=[go.Bar(x=product_names, y=counts)])
    fig.update_layout(
        title={
            'text': 'Elementos Más Recurrentes',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 24 
            }
        },
        xaxis_title='Nombre del Producto',
        yaxis_title='Cantidad de Repeticiones',
        xaxis=dict(tickmode='linear')
    )
    
    div_elementos = plot(fig, output_type='div', include_plotlyjs=False)

# ----------¿CUÁLES ELEMENTOS SON LOS MÁS RECURRENTES DENTRO DEL TOP 10?----------

    # Obtener los elementos más recurrentes en product_id
    most_common_elements = H_Shopping_Cart.objects.values('product_id').annotate(count=Count('product_id')).order_by('-count')[:17]
    
    # Extraer los datos para el gráfico
    element_ids = [entry['product_id'] for entry in most_common_elements]
    counts = [entry['count'] for entry in most_common_elements]
    
    # Obtener los nombres de los productos correspondientes a los IDs
    product_names = [D_Products.objects.get(product_id=product_id).product_name for product_id in element_ids]
    
    # Crear el gráfico de pastel utilizando Plotly
    fig = go.Figure(data=[go.Pie(labels=product_names, values=counts)])
    fig.update_layout(
        title={
            'text': 'Top 10 Elementos Más Recurrentes',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 24 
            }
        },
    )
    
    div_elementos_top_10 = plot(fig, output_type='div', include_plotlyjs=False)

# ----------¿EN QUÉ DÍAS SE REALIZAN MÁS TRANSACCIONES DE LOS ELEMENTOS MÁS RECURRENTES?----------

    # Obtener los datos de la consulta SQL
    query_results = (H_Shopping_Cart.objects
                     .values('shopping_date', 'product__product_name')
                     .annotate(transaction_count=Count('*'))
                     .order_by('-transaction_count')[:10])

    # Preparar los datos para el gráfico
    transaction_dates = [result['shopping_date'] for result in query_results]
    product_names = [result['product__product_name'] for result in query_results]
    transaction_counts = [result['transaction_count'] for result in query_results]

    # Crear el gráfico de dispersión utilizando Plotly
    fig = go.Figure()

    for date, product, count in zip(transaction_dates, product_names, transaction_counts):
        fig.add_trace(go.Scatter(
            x=[date],
            y=[product],
            mode='markers',
            marker=dict(size=[count], sizemode='area', sizeref=2.*max(transaction_counts)/(40.**2), sizemin=4),
            text=f'{count} transacciones',
            name=product
        ))

    fig.update_layout(
        title={
            'text': 'Días con Más Transacciones de los Productos Más Recurrentes',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },  
        xaxis_title='Fecha',
        yaxis_title='Producto',
        showlegend=True
        
    )

    div_recurrentes = plot(fig, output_type='div', include_plotlyjs=False)

# ----------¿IDENTIFICAR SITUACIONES DE BORDE?----------

    return render(request, 'dashboards/home.html', {
        'div_transacciones': div_transacciones,
        'div_elementos': div_elementos,
        'div_elementos_top_10': div_elementos_top_10,
        'div_recurrentes': div_recurrentes,
        })
