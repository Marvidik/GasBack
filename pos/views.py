from django.shortcuts import render
from .models import Product,Sales,Amount,Expenses
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET'])
def individual_sales(request, id):
    # Filter sales for the specified worker and order by date descending
    data = Sales.objects.filter(worker=id).order_by('-date', 'id')

    # Serialize the data
    serializer = SalesSerializer(instance=data, many=True)

    return Response({'worker_sales': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_sales(request):
    data=Sales.objects.all()

    serializer=SalesSerializer(instance=data,many=True)

    return Response({'worker_sales': serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def workers_sales_stats(request, id):
    try:
        # Filter sales for the worker
        sales = Sales.objects.filter(worker_id=id)

        # Aggregate total amount bought and total amount paid
        stats = sales.aggregate(
            total_sales=Sum('amount_bought'),
            total_money_made=Sum('amount_paid')
        )

        return Response({
            "worker_id": id,
            "total_sales": stats["total_sales"] or 0,  # Handle case where there's no sales
            "total_money_made": stats["total_money_made"] or 0
        })
    except Sales.DoesNotExist:
        return Response({"error": "Worker not found"}, status=404)
    
@api_view(["GET"])
def workers_sales_stats_today(request, id):
    try:
        # Get the current date
        today = datetime.now().date()

        # Filter sales for the worker on the current date
        sales = Sales.objects.filter(worker_id=id, date__date=today)

        # Aggregate total amount bought and total amount paid
        stats = sales.aggregate(
            total_sales=Sum('amount_bought'),
            total_money_made=Sum('amount_paid')
        )

        return Response({
            "worker_id": id,
            "date": today,
            "total_sales": stats["total_sales"] or 0,
            "total_money_made": stats["total_money_made"] or 0
        })
    except Sales.DoesNotExist:
        return Response({"error": "Worker not found"}, status=404)
    
@api_view(["GET"])
def general_stats_today(request):
    # Get the current date
    today = datetime.now().date()

    # Filter sales for the current date
    sales = Sales.objects.filter(date__date=today)

    # Aggregate total amount bought and total amount paid
    stats = sales.aggregate(
        total_sales=Sum('amount_bought'),
        total_money_made=Sum('amount_paid')
    )

    return Response({
        "date": today,
        "total_sales": stats["total_sales"] or 0,
        "total_money_made": stats["total_money_made"] or 0
    })


@api_view(["GET"])
def general_stats(request):

    # Filter sales for the current date
    sales = Sales.objects.all()

    # Aggregate total amount bought and total amount paid
    stats = sales.aggregate(
        total_sales=Sum('amount_bought'),
        total_money_made=Sum('amount_paid')
    )

    return Response({
        "total_sales": stats["total_sales"] or 0,
        "total_money_made": stats["total_money_made"] or 0
    })


@api_view(["POST"])
def create_sale(request):
    # Extract the data from the request
    data = request.data

    try:
        # Get worker details
        worker_id = data.get('worker_id')
        worker = User.objects.get(id=worker_id)
        
        # Get the customer details and sale info
        customer = data.get('customer')
        phone = data.get('phone')
        amount_bought = int(data.get('amount_bought'))
        amount_paid = int(data.get('amount_paid'))
        payment_option = data.get('payment_option')

        # Get the latest product by order of creation or date
        latest_product = Product.objects.latest('id')

        # Ensure all fields are provided
        if not all([worker_id, customer, phone, amount_bought, amount_paid, payment_option]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if enough product quantity is available
        if latest_product.quantity < amount_bought:
            return Response({"error": "Not enough product available"}, status=status.HTTP_400_BAD_REQUEST)

        # If enough quantity, create the sale and update product quantity
        sale = Sales.objects.create(
            worker=worker,
            customer=customer,
            phone=phone,
            amount_bought=amount_bought,
            amount_paid=amount_paid,
            payment_option=payment_option
        )

        # Reduce the product quantity
        latest_product.quantity -= amount_bought
        latest_product.save()

        return Response({
            "message": "Sale created successfully",
            "sale_id": sale.id,
            "remaining_quantity": latest_product.quantity
        }, status=status.HTTP_201_CREATED)

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    except User.DoesNotExist:
        return Response({"error": "Worker not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def calculate_total_expenses(request):
    try:
        # Aggregate total expenses
        total_expenses = Expenses.objects.aggregate(total_amount=Sum('amount'))

        return Response({
            "total_expenses": total_expenses["total_amount"] or 0  # Return 0 if no expenses exist
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def price(request):
    try:
        # Get the latest Amount entry
        last_amount = Amount.objects.latest('id')  # Assuming 'id' is the auto-incrementing primary key
        
        return Response({
            "price": last_amount.price
        }, status=status.HTTP_200_OK)

    except Amount.DoesNotExist:
        return Response({"error": "No entries found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def calculate_total_revenue(request):
    try:
        # Aggregate total revenue from amount_paid
        total_revenue = Sales.objects.aggregate(total_amount=Sum('amount_paid'))

        return Response({
            "total_revenue": total_revenue["total_amount"] or 0  # Return 0 if no sales exist
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def calculate_worker_daily_revenue(request, worker_id):
    try:
        # Get the worker by ID
        worker = get_object_or_404(User, id=worker_id)

        # Get the current date
        today = datetime.now().date()

        # Aggregate total revenue from amount_paid for the specified worker for today
        total_revenue = Sales.objects.filter(worker=worker, date__date=today).aggregate(total_amount=Sum('amount_paid'))

        return Response({
            "worker_id": worker.id,
            "worker_username": worker.username,
            "total_daily_revenue": total_revenue["total_amount"] or 0  # Return 0 if no sales exist for today
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)