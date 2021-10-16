from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('inicio', views.home,name='home-page'),
    path('landing', views.Landing,name='landing'),
    path('preguntas', views.preguntas,name='preguntas'),
    path('reglamento', views.reglamento,name='reglamento'),
    path('inicio-juego', user_views.old_games,name='home-game'),
    path('inicio-staff', views.Admin_Staff,name='home-staff'),
    path('inicio-group', views.Admin_Group,name='home-group'),
    path('inicio-tienda', views.Admin_tienda,name='home-tienda'),
    path('inicio-verificador', views.verificador,name='home-verificador'),
]