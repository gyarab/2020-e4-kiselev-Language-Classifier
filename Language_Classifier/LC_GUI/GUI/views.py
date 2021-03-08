from django.http import HttpResponse
from django.shortcuts import render
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import pickle
from urllib.parse import unquote


model = pickle.load(open("model.pkl", 'rb'))


def index(request):
    if (request.GET.get("text") != '' and (request.GET.get("text") != None)):
        languages = ['CZ', 'RU', 'FR', 'DE', 'EN', 'PL', 'IT', 'JA', "UK", "AR", "FI", "BG"]
        # print(str(request.GET.get("text")))
        input = [unquote(str(request.GET.get("text")))]
        output = languages[model.predict_proba(input).argmax(-1)[0]]
        # languages[model.predict_proba(a).argmax(-1)][0]
    else:
        output = 'input not found'
    return render(request, 'GUI/index.html', {'nbar': 'home', 'output': output})


def about(request):
    return render(request, 'GUI/index.html', {'nbar': 'about'})


def doc(request):
    return render(request, 'GUI/index.html', {'nbar': 'doc'})
