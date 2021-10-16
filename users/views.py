from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import  messages
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm, ProfileForm_NoImg,PersonForm, LogingForm, Profileste
from django.contrib.auth.decorators import login_required
from .models import Profile
from game.models import Game
from .utils import validarCedula ,validateAge
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import datetime
# Create your views here.
#@transaction.atomic
def register(request):
    try:
        print(request.session['user_log'])
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            profile_form = ProfileForm(request.POST)
            if form.is_valid():
                form.save()
                user = Profile.objects.last()
                return redirect('registro_nuevo', pk=user.pk)
    
        else:
            form = UserRegisterForm()
        return render(request,'users/register.html',{'form':form})
    except Exception as identifier:
        request.session['url'] = 'a1'
        return redirect('index')
    


def register_update_view(request, pk):
    person = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(instance=person)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=person)
        if form.is_valid():
            form.save()
            return redirect('registro_change', pk=pk)
    return render(request, 'home-page', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Tu cuenta se a actualizado')
            return redirect('profile')    
    else:
        prof = Profile.objects.filter(user=request.user).first()
        field_object = prof._meta.get_field('verificate')
        field_value = field_object.value_from_object(prof)
        if field_value:
            p_form = ProfileForm_NoImg(instance=request.user.profile)
        else:
            p_form = ProfileForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

    

@login_required
def old_games(request):
    game_user = Game.objects.filter(user=request.user).order_by('-pk')
    game_all = []
    for game_o in game_user:
        game_o.date = game_o.date - datetime.timedelta(hours=6)
        game_all.append(game_o)
    page = request.GET.get('page', 1)
    paginator = Paginator(game_all, 10)
    try:
        game_all = paginator.page(page)
    except PageNotAnInteger:
        game_all = paginator.page(1)
    except EmptyPage:
        game_all = paginator.page(paginator.num_pages)
    context = {'games':game_all}
    return render(request, 'users/old_games.html', context)

#Codigo de select
class PersonCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    second_form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'users/profile_form.html'
    def post(self,request):
        
        form_class = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
        if form_class.is_valid() :
            dni = form_class.cleaned_data.get('DNI')
            if validarCedula(dni) and validateAge(dni):
                dni_dd = dni[3:5]
                dni_mm = dni[5:7]
                dni_yy = dni[7:9]
                fehca_din = '19' + dni_yy + '-' + dni_mm + '-' + dni_dd
                fecha = form_class.cleaned_data.get('birthday')
                print(fecha)
                #if fecha == fehca_din:
                if True:
                    print('llego al form')
                    form_class.save()
                    messages.success(request,f'Cuenta Actualizada ')
                    return redirect('login')
                else:
                    profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
                    messages.error(request,f'tu fecha de nacimiento no coincide con tu cédula')
                    return render(request, 'users/profile_form.html',{'form':profile_form})
            else:
                #raise ValidationError('El DNI no es valido')
                profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
                messages.error(request,f'La Cedula no es válida')
                return render(request, 'users/profile_form.html',{'form':profile_form})
        return render(request, 'users/profile_form.html',{'form':form_class})
class PersonUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('home')



def login_request(request):
    context = {}
    
    if request.method == 'POST':
        
        form = LogingForm(request.POST)
        context= {'form': form, 'error':'El nombre de usuario ya fue tomado'}
        
        if True:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                
                login(request, user)
                #messages.info(request, f"Te has logeado como  {username}")
                return redirect('home-page')
            else:
                context["message"] = "Usuario o contraseña inválida."
        else:
            context["message"] = "Usuario o contraseña inválida."
    form = LogingForm()
    context['form'] = form
    return render(request = request,
                    template_name = "users/login.html",
                    context = context)

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    second_form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'users/profile.html'
    
    def post(self,request,pk):

        form_class = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form_class.is_valid() :
            dni = form_class.cleaned_data.get('DNI')
            if validarCedula(dni) and validateAge(dni):
            #if True:
                form_class.save()
                
                username = form_class.cleaned_data.get('username')
                messages.success(request,f'Cuenta Actualizada {request.user.first_name}')
                return redirect('home-page')
            else:
                #raise ValidationError('El DNI no es valido')
                profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
                messages.error(request,f'La Cedula no es válida')
                return render(request, 'users/profile.html',{'form':profile_form})
        return render(request, 'users/profile.html',{'form':form_class})


class ProfilCrView(CreateView):
    model = Profile
    form_class = ProfileForm
    second_form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'users/profile_form.html'
    def post(self,request,pk):

        form_class = ProfileForm(request.POST, request.FILES, instance=Profile.objects.filter(pk=pk).first())
        if form_class.is_valid() :
            dni = form_class.cleaned_data.get('DNI')
            if validarCedula(dni) and validateAge(dni):
                dni_dd = dni[3:5]
                dni_mm = dni[5:7]
                dni_yy = dni[7:9]
                fehca_din = '19' + dni_yy + '-' + dni_mm + '-' + dni_dd
                fecha = form_class.cleaned_data.get('birthday')
                print(fecha)
                print(fehca_din)
                #if str(fecha) == str(fehca_din):
                if True:
                    form_class.save()
                    prof = Profile.objects.last()
                    username = User.objects.filter(pk=prof.user.pk)
                    messages.success(request,f'Cuenta creada {prof} te hemos enviado un correo electronico para confirmar tu registro')
                    msg_html = render_to_string('users/email.html')
                    send_mail(
                                'Bienvenido a la Chalupa Toña.',
                                'Ya estás registrado, prepárate para jugar y ganar muchos premios.',
                                from_email='no-reply@chalupatona.com',
                                recipient_list=[prof],
                                html_message=msg_html,
                                fail_silently=False,
                            )
                    
                    
                    return redirect('login')
                else:
                    profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
                    messages.error(request,f'tu fecha de nacimiento no coincide con tu cédula')
                    return render(request, 'users/profile_form.html',{'form':profile_form})
            else:
                #raise ValidationError('El DNI no es valido')
                profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.last())
                messages.error(request,f'La Cédula no es válida')
                return render(request, 'users/profile_form.html',{'form':profile_form})
        return render(request, 'users/profile_form.html',{'form':form_class})