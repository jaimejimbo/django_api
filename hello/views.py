from django.shortcuts import render

from django.http import JsonResponse

from .models import Greeting

import wikipedia as wk
import threading as th
import queue
import re#, json
#import scipy as sp
import middleware.middleware as middle
#import numba


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

#@numba.jit(cache=True, nogil=True, nopython=True)
def workData(request):
    """
    
    :param request: 
    :return: 
    """
    uid = request.GET['uid']
    busq = request.GET['busq']
    pattern = request.GET['pattern']
    local = request.GET['contenido']
    results = request.GET['results']
    lang = request.GET['lang']
    wk.set_lang = lang
    targets = wk.search(busq, results=results)
    threads = []
    q1 = queue.Queue()

    def wrapper(target, que, pattern):
        try:
            page = wk.page(target)
            text = page.content
            url = page.url
            if (local == "true"):
                num = 0
                content = text
                que.put([num, target, pattern, url, content])
                return
            else:
                content = ""
                reg = re.compile(pattern, re.IGNORECASE)
                num = len(reg.findall(text))
                que.put([num, target, pattern, url, content])
                return
        except wk.exceptions.DisambiguationError as e:
            que.put([-1, "ambiguous", "fail", "", ""])

    for target in targets:
        thread = th.Thread(target=wrapper, args=(target, q1, pattern))
        threads.append(thread)
        thread.start()
    amounts = []
    for thread in threads:
        thread.join()
        data = q1.get()
        amounts.append({
            'title': data[1],
            'amount': data[0],
            'pattern': data[2],
            'url': data[3],
            'content': data[4]
        })
    data = {
        "target": busq,
        "pattern": pattern,
        "reps": amounts
    }
    return data

def api(request):
    """
    Esta API esta ideada para devolver graficos, pero aun no esta implementada.
    :param request: peticion http
    :return: vista
    """
    data = workData(request)
    middleware = middle.XsSharing()
    response = middleware.process_response(request, render(request, 'amounts.html', data))
    return response

def apijson(request):
    """
    :param request: peticion http
    :return: json con datos
    """
    data = workData(request)
    middleware = middle.XsSharing()
    response = middleware.process_response(request, JsonResponse(data))
    return response
