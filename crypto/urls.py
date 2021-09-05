from django.urls import path
from .views import base_views, pumping_views, strategy_views, cross_views

urlpatterns = [
    path('', base_views.index, name='index'),
    path('pumping', pumping_views.pumping, name='pumping'),
    path('pumpingChart', pumping_views.pumpingChart, name='pumpingChart'),
    path('strategy', strategy_views.strategy, name='strategy'),
    path('strategyChart', strategy_views.strategyChart, name='strategyChart'),
    path('cross', cross_views.cross, name='cross'),
    path('crossChart', cross_views.crossChart, name='crossChart'),
]