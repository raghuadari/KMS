from django.shortcuts import render, redirect
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import Kudo, User, Release
from .forms import KudoForm

@login_required
def home(request):
    current_user = request.user
    kudos_granted = Kudo.objects.filter(from_user=current_user).count()
    kudos_received = Kudo.objects.filter(to_user=current_user).count()
    grantor_leaders = Kudo.objects.values('from_user').annotate(dcount=Count('from_user')).order_by('-dcount')
    for x in grantor_leaders:
        id = x['from_user']
        x['from_user'] = User.objects.get(pk=id)
    receiver_leaders = Kudo.objects.values('to_user').annotate(dcount=Count('to_user')).order_by('-dcount')
    for x in receiver_leaders:
        id = x['to_user']
        x['to_user'] = User.objects.get(pk=id)
    context = {'kudos_granted': kudos_granted, 'kudos_received': kudos_received,
               'grantor_leaders': grantor_leaders, 'receiver_leaders': receiver_leaders, 'user': current_user}
    return render(request, 'home.html', context)

@login_required
def add_model(request):

    if request.method == "POST":
        form = KudoForm(request.POST)
        if form.is_valid():

            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.from_user = request.user
            model_instance.release = Release.objects.filter(is_current_release=True).first()
            model_instance.date = datetime.now()
            model_instance.save()
            return redirect('home')
    else:
        form = KudoForm()
        form.Meta.fields

    return render(request, "kudos/grant.html", {'form': form})
