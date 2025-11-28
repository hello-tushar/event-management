from django.shortcuts import render, redirect
from django.http import HttpResponse
from event.forms import *
from event.models import *
from django.db.models import Count
from datetime import date
from django.db.models import Q

def home(request):
    base_query = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants')).all()
    search = request.GET.get("search", "")
    if search:
        base_query = base_query.filter(Q(name__icontains=search) | Q(location__icontains=search))
    context = {
        'base_query': base_query
    }
    return render(request, 'user.html', context)

def eventDetail(request, id):
    query = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    context = {'query': query}

    return render(request, 'eventDetail.html', context)
def test(request):
    return render(request, 'test.html')
def create_event(request):
    event_form = EventModelForm() # For GET

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect('home/')


    context = {'event_form': event_form}
    return render(request, 'event_form.html', context)

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance = event) # for GET
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance = event)

        if event_form.is_valid():
            event_form.save()
            return redirect('home/')
    context = {'event_form': event_form}
    return render(request, 'event_form.html', context)

def delete_event(request, id):
    
    event = Event.objects.get(id=id)
    if request.method == "GET":
        event.delete()
        return redirect('home/')

def organizerDashboard(request):

    base_query = Event.objects.select_related('category').prefetch_related('participants')
    type = request.GET.get('type', 'all')
    total_participants = Participant.objects.filter(events__isnull=False).distinct().count()

    eventType = 'All Event'
    if type == 'upcoming-event':
        events = base_query.filter(date__gt=date.today()).annotate(cnt=Count('participants'))
        eventType = 'Upcoming Events'
    elif type == 'past-event':
        events = base_query.filter(date__lt=date.today()).annotate(cnt=Count('participants'))
        eventType = 'Past Events'
    else:
        events = base_query.all().annotate(cnt=Count('participants'))
    
    eventToday = base_query.filter(date=date.today()).annotate(cnt=Count('participants'))

    allEventCount = base_query.count()
    upcomingEventCount = base_query.filter(Q(date__gt=date.today()) | Q(date=date.today())).count()
    pastEventCount = base_query.filter(date__lt=date.today()).count()

    

    context = {
        'total_participants': total_participants,
        'events': events,
        'allEventCount': allEventCount,
        'upcomingEventCount': upcomingEventCount,
        'pastEventCount': pastEventCount,
        'eventType': eventType,
        'eventToday': eventToday,
    }
    return render(request, 'organizerDashboard.html', context)


def addParticipant(request):
    participant_form = ParticipantModelForm() # For GET

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            return redirect('home/create-event/')


    context = {'participant_form': participant_form}
    return render(request, 'addParticipant.html', context)

def addCategory(request):
    category_form = CategoryModelForm() # For GET

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('home/create-event/')


    context = {'category_form': category_form}
    return render(request, 'addCategory.html', context)