from django.db import models

class D_Orders(models.Model):
    try:
        order_id = models.IntegerField(primary_key=True)
        customer_id = models.IntegerField()
        payment = models.IntegerField()
        order_date = models.DateField()
        delivery_date = models.DateField()
        
    except Exception as e:
        print('Modelo no creado: ', e)

class D_Customers(models.Model):
    try:
        customer_id = models.IntegerField(primary_key=True)
        customer_name = models.CharField(max_length=200)
        gender = models.CharField(max_length=100)
        age = models.IntegerField()
        home_address = models.CharField(max_length=500)
        zip_code = models.IntegerField()
        city = models.CharField(max_length=250)
        state = models.CharField(max_length=150)
        country = models.CharField(max_length=150)

    except Exception as e:
        print('Modelo no creado: ', e)

class D_Sales(models.Model):
    try:
        sales_id = models.IntegerField(primary_key=True)
        order_id = models.IntegerField()
        product_id = models.IntegerField()
        price_per_unit = models.IntegerField()
        quantity = models.IntegerField()
        total_price = models.IntegerField()

    except Exception as e:
        print('Modelo no creado: ', e)

class D_Products(models.Model):
    try:
        product_id = models.IntegerField(primary_key=True)
        product_type = models.CharField(max_length=100)
        product_name = models.CharField(max_length=200)
        size = models.CharField(max_length=100)
        colour = models.CharField(max_length=100)
        price = models.IntegerField()
        quantity = models.IntegerField()
        description = models.CharField(max_length=500)

    except Exception as e:
        print('Modelo no creado: ', e)

class H_Shopping_Cart(models.Model):
    try:
        sales = models.ForeignKey(D_Sales, on_delete=models.CASCADE)
        product = models.ForeignKey(D_Products, on_delete=models.CASCADE)
        order = models.ForeignKey(D_Orders, on_delete=models.CASCADE)
        customer = models.ForeignKey(D_Customers, on_delete=models.CASCADE)
        shopping_date = models.DateField()

    except Exception as e:
        print('Modelo no creado: ', e)
