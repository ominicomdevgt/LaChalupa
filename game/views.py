from django.shortcuts import render, redirect
from .models import Card, Game, Reward, Store, Conteo,Stock
from users.models import  Profile
from django.contrib.auth.decorators import login_required
import datetime
import numpy as np
from django.core.mail import send_mail
from django.http import JsonResponse
import random, string, json
from django.contrib import  messages
from django.template.loader import render_to_string
# Create your views here.
@login_required
def dashboard(request): 
    # dictionary for initial data with  
    # field names as keys
    if request.session.get('home'):
        context ={}
        request.session['home'] = False
        if request.session.get('reward_type') > 0:
            valor_cont = Conteo.objects.filter(pk=request.session.get('reward_type')).first()
            if valor_cont.contador <= 0:
                context["tipo_reward"] = 0
            else:
                context["tipo_reward"] = request.session.get('reward_type')
        else:
            context["tipo_reward"] = 0
        prof = Profile.objects.filter(user=request.user).first()
        field_object = prof._meta.get_field('count')
        field_value = field_object.value_from_object(prof)
        if True:

            if  int(field_value) > 0:
                prof.count = prof.count - 1
                prof.save()
                
                randdash = np.random.choice(range(1,17), 9, replace=False)
                randdash = np.random.choice(randdash, 9, replace=False)
                randcards = np.random.choice(range(1,17), 14, replace=False)
                randcards = np.random.choice(randcards, 14, replace=False)
                orderdash = np.sort(randdash)
                ordercards = np.sort(randcards)
                result = False
                if np.in1d(orderdash,ordercards).all():
                #if True:
                    context["won"] = True
                    request.session['won'] = True
                    reward_type = context["tipo_reward"]
                    if reward_type == 0:
                        request.session['tipo_reward'] = 0
                        request.session['reward'] = None
                        pin = random.randint(999, 9999)
                        game_target = Game(user=request.user,date=datetime.datetime.now(),won=True,
                                            reward=None,cards=randdash, sing=randcards,PID=pin)
                        game_target.save()
                    else:
                        
                        count = Conteo.objects.filter(pk=reward_type).first()
                        count.contador = count.contador - 1
                        count.save()
                        if reward_type == 1:
                            reward_type = 'Camiseta'
                        elif reward_type == 2:
                            reward_type = 'Gorra'
                        elif reward_type == 3:
                            reward_type = '12 Pack Gratis'
                        elif reward_type == 4:
                            reward_type = 'Juego de Mesa Chalupa'
                        reward = Reward.objects.filter( type_reward = reward_type).first()
                        request.session['reward'] = reward.pk
                        pin = random.randint(999, 9999)
                        game_target = Game(user=request.user,date=datetime.datetime.now(),won=True,
                                            reward=reward,cards=randdash, sing=randcards,PID=pin)
                        game_target.save()
                        
                
                else:
                    
                    pin = random.randint(999, 9999)
                    context["won"] = False
                    request.session['won'] = False
                    game_target = Game(user=request.user,date=datetime.datetime.now(),won=False,
                                        reward=None,cards=randdash,sing=randcards,PID=pin)
                    game_target.save()
                dataset=[]
                cards=[]
                for data in randdash:
                    dataset.append(Card.objects.filter(pk=data).first())
                for data in randcards:
                    cards.append(Card.objects.filter(pk=data).first())
                context["dataset"] = dataset
                context["cards"] = cards
                dataset_json = []
                cards_json = []
                for x in dataset:
                    obj ={
                        'image': x.image.url,
                        'description': x.description,
                        'IDTag': str(x.pk) + 'Card'
                    }
                    dataset_json.append(obj)
                for data in cards:
                    on_game = 1  if data.pk in randdash else 0
                    obj ={
                        'image': data.image.url,
                        'description': data.description,
                        'sound' : data.sound,
                        'On_dash': on_game,
                        'id': str(data.id) + 'Card'
                    }
                    cards_json.append(obj)
                context['dash_json'] = json.dumps(dataset_json)
                context['cards_json'] = json.dumps(cards_json)    
                context['is_won_json'] = json.dumps({ 'won': context['won'] })
                request.session['pk'] = game_target.pk
                return render(request, "game/dashboard.html", context) 
            else:
                return render(request, "game/intentos.html")
        else:
            messages.warning(request,f'Tu Perfil no esta verificado.')
            return redirect(' ')
    else:
        return redirect(' ') 
    

@login_required
def endgame(request,endgame):
    if endgame == 1:
        context = {}
        context['won'] = request.session.get('won')
        game_re =  Game.objects.filter(pk=request.session.get('pk')).first()
        context['game'] = game_re
        context['reward'] = Reward.objects.filter(pk=request.session.get('reward')).first()
        if Store.objects.filter(city=request.user.profile.city).exists():
            stores = Store.objects.filter(city=request.user.profile.city)
        else:
            stores = Store.objects.all()
        
        context["Stores"] = stores
        store_json = []
        for x in stores:
            obj ={
                'id': x.pk,
                'nombre': x.name,
                'latitud': x.lat,
                'longitud': x.longitude
            }
            store_json.append(obj)
        context['store_json'] = json.dumps(store_json)
        request.session['game'] = game_re.pk
        if request.method == 'POST':
            #rewar_id=Reward.objects.filter(pk=request.POST.get('city'))
            game_re = Game.objects.filter(pk=request.session.get('game')).first()
            if game_re.reward.type_reward == 'Camiseta':
                new_reward = Reward.objects.filter(type_reward=game_re.reward.type_reward, size=request.POST.get('talla'),
                gender=request.POST.get('genero')).first()
            elif game_re.reward.type_reward == 'Gorra':
                new_reward = Reward.objects.filter(type_reward=game_re.reward.type_reward, gender=request.POST.get('genero')).first()
            else:
                new_reward = Reward.objects.filter(pk=game_re.reward.pk).first()
            game_re.store = Store.objects.filter(pk=request.POST.get('store')).first()  
            game_re.reward = new_reward
            game_re.delivered = 1
            game_re.save()
            stock = Stock.objects.filter(reward=game_re.reward,store=game_re.store).first()
            stock.unit = stock.unit - 1
            stock.save()
            context['Validate'] = True
            messages.success(request,f'Puedes continuar jugando...')
            msg_html = render_to_string('game/email.html',{'game': game_re })
            send_mail(
                        '¡Felicidades! Ganaste la Chalupa Toña.',
                        'Ingresa a este link para indicarnos donde deseas recoger tu premio.',
                        from_email='no-reply@chalupatona.com',
                        recipient_list=[request.user.username],
                        html_message=msg_html,
                    )
            return redirect(' ')
    else:
        game_re =  Game.objects.filter(pk=request.session.get('pk')).delete()
        return redirect(' ')
    return render(request, "game/endgame.html", context) 

@login_required
def old_game(request,pk):
    context = {}
    if request.method == 'POST':
        game_re = Game.objects.filter(pk=pk).first()
        if game_re.delivered > 0:
            msg_html = render_to_string('game/email.html',{'game': game_re })
            send_mail(
                        '¡Felicidades! Ganaste la Chalupa Toña.',
                        'Ingresa a este link para indicarnos donde deseas recoger tu premio.',
                        from_email='no-reply@chalupatona.com',
                        recipient_list=[request.user.username],
                        html_message=msg_html,
                    )
            messages.success(request,f'Se te a reenviado un correo.')
        else:
            messages.success(request,f'El premio seleccionado son acciones...')
        
        return redirect('oldgames')
    endgame = request.session.get('endgame')
    game_re = Game.objects.filter(pk=pk).first()
    game_re.date = game_re.date - datetime.timedelta(hours=7)
    cards = game_re.cards[1:-1].split()
    sing = game_re.sing[1:-1].split()
    dashcards = np.array(cards,dtype=int)
    dashsing = np.array(sing,dtype=int)
    context['game'] = game_re
    context["dataset"] = Card.objects.filter(pk__in=dashcards)
    context["cards"] = Card.objects.filter(pk__in=dashsing)
    return render(request, "game/oldgame.html", context) 


@login_required
def reward_get(request,pdsc,pid):
    context = {}
    if request.user.profile.country is None:
        return render(request, "game/faltan_datos.html", context)
    else:
        game_re = Game.objects.filter(pk=pdsc, PID=pid).first()
        if game_re.delivered == 0:
            if request.method == 'POST':
                #rewar_id=Reward.objects.filter(pk=request.POST.get('city'))
                game_re = Game.objects.filter(pk=pdsc, PID=pid).first()
                if game_re.reward.type_reward == 'Camiseta':
                    new_reward = Reward.objects.filter(type_reward=game_re.reward.type_reward, size=request.POST.get('talla'),
                    gender=request.POST.get('genero')).first()
                elif game_re.reward.type_reward == 'Gorra':
                    new_reward = Reward.objects.filter(type_reward=game_re.reward.type_reward, gender=request.POST.get('genero')).first()
                else:
                    new_reward = Reward.objects.filter(pk=game_re.reward.pk).first()
                game_re.store = Store.objects.filter(pk=request.POST.get('store')).first()  
                game_re.reward.pk = new_reward.pk
                game_re.delivered = 1
                game_re.save()
                context['Validate'] = True
                return render(request, "game/get_reward.html", context)
            else:
                game_re = Game.objects.filter(pk=pdsc, PID=pid).first()    
                context["Game"] = game_re
                context["Stores"] = Store.objects.filter(city=game_re.user.profile.city)
                context['Validate'] = False
                return render(request, "game/get_reward.html", context)
        else:
            return redirect(' ')

