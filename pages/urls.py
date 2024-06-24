from django.urls import path
from . import views

urlpatterns = [
	path('', views.inicio.as_view(), name='inicio'),
	path('cumulo/<int:entry_id>/', views.cumulo.as_view(), name='cumulo'),
	path('cumuloedicion/<int:entry_id>/', views.cumuloedicion.as_view(), name='cumuloedicion'),
	path('especificacion/<int:entry_id>/<str:element_kind>/', views.especificacion.as_view(), name='especificacion'),
	path('especificacionedicion/<int:entry_id>/<str:element_kind>/<int:element_id>/', views.especificacionedicion.as_view(), name='especificacionedicion'),
	path('nuevocumulo/', views.nuevocumulo.as_view(), name='nuevocumulo'),
	path('busquedaresultados/<str:tag>/', views.busquedaresultados.as_view(), name='busquedaresultados'),
	path('cumuloeliminacion/<int:entry_id>/', views.cumuloeliminacion.as_view(), name='cumuloeliminacion'),
	path('especificacioneliminacion/<int:entry_id>/<str:element_kind>/<int:element_id>/', views.especificacioneliminacion.as_view(), name='especificacioneliminacion'),
]

