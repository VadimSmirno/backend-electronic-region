from django.urls import path
from . import views

urlpatterns = [

    path('find_routes/<int:land_plot_gid>/<str:start_point_lat>/<str:start_point_lon>/', views.find_routes_to_land_plot, name='find_routes'),
    path('find_rout_form/', views.find_route, name='find_rout_form'),
    path('land-plot-list/', views.land_plot_list, name='land_plot_list'),
    path('land-plot/<int:land_plot_id>/', views.land_plot_detail, name='land_plot_detail'),
]