from django.urls import path, include
from .views import PropositionsView, PropositionsViewDetailView

app_name = 'proposition'


urlpatterns = [
    path('', PropositionsView.as_view(), name='all_prospositions'),
    path('single_proposition/<slug>', PropositionsViewDetailView.as_view(), name='single_proposition'),
]
