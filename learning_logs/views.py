from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def check_topic_owner(topic, request):
    if topic.owner != request.user:
        return Http404

def index(request):
    #домашняя страницца для приложения Learning log
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    #Выводит список тем
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    #Выводит одну тему и ее записи
    topic = Topic.objects.get(id=topic_id)

    #Проверка на пользователя
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        #данные не отправились, создается пустая форма
        form = TopicForm()
    else:
        #отправлены данные пост, обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    #вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    if request.method != 'POST':
        #данные не отправились, создается пустая форма
        form = EntryForm()
    else:
        #отправлены данные пост, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    #вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        #отправлены данные пост, обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    #вывести пустую или недействительную форму
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)