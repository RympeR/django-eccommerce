from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Proposition


class PropositionsView(ListView):
    model = Proposition
    paginate_by=20
    template_name="blog.html"

class PropositionsViewDetailView(DetailView):
    model = Proposition
    template_name = "blog-single.html"
