
from django.urls import path
from .views import * 

urlpatterns = [
    path("worker_sales/<id>", individual_sales,name="workers-sales"),
    path("all_sales",all_sales,name="all_sales"),
    path("workers_stats/<id>",workers_sales_stats,name="workers_stats"),
    path("workers_stats_today/<id>",workers_sales_stats_today,name="today_workers_stats"),
    path("all_stats_today/", general_stats_today, name="general_stats"),
    path("all_stats",general_stats,name="general_stats"),
    path("add_sales",create_sale,name="add_sales"),
    path("total_expenses",calculate_total_expenses,name="total_expense"),
    path("price",price,name="price"),
    path("revenue",calculate_total_revenue,name="revenue"),
    path("workers_revenue/<worker_id>",calculate_worker_daily_revenue,name="workers_revenue"),
    path("other_products",get_products,name="products"),
    path("prodsale/",CreatePSalesView.as_view(),name="productsale"),
    path("individual_product_sale/<id>",individual_other_sales,name="prodsales")
]
