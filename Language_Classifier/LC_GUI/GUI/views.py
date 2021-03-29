from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import pickle
from urllib.parse import unquote
from .classify import *
import html
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


model = pickle.load(open("model.pkl", 'rb'))


def index(request):

    languages = ['Czech', 'Russian', 'French', 'German', 'English', 'Polish', 'Italian', "Ukrainian", "Finnish", "Bulgarian", "Spanish", "Portuguese"]
    languages_colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99",
                        "#b15928"
    ]
    new_output = [4]
    new_input = ['Please input several sentences of text longer than 5 words. Then click "Detect Language" button in the bottom right corner.']

    numbers = []
    new_colors = []
    for i in range(0, len(new_output)):
        numbers.append(i)
        new_colors.append([languages_colors[new_output[i]],languages_colors[new_output[i]]])
    input_dic = dict(zip(new_input, new_colors))
    color_meaning = []
    color_meaning.append(new_colors[0][0])

    if (request.GET.get("text") != '' and (request.GET.get("text") != None)):

        input = [unquote(str(request.GET.get("text")))]
        input[0] = html.unescape(input[0])
        input[0] = re.sub("[\<].*?[\>]", "", input[0])
        test = input[0].translate({ord(c): " " for c in
                                       ",|\$|\{|\}|\-|\+|\[|\]|\<|\>|\"|\=|\:|\;|\*|\||\#|\$|\(|\)|\/|\.|\–|\_|\«|\»|\—|\!|\&|\?|\`|\~|\%|\@|\¡|\™|\£|\¢|\∞|\§|\¶|\•|\ª|\º|\–|\≠|\«|\æ|\÷|\≥|\≤|\÷|\»|\\|\^|\ˆ|\|\\|\||\）|\（|\、|\""})
        test = ''.join([i for i in test if not i.isdigit()])
        test = test.lower()
        test = re.sub('\n+', ' ', test)
        test = re.sub('\r+', ' ', test)
        test = re.sub(' +', ' ', test)

        if (len(test)>0 and test != '' and test != ' ' and test != None and test != '\n' and test != '\r\n' and len(test.split(" "))>4):
            new_output, new_input = classify(model, input, languages)
            numbers = []
            new_colors = []
            temp_input = []
            temp_output = []

            for i in range(0, len(new_input)):
                if len(new_input[i].split(" ")) > 4:
                    temp_input.append(' '.join(word for word in new_input[i].split(' ')[:2]))
                    temp_input.append(' '.join(word for word in new_input[i].split(' ')[2:-2]))
                    temp_input.append(' '.join(word for word in new_input[i].split(' ')[-2:]))
                    for j in range(0, 3):
                        temp_output.append(new_output[i])
                else:
                    temp_input.append(new_input[i])
                    temp_input.append('')
                    temp_input.append('')
                    for j in range(0, 3):
                        temp_output.append(new_output[i])
            new_output = temp_output
            new_input = temp_input
            temp_input = []
            temp_output = []

            temp_input.append(new_input[0])
            temp_output.append(new_output[0])
            temp_input.append(new_input[1])
            temp_output.append(new_output[1])

            for i in range(2, len(new_input), 3):

                if i+1 != len(new_input):
                    temp_input.append(new_input[i] + " " + new_input[i+1])
                    temp_output.append(new_output[i])
                    temp_input.append(new_input[i+2])
                    temp_output.append(new_output[i+2])
                else:
                    temp_input.append(new_input[i])
                    temp_output.append(new_output[i])

            new_output = temp_output
            new_input = temp_input
            new_colors = []

            temp_input = []
            temp_output = []
            for i in range(0, len(new_input)):
                if new_input[i] != "":
                    temp_input.append(new_input[i])
                    temp_output.append(new_output[i])
            new_output = temp_output
            new_input = temp_input

            color_meaning = []
            for i in range(0, len(new_output)):
                if i+1 < len(new_output):
                    new_colors.append([languages_colors[new_output[i]], languages_colors[new_output[i+1]]])
                    if languages_colors[new_output[i]] not in color_meaning:
                        color_meaning.append(languages_colors[new_output[i]])
                    if languages_colors[new_output[i+1]] not in color_meaning:
                        color_meaning.append(languages_colors[new_output[i+1]])
                else:
                    new_colors.append([languages_colors[new_output[i]], languages_colors[new_output[i]]])
                    if languages_colors[new_output[i]] not in color_meaning:
                        color_meaning.append(languages_colors[new_output[i]])

            for i in range(0, len(new_input)):
                if new_input[i] != '' and new_input[i][0] == ' ':
                    new_input[i] = new_input[i][1:]
            if new_input[len(new_input)-1] == '':
                del new_input[len(new_input)-1]

            input_dic = dict(zip(new_input, new_colors))

    color_language = []

    for i in color_meaning:

        color_language.append(languages[languages_colors.index(i)])

    card_dic = dict(zip(color_language, color_meaning))

    return render(request, 'GUI/index.html', {'nbar': 'home',
                                              'languages': languages,
                                              'card': card_dic,
                                              'input': input_dic,
                                              })


def about(request):
    return render(request, 'GUI/about.html', {'nbar': 'about'})


def doc(request):
    try:
        return FileResponse(open('LanguageClassifier_Dokumentace.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()