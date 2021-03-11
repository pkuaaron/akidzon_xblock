import yaml
import itertools
import random
from django.templatetags.static import static
import pandas as pd
from datetime import date
import json


def parse_yml(path):
    with open(path, 'r', 1) as file_stream:
        yml_file = yaml.load(file_stream)
    return yml_file


def get_next_question_difficulty_level(question_history):
    question_history = pd.DataFrame.from_dict(question_history)
    question_history = question_history.sort_values(by=['question_difficulty_level', 'interpretable_arguments'])
    return 0


def get_available_img_name(img_type='frame'):
    if img_type == 'frame':
        return ['triangle', 'square', 'pentagon',  'octagon', 'circle']
    elif img_type == 'skip 1':
        return ['apple', 'car', 'clock', 'diamond', 'hamburger', 'key', 'oval', 'pumpkin', 'triangle', 'bear', 'butterfly', 'chicken', 'deer', 'flower', 'girl', 'goat', 'goose', 'heart',
                'horse', 'ox', 'police car', 'rooster', 'rose', 'sheep', 'squirrel', 'tidy bear', 'zebra']
    elif img_type == 'skip n':
        return ['apples', 'cars', 'clocks', 'diamonds', 'hamburgers', 'keys', 'ovals', 'pumpkins', 'triangles', 'bears', 'butterflies', 'chicken', 'deer', 'flowers', 'girls', 'goats', 'geese', 'hearts',
                'horses', 'oxen', 'police cars', 'roosters', 'roses', 'sheep', 'squirrels', 'tidy bears', 'zebras']
    elif img_type == 'groups':
        return [['bear', 'butterfly', 'deer', 'goose', 'horse', 'ox', 'rooster', 'sheep', 'squirrel', 'zebra'],
                ['apple', 'car', 'clock', 'diamond', 'hamburger', 'key', 'oval']]
    elif img_type == 'measure':
        return ['comb', 'pencil', 'scissors', 'forks', 'knife', 'eraser', 'crayon', 'spoon']


def check_user_answer(user_answers, standard_answers):
    total_points = len(standard_answers)
    earned_points = 0
    is_answered = False
    for k, v in standard_answers.items():
        if k in user_answers:
            user_answer = user_answers[k]
            if str(user_answer).strip() == str(v).strip() or (str(user_answer).lower()=='' and str(v).strip().lower()=='false'):
                earned_points = earned_points+1
            if user_answers[k] not in ['false', 'False', '', None, False]:
                is_answered = True

    return is_answered, earned_points == total_points


def convert_df_to_html(df, show_head=True, table_css=None, table_style=''):
    '''
    table_css: {'colname_rowindex':css}
    '''
    table_css = table_css or {}
    rows = df.to_dict(orient='rows')
    columns = [c.lower().replace(' ','') for c in df.columns]
    thead = '''<thead>
<tr style="text-align: center;">
    {}
</tr>
</thead>'''
    trs = [f'''<table  class="table table-bordered table-responsive-md table-striped text-center"> {table_style}''']
    ths = []
    for col in columns:
        ths.append('<th>{}</th>'.format(col))
    if show_head:
        trs.append(thead.format('\n'.join(ths)))
    for i, r in enumerate(rows):
        tds = []
        for col in columns:
            css = table_css.get('{}_{}'.format(col, i))
            if css:
                tds.append('<td {}></td>'.format(css).format(value=r[col]))
            else:
                tds.append('<td>{}</td>'.format(r[col]))
        trs.append('<tr>{}</tr>'.format('\n'.join(tds)))
    trs.append('</table>')
    question_table = '\n'.join(trs)
    return question_table


def get_pos_nums(num):
    pos_nums = []
    pos_units = ['Millions + ', 'Hundreds of Thousands +', 'Tens of Thousands +', 'Thousands +', 'Hundreds +', 'Tens +', 'Ones']

    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return zip(pos_nums[::-1], pos_units[-len(pos_nums):])


def create_table_html(image_names, image_counts, table_type='list'):
    trs = []
    trs1 = []
    trs2 = []
    trs3 = []
    max_tds = 10 if max(image_counts) > 9 else max(image_counts)
    for img, cnt in zip(image_names, image_counts):
        if cnt < 1:
            continue
        tds = ['<tr><td rowspan="{}">{}</td>'.format((cnt-1)//10+1, img.title())]
        for i in range(cnt):
            tds.append('''<td><img src="{}" style='width:50px' alt=""></td>'''.format(static('akidzon_icons/items/{}.png'.format(img))))
            if (i+1) % 10 == 0 and i != 0:
                tds.append('</tr><tr>')
        tds = tds + ["<td></td>"]*(max_tds-i % 10-1)
        tds.append('</tr>')
        trs.append('\n'.join(tds))

        trs1.append('''<tr><td><img src="{}" style='width:50px' alt=""></td><td style='width:100px' class='text-center'>{}</td></tr>'''.format(static('akidzon_icons/items/{}.png'.format(img)), cnt))
        trs2.append('''<tr><td><img src="{}" style='width:50px' alt=""></td><td><img src="{}" style='height:50px' alt=""></td></tr>'''.format(static('akidzon_icons/items/{}.png'.format(img)),
                                                                                                                                              static('akidzon_icons/counting_index/countingstick_{}.png'.format(cnt))))

    if table_type == 'tally':
        correct_graph_html = '''<table  border="1" style='background: transparent'><tr><td class='text-center'>Item</td><td class='text-center'>Count</td></tr>{}</table>'''.format('\n'.join(trs2))
    elif table_type == 'count':
        correct_graph_html = '''<table  border="1" style='background: transparent'><tr><td class='text-center'>Item</td><td class='text-center'>Count</td></tr>{}</table>'''.format('\n'.join(trs1))
    elif table_type == 'horizon_table':
        tds = ['''<td><img src="{}" style='height:50px' alt=""></td>'''.format(static('akidzon_icons/items/{}.png'.format(img))) for img in image_names]
        trs3 = ['''<tr><td style='width:100px'>Items</td>{}</tr>'''.format(''.join(tds))]
        tds = ['''<td class='text-center'>{}</td>'''.format(cnt) for cnt in image_counts]
        trs3.append('''<tr><td style='width:100px'>How many?</td>{}</tr>'''.format(''.join(tds)))
        correct_graph_html = '''<table  border="1" style='background: transparent'>{}</table>'''.format('\n'.join(trs3))
    else:
        correct_graph_html = '''<table  border="1" style='background: transparent'>{}</table>'''.format('\n'.join(trs))
    return correct_graph_html


def add_limit_factors(max_total, number_of_factors=2, min_factor_value=1, min_total=0):
    all_options = [range(min_factor_value, max_total+1) for i in range(number_of_factors)]
    factors = [x for x in itertools.product(*all_options) if sum(x) <= max_total and sum(x) > min_total]
    return factors


def make_a_wrong_result(factor1, factor2, operation='+'):
    if operation == '+':
        return random.choice([x for x in range(abs(factor1-factor2), factor1+factor2+5) if x != factor1+factor2])
    elif operation == '-':
        return random.choice([x for x in range(max(0, factor1-factor2-5), factor1+5) if x != factor1-factor2])


def make_a_formula(target=None, operation='+', is_correct=True, is_formula=False, is_full_formula=False):
    target = target or random.randint(1, 20)
    if operation == '+':
        if is_correct:
            factor1, factor2 = random.choice([(x1, x2) for x1 in range(target+1) for x2 in range(target+1) if x1+x2 == target])
        else:
            factor1, factor2 = random.choice([(x1, x2) for x1 in range(target+1) for x2 in range(target+1) if x1+x2 != target and abs(x1-x2-target) < 4])
    elif operation == '-':
        operation = '–'
        if is_correct:
            factor1, factor2 = random.choice([(x1, x2) for x1 in range(target+21) for x2 in range(target+1) if x1-x2 == target])
        else:
            factor1, factor2 = random.choice([(x1, x2) for x1 in range(target+21) for x2 in range(target+1) if x1-x2 != target and abs(x1-x2-target) < 4])
    if is_formula:
        formula = '{}{}{}'.format(factor1, operation, factor2)
        if is_full_formula:
            return '{}={}'.format(formula, target)
        else:
            return formula
    return factor1, factor2


def flatten_list(l):
    a = []
    for t in l:
        a = a + t
    return a


def get_word_expression(factor1, factor2, operation='+'):
    equals = ['equals', 'is', 'are']
    if operation == '+':
        plus = ['add', 'plus', 'and']
        result = factor1+factor2
    if operation == '-':
        plus = ['minus', 'subtract', 'take away']
        result = factor1-factor2

    if random.randint(1, 10) > 4:
        factor1 = get_word_from_digits(factor1)
        factor2 = get_word_from_digits(factor2)
        result = get_word_from_digits(result)
    if operation == '+':
        return '{} {} {} {} {}'.format(factor1, random.choice(plus), factor2, random.choice(equals), result)
    elif operation == '-':
        return random.choice(['{} {} {} {} {}'.format(factor1, random.choice(plus), factor2, random.choice(equals), result), '{} is subtracted from {} {} {}'.format(factor2, factor1, random.choice(equals), result)])


def get_dict_object_from_request(request, keyword):
    dic = {}
    for k, v in request.items():
        if k.startswith('{}['.format(keyword)) and k.endswith(']'):
            dic[k.replace('{}['.format(keyword), '').replace(']', '')] = v
    return dic


def make_a_number(number, standard=True):
    tens = number//10
    ones = number % 10
    if standard:
        return tens, ones
    else:
        shift = random.randint(1, tens)
        tens = tens - shift
        ones = ones + 10*shift
        return tens, ones


def get_word_from_digits(n):
    units = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["Twenty", "Thirty", "Fourty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    if n <= 9:
        return units[n]
    elif n >= 10 and n <= 19:
        return teens[n-10]
    elif n >= 20 and n <= 99:
        return tens[(n//10)-2] + " " + (units[n % 10] if n % 10 != 0 else "")
    elif n >= 100 and n <= 999:
        return get_word_from_digits(n//100) + " Hundred " + (get_word_from_digits(n % 100) if n % 100 != 0 else "")
    elif n >= 1000 and n <= 99999:
        return get_word_from_digits(n//1000) + " Thousand " + (get_word_from_digits(n % 1000) if n % 1000 != 0 else "")
    elif n >= 100000 and n <= 9999999:
        return get_word_from_digits(n//1000000) + " Million " + (get_word_from_digits(n % 100000) if n % 100000 != 0 else "")
    return ''
