from django.shortcuts import render
from django.http import HttpResponse
from .tasks import task_1, get_parsing_data


def index(request):

    task_1.delay()

    return HttpResponse("Hello world!")


def parser(request):

    get_parsing_data.delay()

    return HttpResponse("Parsing is already finished")
