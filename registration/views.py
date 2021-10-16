from django.shortcuts import render, redirect
import datetime
from django.http import  HttpResponse
from django.conf import settings
from django.views.generic.base import TemplateView
from users.utils import validarCedula, validateAge
from users.models import Profile
from game.models import  Game, Reward, Stock, Conteo
from .models import City
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.db.models import Count, Subquery
from django.core.mail import send_mail
from django.template.loader import render_to_string
import numpy as np
import random
from users.forms import UserRegisterForm, ProfileFormAdmin, UserUpdateForm, ProfileForm_NoImg,PersonForm, LogingForm, Profileste
# Create your views here.
def home(request):
    context ={} 
    if request.user.is_authenticated:
        context['nombre'] = request.user.first_name
        if request.user.groups.filter(name='Administrador Tienda').exists():
            return redirect('home-tienda')
        elif request.user.groups.filter(name='Grupo Tienda').exists():
            return redirect('home-group')
        elif request.user.is_staff:
            return redirect('home-staff')
        elif request.user.groups.filter(name='Verificadores').exists():
            return redirect('home-verificador')
        else:
            return redirect('home-game')
    else:
        return render(request, 'registration/landing.html',context)    

def verificador(request):
    return render(request, 'registration/verficadores.html')

def Landing(request):
    context ={} 
    return render(request, 'registration/store.html',context)    

def Inicio_Juego(request):
    context ={}
    
    prof = Profile.objects.filter(user=request.user).first()
    field_object = prof._meta.get_field('verificate')
    field_value = field_object.value_from_object(prof)
    game_user = Game.objects.filter(user=request.user).count()
    game_won = Game.objects.filter(user=request.user,won =True).count()
    context['Comentario'] = prof
    context['acciones'] = game_user
    context['won'] = game_won
    old_games = Game.objects.values('reward_id').distinct().filter(user=request.user)
    old_rewards = []
    old_types = []
    
    if old_games is not None:
        for old in old_games:
            old_rewards.append(old['reward_id'])
        rewards = Reward.objects.filter(pk__in=old_rewards)
        for old in rewards:
            if old.type_reward == 'Camiseta':
                old_types.append(1)
            elif old.type_reward == 'Gorra':
                old_types.append(2)
            elif old.type_reward == '12 Pack Gratis':
                old_types.append(3)
            elif old.type_reward == 'Juego de Mesa Chalupa':
                old_types.append(4)
        numbers = list(range(1, 5))
        for x in old_types:
            numbers.remove(x)
        count = Conteo.objects.filter(contador__lte=0)
        if count is not None:
            for x in count:
                if int(x.pk) in numbers:
                    numbers.remove(x.pk)
        reward_type = 0
        if numbers != []:
            reward_type = random.choice(numbers)
        context['reward'] = reward_type
        request.session['reward_type'] = reward_type
    else:
        numbers = list(range(1, 5))
        count = Conteo.objects.filter(contador=0)
        if count is not None:
            for x in count:
                numbers.remove(x.pk)
        reward_type = 0
        if numbers != []:
            reward_type = random.choice(numbers)
        context['reward'] = reward_type
        request.session['reward_type'] = reward_type
    
    if field_value:
        context['validar'] = True
    else:
        context['validar'] = False
    request.session['home'] = True
    return render(request, 'registration/home.html',context)

def Admin_Staff(request):
    context ={}
    context['game_all'] = Game.objects.filter(won=True, delivered__in=[1,2]).count()
    context['game_por_entregar'] = Game.objects.filter(won=True,delivered__in=[1]).count()
    context['game_entregados'] = Game.objects.filter(won=True,delivered=2).count()
    context['stores'] = Game.objects.raw('''
    select  T.id, st.name, st.id sucursal, count(distinct T.id) todos, 
	(select sum( I.unit)  from game_stock I where I.reward_id <> 1 and I.store_id = T.store_id limit 1 ) Total,	
    (select count(id) from game_game I where delivered in (1) and store_id = T.store_id ) por_recorger,
    (select count(id) from game_game I where delivered = 2 and store_id = T.store_id ) recogidos
    from game_game T 
    inner join game_store st on st.id = T.store_id 
    group by T.store_id;

    ''')
    return render(request, 'registration/admin_page.html',context)


def Admin_tienda(request):
    context ={}
    prof = Profile.objects.filter(user=request.user).first()
    game_usr = Game.objects.filter(store=prof.store, delivered=1)
    context['games'] = game_usr
    context['user'] = prof
    return render(request, 'registration/store.html',context)

def Admin_Group(request):
    context ={}
    context['game_all'] = Game.objects.filter(won=True,store__group=request.user.profile.store.group).count()
    context['game_por_entregar'] = Game.objects.filter(won=True,delivered__in=[0,1],store__group=request.user.profile.store.group).count()
    context['game_entregados'] = Game.objects.filter(won=True,delivered=2,store__group=request.user.profile.store.group).count()
    context['stores'] = Game.objects.raw('''
    select  T.id, st.name, st.id sucursal, count(distinct T.id) todos, 
	(select sum( I.unit)  from game_stock I where I.reward_id <> 1 and I.store_id = T.store_id limit 1 ) Total,	
    (select count(id) from game_game I where delivered in (1) and store_id = T.store_id ) por_recorger,
    (select count(id) from game_game I where delivered = 2 and store_id = T.store_id ) recogidos
    from game_game T 
    inner join game_store st on st.id = T.store_id
    where st.group = %s 
    group by T.store_id;

    ''',[request.user.profile.store.group])

    return render(request, 'registration/admin_page.html',context)
class Home(TemplateView):
    isValid = validarCedula('0012605930022A')
    isBig = validateAge('0012605050022A')
    def get_template_names(self, request):
        if request.session['user-log'] is None:
            template_name = "index.html"
            request.session['user-log'] = True
            return template_name
        else:
            redirect(' ')

def get_temc(request):
    try:
        log = request.session['user_log']
        return redirect('home-page')
    except Exception as identifier:
        template_name = "index.html"
        request.session['user_log'] = True
        return render(request, "index.html")
    
def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'registration/city_dropdown.html', {'cities': cities})

@login_required
def reward(request,pk):
    context = {}
    if request.method == 'POST':
        game_re = Game.objects.filter(pk=pk).first()
        game_re.delivered = 2
        game_re.date_reward = datetime.datetime.now()
        type_reward = 0
        if game_re.reward.type_reward == 'Camiseta':
            type_reward = 1
        elif game_re.reward.type_reward == 'Gorra':
            type_reward = 2
        elif game_re.reward.type_reward == '12 Pack Gratis':
            type_reward = 3
        elif game_re.reward.type_reward == 'Juego de Mesa Chalupa':
            type_reward = 4
        count_obj = Conteo.objects.filter(pk=type_reward).first()
        count_obj.contador = count_obj.contador - 1
        count_obj.save()
        
        game_re.save()
        messages.success(request,f'El premio fue entregado')
        return redirect('/inicio') 
    else:
        game_re = Game.objects.filter(pk=pk).first()
        context["Game"] = game_re
        return render(request, "registration/reward.html", context) 

@login_required
def sucursal(request,pk):
    context = {}
    context['sucursal'] = pk  
    context['nombre'] = request.user.first_name
    context['game_all'] = Game.objects.filter(store=pk).count()
    context['game_por_entregar'] = Game.objects.filter(store=pk,delivered__in=[0,1]).count()
    context['game_entregados'] = Game.objects.filter(store=pk,delivered=2).count()
    context['rewards'] =  Game.objects.raw('''
            select T.id, st.type_reward, st.gender, st.size, st.id sucursal, count(T.id) todos,
			(select unit from game_stock I where  T.store_id = %s and reward_id = T.reward_id limit 1) Total,
            (select count(id) from game_game I where delivered in (1) and I.store_id = %s and reward_id = T.reward_id ) por_recorger,
            (select count(id) from game_game I where delivered = 2 and I.store_id = %s and reward_id = T.reward_id ) recogidos
            from game_game T 
            inner join game_reward st on st.id = T.reward_id
            where T.store_id = %s
            group by T.reward_id;
            ''', [pk,pk,pk,pk])
    
    return render(request, "registration/store_reward.html", context) 


@login_required
def ganadores(request):
    context = {}
    if request.user.groups.filter(name='Grupo Tienda').exists():
        context['ganadores'] = Game.objects.filter(won=True,store__group=request.user.profile.store.group,delivered__gte=1).order_by('-date')
    else:
               
        context['ganadores'] = Game.objects.filter(won=True,delivered__gte=1).order_by('-date')
    return render(request, "registration/ganadores.html", context)

 

@login_required
def ganadores_sucursal(request,pk,won):
    context = {}    
    context['ganadores'] = Game.objects.filter(won=True,delivered=won,store_id=pk).order_by('date')
    return render(request, "registration/ganadores.html", context) 

def Landing(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'registration/city_dropdown.html', {'cities': cities})


def preguntas(request):
    
    return render(request, 'registration/preguntas.html')


def reglamento(request):
    return render(request, 'registration/reglamento.html')


def blank(request):
    return render(request, 'registration/blank.html')

def handler404(request, exception):
    return render(request, 'registration/blank.html')

def handler500(request):
    return render(request, 'registration/500.html')
@login_required
def list_verificate(request,pk):
    context = {}
    estado = True if pk == 1 else False 
    context['usuarios'] = Profile.objects.filter(verificate=estado, DNI__isnull=False)
    context['verficado'] = 'Verficados' if pk else 'No Verficados'
    return render(request, 'registration/listado_verificadores.html',context)
    

@login_required
def id_verificate(request,pk):
    context = {}
    if request.method == 'POST':
        verificado = request.POST.get('verficado')
        if verificado:
            prof = Profile.objects.filter(pk=pk).first()
            prof.verificate = True
            prof.save()
            msg_html = render_to_string('users/email_verificado.html')
            send_mail(
                        'Tu Usuario ha sido Verificado',
                        'Ingresa a este link para indicarnos donde deseas recoger tu premio.',
                        from_email='no-reply@chalupatona.com',
                        recipient_list=[prof.user.username],
                        html_message=msg_html,
                    )
        else:
            
            prof = Profile.objects.filter(pk=pk).first()
            prof.verificate = False
            prof.comment = request.POST.get('comentario')
            prof.save()
            msg_html = render_to_string('users/email_noverificado.html',{'comentario':prof.comment,'perfil':prof.pk})
            send_mail(
                        'Tu Usuario no ha podido ser verificado',
                        'Ingresa a este link para indicarnos donde deseas recoger tu premio.',
                        from_email='no-reply@chalupatona.com',
                        recipient_list=[prof.user.username],
                        html_message=msg_html,
                    )
        messages.success(request,f'El usuario fue modificado exitosamente!!')
        return redirect('verficar-list',pk=0) 
    context['usuario'] = Profile.objects.filter(pk=pk).first()
    return render(request, 'registration/id_verficador.html',context)

@login_required
def premios_entregados(request):
    context = {}
    if request.user.groups.filter(name='Grupo Tienda').exists():
        context['camisetas'] = Game.objects.filter(delivered=2, reward__type_reward='Camiseta',store__group=request.user.profile.store.group).count()
        context['gorras'] = Game.objects.filter(delivered=2, reward__type_reward='Gorra',store__group=request.user.profile.store.group).count()
        context['chalupa'] = Game.objects.filter(delivered=2, reward__type_reward='Juego de Mesa Chalupa',store__group=request.user.profile.store.group).count()
        context['liquido'] = Game.objects.filter(delivered=2, reward__type_reward='12 Pack Gratis',store__group=request.user.profile.store.group).count()    
        context['stores'] = Game.objects.filter(won=True,delivered=2,store__group=request.user.profile.store.group).order_by('-date_reward')
    else:
        context['camisetas'] = Game.objects.filter(delivered=2, reward__type_reward='Camiseta').count()
        context['gorras'] = Game.objects.filter(delivered=2, reward__type_reward='Gorra').count()
        context['chalupa'] = Game.objects.filter(delivered=2, reward__type_reward='Juego de Mesa Chalupa').count()
        context['liquido'] = Game.objects.filter(delivered=2, reward__type_reward='12 Pack Gratis').count()    
        context['stores'] = Game.objects.filter(won=True,delivered=2).order_by('-date_reward')
    return render(request, "registration/premios_entregados.html", context)


@login_required
def premios_entregados_sucursal(request,pk):
    context = {}
    context['camisetas'] = Game.objects.filter(delivered=2, reward__type_reward='Camiseta', store=pk).count()
    context['gorras'] = Game.objects.filter(delivered=2, reward__type_reward='Gorra',store__pk=pk).count()
    context['chalupa'] = Game.objects.filter(delivered=2, reward__type_reward='Juego de Mesa Chalupa',store__pk=pk).count()
    context['liquido'] = Game.objects.filter(delivered=2, reward__type_reward='12 Pack Gratis',store__pk=pk).count()    
    context['stores'] = Game.objects.filter(won=True,delivered=2,store__pk=pk).order_by('-date_reward')
    return render(request, "registration/premios_entregados.html", context)


@login_required
def usuarios_incompletos(request):
    context = {}
    context['usuarios'] = Profile.objects.filter(DNI__isnull=False, store__isnull=True).order_by('-pk')[:200]
    return render(request, "registration/usuarios_incompletos.html",context)

@login_required
def profile(request,pk):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=pk)
        perfil = Profile.objects.filter(user__pk=pk).first()
        p_form = ProfileFormAdmin(request.POST, request.FILES, instance=perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Tu cuenta se a actualizado')
            return redirect('profile')    
    else:
        
        prof = Profile.objects.filter(user_id=pk).first()
        field_object = prof._meta.get_field('verificate')
        field_value = field_object.value_from_object(prof)
        if field_value:
            p_form = ProfileFormAdmin(instance=prof)
        else:
            p_form = ProfileFormAdmin(instance=prof)
        u_form = UserUpdateForm(instance=prof.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'perfil': prof
    }
    return render(request, 'registration/profile-admin.html', context)



def resgistros_completos(request):
    context = {}
    context['usuarios'] = Game.objects.raw('''
    select USUARIOS.id, USUARIOS.first_name NOMBRE, PERFIL.DNI CEDULA, CONCAT('https://chalupatona.com/media/',PERFIL.image) FOTOGRAFIA,
    CIUDAD.name MUNICIPIO, DEPART.name DEPARTAMENTO, USUARIOS.date_joined FECHA_REGISTRO,
    YEAR(CURRENT_TIMESTAMP) - YEAR(PERFIL.birthday)
	- (RIGHT(CURRENT_TIMESTAMP, 5) < RIGHT(PERFIL.birthday, 5)) Edad, PERFIL.telephone Telefono,
    (select count(JI.id) from game_game JI where JI.user_id = JUEGO.user_id ) 'Partidas_Totales',
    (select count(JI.id) from game_game JI where JI.user_id = JUEGO.user_id and JI.won=1 and JI.reward_id > 0 ) 'Premios_Ganados',
    (select count(JI.id) from game_game JI where JI.user_id = JUEGO.user_id and JI.won=1 IS NOT NULL and JI.delivered=2 ) 'Premios_Redimidos',
    (select count(JI.id) from game_game JI where JI.user_id = JUEGO.user_id and JI.won =1 and isnull(JI.reward_id)) 'Acciones_Ganadas' 
    from game_game JUEGO
    inner join auth_user USUARIOS on JUEGO.user_id = USUARIOS.id
    inner join users_profile PERFIL on PERFIL.user_id= USUARIOS.id
    INNER JOIN registration_city CIUDAD ON CIUDAD.id  = PERFIL.city_id
    INNER JOIN registration_country DEPART ON DEPART.id = PERFIL.country_id
    where PERFIL.verificate = 1
    group by JUEGO.user_id
    order by Partidas_Totales desc
    limit 1906
    ;
    ''')
    return render(request, "registration/registros_completos.html",context)

def random_jugadores(request):
    context = {}
    randdash = np.random.choice(range(152,4627), 40, replace=False)
    perfil = Profile.objects.filter(pk__in=randdash, verificate=True)[:10]
    context['usuarios'] = perfil
    return render(request, 'registration/random_user.html',context)

def selected_jugadores(request):
    context = {}
    usuario_array = [1469,1490,1490,1509,1541,1536,1552,1573,1586,1594,1605,1616,1627,1634,1639,1640,1643,1653,1646,1689,1691,1695,1703,1709,1807,1830,1837
    ,1836,1838,1843,1857,1871,1917,1921,1941,1942,1943,1949,1975,1989,1988,2000,2016,2023,2024,2039,2055,2064,2065,2076,2078,2081,2083,2095,2106,2113,2121,2128,2131,2132,2195,2194,2197,2206,2222,2226,2229,2234
    ,2237,2238,2265,2303,2308,2325,2336,2359,2360,2383,2419,2420,2425,2456,2474,2500,2508,2517,2521,2554,2689,2700,2777,2815,2849,2881,2915,2912,2926,2944,2949,2952,3035,3045,3047,3046,3051,3144,3221,3220,3238,3250,3264,3454,3499,
    4975,4978,4979,4983,5010,5033,5066,5096,5132,5186]
    randdash = np.random.choice(usuario_array, 13, replace=False)
    perfil = Profile.objects.filter(user_id__in=randdash, verificate=True)[:10]
    context['usuarios'] = perfil
    return render(request, 'registration/selected_users.html',context)

def inicio_tombola(request):
    return render(request, "inicio_tombola.html")

def parar_tombola(request):
    return render(request, "parar_tombola.html")

def nuevos_jugadores(request):
    context = {}
    perfil = Profile.objects.filter(user__date_joined__gte='2021-02-06', verificate=True)
    context['usuarios'] = perfil
    return render(request, 'registration/random_user.html',context)

def codigo(request):
    return render(request, "registration/codigo_random.html")