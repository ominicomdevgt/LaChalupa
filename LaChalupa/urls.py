"""LaChalupa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from users import views as user_views
from registration import views as reg_views
from game import views as game_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from users.forms import EmailValidationOnForgotPassword
from django.conf.urls import handler404, handler500
from django.views.static import serve 
from django.http import HttpResponse

urlpatterns = [
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: * \n Disallow: ", content_type="text/plain"), name="robots_file"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('ajax/load-cities/', reg_views.load_cities, name='ajax_load_cities'),
    path('snodadmiljo/', admin.site.urls),
    path('user-registro/', user_views.register,name='user_registro'),
    path('user-registro/a1', user_views.register, name='registroa1'),
    path('user-registro/b2', user_views.register, name='registrob2'),
    path('user-registro/c3', user_views.register, name='registroc3'),
    path('user-registro/d4', user_views.register, name='registrod4'),
    path('user-registro/e5', user_views.register, name='registroe5'),
    path('user-registro/f6', user_views.register, name='registrof6'),
    path('user-registro/g7', user_views.register, name='registrog7'),
    path('user-registro/h8', user_views.register, name='registroh8'),
    #path('registro/<int:pk>/', user_views.register_update_view, name='registro_change'),
    path('registro/', user_views.PersonCreateView.as_view(), name='registro'),
    path('registro/<int:pk>', user_views.ProfilCrView.as_view(), name='registro_nuevo'),
    path('<int:pk>/', user_views.PersonUpdateView.as_view(), name='registro_change'),
    path('oldgames/', user_views.old_games, name='oldgames'),
    path('oldgame/<int:pk>/', game_views.old_game, name='oldgame'),
    path('reward/<int:pk>/', reg_views.reward, name='reward-id'),
    re_path(r'^snd/(?P<pdsc>\d+)-([ a-zA-ZáéíóúÁÉÍÓÚÑñ\s0-9-/.%+&!"#$%&()*+,/=@-]+)-(?P<pid>\d+)-([ a-zA-ZáéíóúÁÉÍÓÚÑñ\s0-9-/.%+&!"#$%&()*+,/=@-]+)/$', game_views.reward_get, name='reward_get'),
    path('list-verficadores/<int:pk>', reg_views.list_verificate, name='verficar-list'),
    path('id-verficadores/<int:pk>', reg_views.id_verificate, name='verficar-id'),
    path('perfil/<int:pk>',login_required(user_views.ProfileUpdateView.as_view()), name='profile'),
    path('dashboard/', game_views.dashboard,name='dashboard'),
    path('perfil-admin/<int:pk>',reg_views.profile, name='profile-admin'),
    path('endgame/<int:endgame>', game_views.endgame,name='endgame'),
    path('sucursal/<int:pk>/', reg_views.sucursal, name='sucursal-id'),
    path('ganadores/', reg_views.ganadores, name='ganador'),
    path('premios-entregados/', reg_views.premios_entregados, name='premios-admin'),
    path('premios-entregados/<int:pk>', reg_views.premios_entregados_sucursal, name='premios-tienda'),
    path('ganadores/<int:pk><int:won>', reg_views.ganadores_sucursal, name='ganador-id'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('login/', user_views.login_request,name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword,  template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('registration.urls')),
    path("", reg_views.get_temc, name="index"),
    path("Inicio-Tombola", reg_views.inicio_tombola, name="inicio-tombola"),
    path("Tombola", reg_views.parar_tombola, name="parar-tombola"),
    path('usuarios_sel', reg_views.selected_jugadores, name='usuarios_sel'),
    path('incompletos/', reg_views.usuarios_incompletos, name='usuarios_incompletos'),
    path('MpS2HeKP-registros/', reg_views.resgistros_completos, name='usuarios_comp'),
    path('random_users/', reg_views.random_jugadores, name='usuarios_random'),
    path('nuevos_users/', reg_views.nuevos_jugadores, name='usuarios_nuevos'),
    path('codigo/', reg_views.codigo, name='codigo'),
    path('', include('registration.urls')),
    path('reward/<int:pk>/', reg_views.reward, name='reward-id'),
    path('oldgames/', user_views.old_games, name='oldgames'),
    path('oldgame/<int:pk>/', game_views.old_game, name='oldgame'),
]

handler404 = reg_views.handler404
handler500 = reg_views.handler500
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)