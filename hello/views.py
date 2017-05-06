from django.shortcuts import render

from django.http import JsonResponse

from .models import Greeting

import wikipedia as wk
import threading as th
import queue
import re, json
import scipy as sp

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def prueba(request):
	return render(request, 'prueba.html')

def apijson(request):
    """
    :param request: peticion http
    :return: json con datos
    """
    uid = request.GET['uid']
    busq = request.GET['busq']
    pattern = request.GET['pattern']
    targets = wk.search(busq)
    threads = []
    q1 = queue.Queue()
    def wrapper(target, que, pattern):
        try:
            page = wk.page(target)
            text = page.content
            reg = re.compile(pattern)
            que.put([len(reg.findall(text)), target, pattern])
        except wk.exceptions.DisambiguationError as e:
            que.put([-1, "ambiguous", "fail"])
    for target in targets:
        thread = th.Thread(target=wrapper, args=(target, q1, pattern))
        threads.append(thread)
        thread.start()
    amounts = []
    urls = []
    for thread in threads:
        thread.join()
        data = q1.get()
        amounts.append({
            'url': data[1],
            'amount': data[0]
        })
        urls.append(data[1])
    data = {
        "target": busq,
        "pattern": pattern,
        "reps": amounts
    }
    return JsonResponse(data)


def api(request):
    """
    Esta API esta ideada para devolver graficos, pero aun no esta implementada.
    :param request: peticion http
    :return: vista
    """
    uid = request.GET['uid']
    busq = request.GET['busq']
    pattern = request.GET['pattern']
    targets = wk.search(busq)
    threads = []
    q1 = queue.Queue()
    def wrapper(target, que, pattern):
        try:
            page = wk.page(target)
            text = page.content
            reg = re.compile(pattern)
            que.put([len(reg.findall(text)), target, pattern])
        except wk.exceptions.DisambiguationError as e:
            que.put([-1, "ambiguous", "fail"])
    for target in targets:
        thread = th.Thread(target=wrapper, args=(target, q1, pattern))
        threads.append(thread)
        thread.start()
    amounts = []
    urls = []
    for thread in threads:
        thread.join()
        data = q1.get()
        amounts.append({
            'url': data[1],
            'amount': data[0]
        })
        urls.append(data[1])
    data = {
        "target": busq,
        "pattern": pattern,
        "reps": amounts
    }
    return render(request, 'amounts.html', data)

