import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import pickle
from urllib.parse import unquote
from itertools import chain


def classify(model, input, languages):
    original_input = input.copy()
    original_input[0] = original_input[0].split()
    input[0] = input[0].translate({ord(c): " " for c in
                                   ",|\$|\{|\}|\-|\+|\[|\]|\<|\>|\"|\=|\:|\;|\*|\||\#|\$|\(|\)|\/|\.|\–|\_|\«|\»|\—|\!|\&|\?|\`|\~|\%|\@|\¡|\™|\£|\¢|\∞|\§|\¶|\•|\ª|\º|\–|\≠|\«|\æ|\÷|\≥|\≤|\÷|\»|\\|\^|\ˆ|\|\\|\||\）|\（|\、|\""})
    input[0] = ''.join([i for i in input[0] if not i.isdigit()])
    input[0] = input[0].lower()
    input[0] = re.sub(' +', ' ', input[0])

    input_list = input[0].split()
    krok = 5
    input_list = [' '.join(input_list[i: i + krok]) for i in range(0, len(input_list), krok)]
    output_list = []
    percent = []

    for count in range(0, len(input_list)):
        output_list.append(model.predict_proba(input_list).argmax(-1)[count])
        percent.append(model.predict_proba(input_list)[count][model.predict_proba(input_list)[0].argmax(-1)])

    for i in range(0, len(output_list), 1):
        if i + 1 < len(output_list) and i + 2 < len(output_list):
            if output_list[i] != output_list[i + 1] and output_list[i] == output_list[i + 2]:
                output_list[i + 1] = output_list[i]
    if output_list[len(output_list) - 1] != output_list[len(output_list) - 2]:
        output_list[len(output_list) - 1] = output_list[len(output_list) - 2]
    temp_input = []
    x = -1
    for i in range(0, len(output_list)):
        if x != output_list[i]:
            x = output_list[i]
            temp_input.append(input_list[i])
        else:
            temp_input[len(temp_input) - 1] = temp_input[len(temp_input) - 1] + " " + input_list[i]

    input_list = []
    for i in range(0, len(temp_input), 1):
        input_list.append(' '.join(word for word in temp_input[i].split(" ")[:5]))
        input_list.append(' '.join(word for word in temp_input[i].split(" ")[5:-5]))
        input_list.append(' '.join(word for word in temp_input[i].split(" ")[-5:]))
    input_list = list(dict.fromkeys(input_list))
    if '' in input_list:
        input_list.remove('')
    if ' ' in input_list:
        input_list.remove(' ')
    changes = True
    output_list = []

    for i in range(0, len(input_list), 1):
        output_list.append(model.predict_proba(input_list)[i].argmax(-1))
    x = 0
    while (changes and x <= 25):
        changes = False
        x = x+1
        temp_output = output_list.copy()
        for i in range(0, len(input_list), 1):
            if i - 1 > 0 and i + 1 < len(input_list):
                if output_list[i - 1] != output_list[i] and output_list[i] != output_list[i + 1]:
                    changes = True
                    p1 = model.predict_proba(input_list)[i - 1][output_list[i - 1]]
                    p2 = model.predict_proba(input_list)[i][output_list[i - 1]]
                    p3 = model.predict_proba(input_list)[i][output_list[i + 1]]
                    p4 = model.predict_proba(input_list)[i + 1][output_list[i + 1]]
                    if abs(p1 - p2) > abs(p4 - p3):
                        temp_output[i] = output_list[i - 1]
                    else:
                        temp_output[i] = output_list[i + 1]
        output_list = temp_output.copy()
    x = -1
    new_input = []
    new_output = []
    for i in range(0, len(input_list), 1):
        if output_list[i] != x:
            x = output_list[i]
            new_output.append(x)
            new_input.append(input_list[i])
        else:
            new_input[len(new_input) - 1] = new_input[len(new_input) - 1] + " " + input_list[i]
    new_lang = []
    new_orig = original_input[0].copy()
    l = len(original_input[0])
    for i in new_input:
        input = i.split()
        for word1 in range(0, len(input)):
            for word2 in range(0, len(original_input[0])):
                if input[word1] in original_input[0][word2].lower():
                    del original_input[0][:word2]
                    break
        new_lang.append(l - len(original_input[0]))
    new_input = []
    last = 0
    for i in range(0, len(new_lang)):
        new_input.append(' '.join(word for word in new_orig[last:new_lang[i]]))
        last = new_lang[i]
    new_input[len(new_input) - 1] += " " + ' '.join(word for word in new_orig[last:])

    return new_output, new_input