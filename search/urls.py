from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search-index'),
    path('search/gene/<str:gene_id>/', views.gene_detail, name='gene_detail'),
    path('search/transcript/<str:tr_id>/', views.tr_detail, name='tr_detail'),
    path('search/gene/exp/<str:gene_id>',
         views.single_gene_exp_view,
         name='single_gene_exp_view'),
    path('search/<str:db>/', views.result_view, name='search-results'),
    path('search/neighbor/<str:query_id>',
         views.search_neighbor,
         name='search_neighbor')
]
