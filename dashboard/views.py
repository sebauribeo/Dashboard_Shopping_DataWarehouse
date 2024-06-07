from django.shortcuts import render
from .models import H_Shopping_Cart, D_Products, D_Sales, D_Customers, D_Orders
from django.shortcuts import render
from .models import H_Shopping_Cart
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
import pandas as pd
import numpy as np

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
#-----------------------------------------------------------------------------------------------------------------
    # Obtener transacciones con cantidades extremas
    extreme_transactions = (H_Shopping_Cart.objects
                            .values('product_id')
                            .annotate(total_quantity=Sum('sales__quantity'))
                            .order_by('-total_quantity')[:10])

    product_ids = [transaction['product_id'] for transaction in extreme_transactions]
    total_quantities = [transaction['total_quantity'] for transaction in extreme_transactions]
    product_names = [D_Products.objects.get(product_id=product_id).product_name for product_id in product_ids]

    # Crear el gráfico de dispersión utilizando Plotly
    fig = go.Figure()

    for product, quantity in zip(product_names, total_quantities):
        fig.add_trace(go.Scatter(
            x=[product],
            y=[quantity],
            mode='markers',
            marker=dict(size=[quantity], sizemode='area', sizeref=2.*max(total_quantities)/(40.**2), sizemin=4),
            text=f'{quantity} unidades vendidas',
            name=product
        ))

    fig.update_layout(
        title={
            'text': 'Transacciones con Cantidades Extremas',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },
        xaxis_title='Producto',
        yaxis_title='Cantidad Total Vendida',
        showlegend=True
    )

    div_extreme_transactions = plot(fig, output_type='div', include_plotlyjs=False)

#-----------------------------------------------------------------------------------------------------------------
    # Obtener datos de ventas
    sales_data = (H_Shopping_Cart.objects
                  .values('product_id')
                  .annotate(total_quantity=Sum('sales__quantity')))

    quantities = [sale['total_quantity'] for sale in sales_data]
    product_names = [D_Products.objects.get(product_id=sale['product_id']).product_name for sale in sales_data]

    # Crear el box plot utilizando Plotly
    fig = go.Figure(go.Box(
        y=quantities,
        boxpoints='outliers',
        text=product_names,
    ))

    fig.update_layout(
        title={
            'text': 'Distribución de Cantidades Vendidas',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },
        yaxis_title='Cantidad Total Vendida',
        showlegend=False
    )

    div_quantity_distribution = plot(fig, output_type='div', include_plotlyjs=False)

#-----------------------------------------------------------------------------------------------------------------
    # Obtener datos de ventas diarias
    sales_data = (H_Shopping_Cart.objects
                  .values('shopping_date')
                  .annotate(total_sales=Sum('sales__total_price'))
                  .order_by('shopping_date'))

    # Preparar los datos para el gráfico
    dates = [data['shopping_date'] for data in sales_data]
    total_sales = [data['total_sales'] for data in sales_data]

    # Crear un DataFrame para facilitar la manipulación de datos
    df = pd.DataFrame({'date': dates, 'total_sales': total_sales})
    df.set_index('date', inplace=True)

    # Crear el gráfico lineal utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['total_sales'],
        mode='lines+markers',
        name='Ventas diarias'
    ))

    fig.update_layout(
        title={
            'text': 'Tendencia de Ventas Diarias',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },
        xaxis_title='Fecha',
        yaxis_title='Ventas Totales',
        showlegend=True
    )

    div_daily_sales_trend = plot(fig, output_type='div', include_plotlyjs=False)

#-----------------------------------------------------------------------------------------------------------------
    # Obtener la información sobre datos nulos en cada tabla
    null_info = {
        'H_Shopping_Cart': get_null_info(H_Shopping_Cart),
        'D_Customers': get_null_info(D_Customers),
        'D_Sales': get_null_info(D_Sales),
        'D_Products': get_null_info(D_Products),
        'D_Orders': get_null_info(D_Orders),
    }

    # Verificar si hay datos nulos en cada tabla
    null_data = {table: any(info.values()) for table, info in null_info.items()}

    # Crear gráfico de pastel para mostrar si hay datos nulos o no
    if any(null_data.values()):
        labels = list(null_data.keys())
        values = [1 if has_null else 0 for has_null in null_data.values()]
        colors = generate_color_palette(len(labels))

        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            hole=0.3,
            text=['Hay datos nulos' if has_null else 'No hay datos nulos' for has_null in null_data.values()],
            textinfo='percent+label'
        ))

        fig.update_layout(
            title={
            'text': 'Datos Nulos en Cada Tabla',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },
        )
    else:
        fig = go.Figure(go.Scatter(
            x=[0],
            y=[0],
            mode='text',
            text=['No hay datos nulos en ninguna tabla'],
            textposition='middle center'
        ))

        fig.update_layout(
            title='No hay Datos Nulos',
            xaxis_visible=False,
            yaxis_visible=False
        )

    div_null_chart = plot(fig, output_type='div', include_plotlyjs=False)

#-----------------------------------------------------------------------------------------------------------------
    # Campos de interés para verificar valores repetidos
    fields = ['order_id', 'sales_id', 'product_id', 'customer_id', 'shopping_date']

    # Inicializar el diccionario para almacenar los datos repetidos en cada campo
    duplicate_data = {field: [] for field in fields}

    # Obtener los datos repetidos en cada campo
    for field in fields:
        duplicates = H_Shopping_Cart.objects.values(field).annotate(count=Count(field)).filter(count__gt=1)
        for entry in duplicates:
            duplicate_data[field].append(entry[field])

    # Calcular la cantidad total de datos repetidos
    total_duplicates = sum(len(duplicates) for duplicates in duplicate_data.values())

    # Preparar los datos para el gráfico de donut
    field_names = list(duplicate_data.keys())
    duplicate_counts = [len(duplicates) for duplicates in duplicate_data.values()]

    # Crear el gráfico de donut utilizando Plotly
    fig = go.Figure(go.Pie(
        labels=field_names,
        values=duplicate_counts,
        hole=0.3,
    ))

    fig.update_traces(hoverinfo='label+percent', textinfo='value')

    fig.update_layout(
        title={
            'text': 'Proporción de Datos Repetidos en Cada Campo',
            'y': 0.9, 
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': {
                'size': 20 
            }
        },
    )

    div_duplicate_chart = plot(fig, output_type='div', include_plotlyjs=False)


    return render(request, 'dashboards/home.html', {
        'div_transacciones': div_transacciones,
        'div_elementos': div_elementos,
        'div_elementos_top_10': div_elementos_top_10,
        'div_recurrentes': div_recurrentes,
        'div_extreme_transactions': div_extreme_transactions,
        'div_quantity_distribution': div_quantity_distribution,
        'div_daily_sales_trend': div_daily_sales_trend,
        'div_null_chart': div_null_chart,
        'div_duplicate_chart': div_duplicate_chart
        })

def get_null_info(model):
    # Obtener información sobre datos nulos en el modelo
    null_info = {}
    fields = model._meta.get_fields()
    for field in fields:
        field_name = field.name
        null_info[field_name] = model.objects.filter(**{f'{field_name}__isnull': True}).exists()
    return null_info

def generate_color_palette(num_colors):
    # Generar una paleta de colores única
    palette = np.array([
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ])
    return palette[:num_colors].tolist()
