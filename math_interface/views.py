from django.shortcuts import render
from django.http import HttpResponse
import json

from math_interface.core import MathPlot


def index(request):
    return render(request, 'index.html')


def get_plot_image(request):
    post = json.loads(request.body)
    plot_params = post['plot']
    fn_params = post['fn']
    m = MathPlot(plot_params, fn_params)
    return HttpResponse(m.render(), content_type='image/jpeg')
