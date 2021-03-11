import random
import numpy as np
from akidzon import utils
from akidzon import akidzon_class
import inflect

plural_engine = inflect.engine()


def graph_data(image_counts, checkbox_type=None, table_type='list', align='random', in_order=False):
    fruits = ['apple', 'avocado', 'banana', 'cherry', 'citrus', 'grapes', 'hazelnut', 'kiwi', 'lemon', 'nut', 'orange', 'peach', 'pear', 'pineapple', 'plum', 'raspberry', 'strawberry', 'watermelon']
    foods = ['bread', 'biscuit', 'cheese', 'coffee', 'egg', 'hamburger', 'hot dog', 'pizza', 'popcorn', 'pretzel', 'quesadilla', 'sausages', 'steak', 'taco', 'toast']
    items = ['key', 'binoculars', 'sugar cube', 'popcorn', 'gingerbread house', 'pancake', 'mailbox', 'cup']

    g = random.choice([fruits, items, foods])
    image_names = np.random.choice(g, size=len(image_counts), replace=False)
    imgs = []
    for i, cnt in enumerate(image_counts):
        imgs = imgs+['items/{}.png'.format(image_names[i])]*cnt

    if not in_order:
        random.shuffle(imgs)

    if align == 'random':
        grids = [(x1+random.randint(0, 20), y1+random.randint(0, 20)) for x1 in range(0, 600, 70) for y1 in range(0, 350, 70)]
        positions = random.sample(grids, len(imgs))
    elif align == 'vertical':
        grids = [(x1, y1) for x1 in range(0, 600, 50) for y1 in range(0, 250, 50)]
        positions = grids[:len(imgs)]
    elif align == 'horizonal':
        grids = [(x1, y1) for y1 in range(0, 250, 50) for x1 in range(0, 500, 50)]
        positions = grids[:len(imgs)]

    css = ['position: absolute;left:{}px;top:{}px; width:50px'.format(x1, y1) for x1, y1 in positions]
    correct_graph_html = utils.create_table_html(image_names, image_counts, table_type=table_type)
    fake_image_count = [max(1, cnt+random.randint(-3, 3)) if cnt != 0 else cnt for cnt in image_counts]

    fake_graph_html = utils.create_table_html(image_names, fake_image_count, table_type=table_type)
    answer_options = [correct_graph_html, fake_graph_html]
    random.shuffle(answer_options)
    correct_value_index = answer_options.index(correct_graph_html)

    question_title = 'Which table shows the correct graphs?'

    html_arguments = simple_question(question_title, answer_options=answer_options, break_index=range(len(answer_options)), correct_value_index=[correct_value_index], option_type='html_checkbox')
    html_arguments.update({
        'graph_images': list(zip(css, imgs)),
        'canvas_width': '650px',
        'canvas_height': '350px'
    })
    return html_arguments


def money_counting(align='random', in_order=False, coins_dict=None):
    quarters = {'quarter_{}'.format(x): 25 for x in ['head']+['tail{}'.format(i) for i in range(1, 9)]}
    nickels = {'nickel_{}'.format(x): 5 for x in ['head', 'tail']}
    dimes = {'dime_{}'.format(x): 10 for x in ['head', 'tail']}
    pennies = {'penny_{}'.format(x): 1 for x in ['head', 'tail']}
    halfdollars = {'halfdollar_{}'.format(x): 50 for x in ['head', 'tail']}
    dollars = {'dollar_{}'.format(x): 100 for x in ['head']+['tail{}'.format(i) for i in range(1, 13)]}

    coins = {**quarters, **nickels, **dimes, **pennies, **halfdollars, **dollars}
    picked_coins = []
    if coins_dict:
        for k, v in coins_dict.items():
            coin_2_use = [x for x in list(coins.keys()) if x.startswith(k)]
            picked_coins = picked_coins+list(np.random.choice(coin_2_use, size=v, replace=True))
    else:
        coin_2_use = [x for x in list(coins.keys()) if x.startswith(('penny', 'dime'))]
        picked_coins = np.random.choice(coin_2_use, size=10, replace=True)
    imgs = ['money/{}_webpage.png'.format(coin) for coin in picked_coins]
    correct_value = sum([coins[v] for v in picked_coins])

    if in_order:
        imgs = sorted(imgs)

    if align == 'random':
        grids = [(x1+random.randint(0, 20), y1+random.randint(0, 20)) for x1 in range(0, 600, 120) for y1 in range(0, 350, 120)]
        positions = random.sample(grids, len(picked_coins))
    elif align == 'vertical':
        grids = [(x1, y1) for x1 in range(0, 750, 110) for y1 in range(0, 450, 110)]
        positions = grids[:len(picked_coins)]
    elif align == 'horizonal':
        grids = [(x1, y1) for y1 in range(0, 450, 110) for x1 in range(0, 750, 110)]
        positions = grids[:len(picked_coins)]

    css = ['position: absolute;left:{}px;top:{}px;'.format(x1, y1) for x1, y1 in positions]
    question_title = 'How much money are there in the picture?'
    html_arguments = simple_question(question_title, answer_options=[correct_value],  option_type='inputbox')
    html_arguments.update({
        'graph_images': list(zip(css, imgs)),
        'canvas_width': '750px',
        'canvas_height': '600px',
    })
    return html_arguments


def measure_picture():
    item = random.choice(utils.get_available_img_name(img_type='measure'))
    measure_item = 'measures/{}_horizontal_1.png'.format(item)
    correct_value = random.randint(8, 15)
    measure_width = '{}cm'.format(correct_value)
    question_title = '''How many centimeters is the {}?'''.format(item)
    html_arguments = simple_question(question_title, answer_options=[correct_value], option_type='inputbox')
    html_arguments.update({
        'measure_width': measure_width,
        'measure_item': measure_item,
    })
    return html_arguments


def two_numbers_operation(factor1, factor2, operation='+', horizonal_equations=None, question_title=None, css=None, question_pictures=None, is_horizonal_equation=False):
    len1 = len(str(factor1))
    len2 = len(str(factor2))
    answer = eval(f'{factor1}{operation}{factor2}')
    len_answer = len(str(answer))

    row_len = max(len1, len2+1, len_answer)

    first_row = '%{}d'.format(row_len) % factor1
    correct_values = '%{}d'.format(row_len) % answer
    defalt_horizonal_equations = list(zip(['display', 'display', 'display', 'display', 'number'], [factor1, operation, factor2, '=', answer]))
    if operation == '-':
        second_row = '–%{}d'.format(row_len-1) % factor2
        question_title = 'Calculate the result for the following subtraction.'
    elif operation == '+':
        second_row = '+%{}d'.format(row_len-1) % factor2
        question_title = 'Calculate the result for the following addition.'
    styles = css or ['', 'border-bottom-style: solid', 'missing']

    answer_options = []

    i = 0

    if is_horizonal_equation:
        horizonal_equations = horizonal_equations or defalt_horizonal_equations
        for cls, v in horizonal_equations:
            d = {'html_tag_id': 'input_answer_{}'.format(i), 'td_style': cls, 'html_tag_style': 'display: inline;',
                 'html_tag_type': 'text', 'value_to_check': v, 'option_type': 'inputbox'}
            if cls == 'number':
                d['html_tag_css'] = 'form_to_be_checked input_for_answers'
            elif cls == 'new_row':
                d['new_row'] = True
                d['option_type'] = "display_only"
            else:
                d['value_to_display'] = v
                d['is_display_only'] = True
                d['option_type'] = "display_only"
                d['kwargs'] = 'readonly'
            i = i+1
            answer_options.append(d)
    else:
        for cls, row in zip(styles, [first_row, second_row, correct_values]):
            for j, v in enumerate(row):
                d = {'html_tag_id': 'input_answer_{}'.format(i), 'td_style': cls, 'html_tag_style': 'display: inline; border:0; width:30px; font-size: 35px;',
                     'html_tag_type': 'text', 'value_to_check': v, 'standard_answer': v, 'max_length': 1, 'option_type': 'inputbox', 'new_cell': True}
                if cls == 'missing':
                    d['html_tag_css'] = 'form_to_be_checked input_for_answers'
                    d['html_tag_style'] = 'display: inline; border:4; width:30px; font-size: 35px;'
                    # pass
                else:
                    d['user_answer'] = v
                    d['value_to_display'] = v
                    d['kwargs'] = 'readonly'
                i = i+1
                d['new_row'] = (j+1 == len(row))
                answer_options.append(d)

    question_title = question_title or 'Add the following 2 numbers?'
    return simple_question(question_title, answer_options=answer_options, option_type='input_box_dicts', question_pictures=question_pictures, kwargs={'img_style': 'height:50px;'})


def operation_enum(factor_list1, factor_list2, question_title=None, table_title=None, operation='+'):
    formulas = ['{}{}{}={}'.format(x1, operation, x2, eval('{}{}{}'.format(x1, operation, x2))) for x1, x2 in zip(factor_list1, factor_list2)]

    answer_options = []
    missed_row = random.randint(0, len(formulas)-1)
    i = 0
    for v in formulas:
        d = {'html_tag_id': 'input_answer_{}'.format(i),  'html_tag_style': 'width:130px',
             'html_tag_type': 'text', 'value_to_check': v, 'standard_answer': v,
             'html_tag_editable': 'true', 'option_type': 'table_inputbox'}
        if i == missed_row:
            d['html_tag_css'] = 'form_to_be_checked input_for_answers bg-success'
        else:
            d['value_to_display'] = v
            d['kwargs'] = 'readonly'
            d['html_tag_editable'] = 'false'
        i = i+1
        d['new_row'] = True
        answer_options.append(d)

    html_arguments = simple_question(question_title=question_title, answer_options=answer_options, option_type='input_box_dicts')
    html_arguments.update({'answer_table_class': 'table table-bordered table-responsive-md table-striped text-center'})
    return html_arguments


def addition_table(package_count):
    units = random.choice(range(3, 10))
    packages_items_pair = [('package', 'rubber ball'), ('bag', 'ball'), ('pencil box', 'pencil'), ('pencil box', 'pen'),
                           ('backpack', 'book'), ('room', 'desk'), ('pencil box', 'pencil'), ('pencil box', 'pencil'),
                           ('locker', 'sweat'), ('pencil box', 'pencil'), ('plate', 'cookie'), ('block', 'house'),
                           ('cage', 'bird'), ('pencil box', 'pencil'), ('bowl', 'candy'), ('branch', 'apple'),
                           ('pencil box', 'pencil'), ('laundry basket', 'shirt'), ('pencil box', 'pencil'),
                           ('cup', 'ice cube'), ('fish tank', 'fish'), ('fish tank', 'golden fish'), ('fish tank', 'fish'),
                           ('farm', 'pig'), ('farm', 'chicken'), ('farm', 'dog'), ('farm', 'mill'), ('farm', 'truck'), ('farm', 'worker')]
    package_name, item_name = random.choice(packages_items_pair)
    packages = list(range(1, package_count+1))
    items = utils.flatten_list([[x, y] for x, y in zip(packages, [x*units for x in packages])])
    number_list = [f'Number of {plural_engine.plural(package_name)}', f'Number of {plural_engine.plural(item_name)}'] + items
    break_index = list(range(-1, len(number_list), 2))

    question_title = '''Each {package} has {units_per_package} {item_name},<br> How many {item_name}
    are there in {package_count} {package_plural}?'''.format(
        package=package_name,
        units_per_package=units, item_name=plural_engine.plural(item_name),
        package_count=package_count, package_plural=plural_engine.plural(package_name))
    html_arguments = counting_with_table(number_list=number_list, break_index=break_index, missing_index=[len(number_list)-1], question_title=question_title)
    return html_arguments


def counting_by_pic(min, max, steps=1, step_options=None, is_frame=False, answer_options=None, option_type=None, option_width=100, is_placeofvalue=False, kwargs={}):
    steps = steps or random.choice(step_options or range(1, 11))
    replicate_count = random.randint(min, max)
    correct_value = steps*replicate_count

    if option_type == 'inputbox':
        answer_options = [correct_value]
    missing_index = [0]
    correct_value_index = answer_options.index(correct_value)
    if steps == 1:
        counting_items = utils.get_available_img_name(img_type='skip 1')
        item_name = random.choice(counting_items)
        question_title = 'Count the number of {}.'.format(item_name)
    else:
        counting_items = utils.get_available_img_name(img_type='skip n')
        item_name = random.choice(counting_items)
        question_title = 'Count the {} by skip counting of {}'.format(item_name, steps)
    if is_frame:
        counting_items = utils.get_available_img_name()
        item_name = random.choice(counting_items)
        question_title = 'Count the number of {}.'.format(item_name)
        question_pictures = ['shapes/{}_{}_count{}.png'.format(item_name, random.randint(1, 6), 10)]*(correct_value//10)
        if correct_value % 10:
            question_pictures = question_pictures+['shapes/{}_{}_count{}.png'.format(item_name, random.randint(1, 6), correct_value % 10)]
        question_pictures_dict = [{'html_tag_css': 'float-left', 'img_src': pic, 'new_row': True,
                                   'img_style': kwargs.get('img_style', 'height:50px; width:500px')} for pic in question_pictures]
        if is_placeofvalue:
            placeofvalues = utils.get_pos_nums(correct_value)
            answer_options = []
            for n, u in placeofvalues:
                answer_options = answer_options+[n, u]
            missing_index = range(0, len(answer_options), 2)
    else:
        question_pictures_dict = []
        for i in range(replicate_count):
            question_pictures_dict.append({'img_src': 'skipcounting/skipcounting{}_{}.png'.format(steps, item_name), 'new_row': not bool((i+1) % 5),
                                           'td_style': 'width: 100px; height:150px', 'html_tag_css': 'counting_picture',
                                           'img_style': kwargs.get('img_style', "width: 100px;position: relative; top: 0px; left: 0px; z-index: 1;")}
                                          )

    break_index = range(4, len(answer_options), 5)
    html_arguments = simple_question(question_title, option_type=option_type, question_pictures=question_pictures_dict, answer_options=answer_options, break_index=break_index,
                                     missing_index=missing_index, correct_value_index=correct_value_index)
    html_arguments.update({
        'skipcounting': steps
    })
    return html_arguments


def ordinal_counting(max_items=3):
    groups = utils.get_available_img_name(groups=True)
    ordinal = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth']
    answer_options = random.sample(random.choice(groups), max_items)
    item_to_show = [random.choice(answer_options) for _ in range(10)]  # random.choices(items,k=10)
    selected_values = random.randint(1, 9)
    correct_value_index = [answer_options.index(item_to_show[selected_values])]
    question_title = 'The first picture is {}, what is the {} picture?'.format(item_to_show[0], ordinal[selected_values].lower())
    question_pictures = ['skipcounting/skipcounting1_{}.png'.format(x) for x in item_to_show]

    return simple_question(question_title, answer_options=answer_options, option_type='checkbox', correct_value_index=[correct_value_index],
                           question_pictures=[question_pictures], kwargs={'img_style': 'height:75px; width:75px'})


def simple_question(question_title, option_type=None, question_pictures=None, input_type='number', answer_options=None, break_index=None,
                    checkbox_type=None, correct_value_index=None, missing_index=None, option_width=100, style='', kwargs={}):
    '''
    '''
    if correct_value_index is not None and type(correct_value_index) != type([]):
        correct_value_index = [correct_value_index]

    missing_index = missing_index or [0]

    html_arguments = {
        'answer_options': answer_options,
        'style': style,
        'break_index': break_index,
        'input_type': input_type,
        'correct_value_index': correct_value_index,
        'missing_index': missing_index,
        'checkbox_type': checkbox_type,
        'option_type': option_type,
        'option_width': option_width
    }

    html_arguments.update(akidzon_class.generate_answer_options(**html_arguments))
    img_style = kwargs.get('img_style', '')
    question_pictures_dict = []
    for qp in question_pictures or []:
        if type(qp) == type({}):
            question_pictures_dict.append(qp)
        elif type(qp) == type([]):
            for i, p in enumerate(qp):
                question_pictures_dict.append({'img_src': p, 'new_row': i+1 == len(qp), 'img_style': img_style})
        else:
            question_pictures_dict.append({'img_src': qp, 'new_row': True, 'img_style': img_style})
    html_arguments.update({
        'question_title': question_title,
        'question_pictures': question_pictures_dict
    })
    return html_arguments


def simple_counting(min, max, steps=0, direction=None, step_options=None, freetext=None):
    number_names = {1: 'ones', 2: 'twos', 3: 'threes', 4: 'fours', 5: 'fives', 6: 'sixes', 7: 'sevens', 8: 'eights', 9: 'nines', 10: 'tens'}
    anchor_number = random.randint(min, max)

    if steps == 1:
        direction = direction or [('backwards', -1), ('forwards', 1)]
        select_direction = random.choice(direction)
        correct_value = anchor_number+steps*select_direction[1]
        question_title = 'When counting <strong>{}</strong> from <strong>{}</strong>, which number is the next?'.format(select_direction[0], anchor_number)
    else:
        direction = direction or [('before', -1), ('after', 1)]
        select_direction = random.choice(direction)
        steps = steps or random.choice(step_options)
        correct_value = anchor_number+steps*select_direction[1]
        question_title = 'Which number is <strong>{} {}</strong> when counting by <strong>{}</strong>?'.format(select_direction[0], anchor_number, number_names[steps])

    return simple_question(question_title, answer_options=[correct_value], option_type='inputbox')


def counting_with_table(number_list=None, break_index=None, missing_count=2, missing_index=None, direction=None, question_title=None):
    number_list = number_list or range(1, 101)
    break_index = break_index or list(range(-1, 100, 10))

    if direction:
        # direction = [('more':1),('less':-1)]
        select_direction = random.choice(direction)
        anchor_index = random.choice(number_list[10:90])
        move_steps = random.choice(range(1, 11))
        anchor_number = number_list[anchor_index]
        correct_index = [anchor_index+move_steps*select_direction[1]]
        html_arguments = {
            'cell_values': number_list,
            'break_index': break_index,
            'anchor_index': [anchor_index],
            'correct_index': correct_index,
            'checkable': True,
            'option_type': 'cells',
        }
        html_arguments.update(akidzon_class.generate_answer_options(**html_arguments))
        html_arguments.update({
            'answer_table_class': 'table table-bordered table-responsive-md table-striped text-center',
            'question_title': 'Pick the number that is <strong>{} {}</strong> than <strong>{}</strong> in the one hundred chart'.format(move_steps, select_direction[0], anchor_number),
        })
    else:
        missing_index = missing_index or random.sample(range(len(number_list)), missing_count)

        html_arguments = {
            'cell_values': number_list,
            'break_index': break_index,
            'missing_index': missing_index,
            'checkable': False,
            'option_type': 'cells',
        }
        html_arguments.update(akidzon_class.generate_answer_options(**html_arguments))
        html_arguments.update({
            'answer_table_class': 'table table-bordered table-responsive-md table-striped text-center',
            'question_title': question_title or 'Fill all the missing number in the one hundred chart',
        })
    return html_arguments


def drag_and_drop_pattern(pattern_scheme='repeat', difficult_level=0, missing_count=1, prefill_count=0):
    shapes = ['hexagon_6.png', 'hexagon_7.png', 'hexagon_8.png',
            'circle_1.png','square_1.png','hexagon_1.png','heptagon_1.png','pentagon_1.png','triangle_1.png',
            'circle_2.png','square_2.png','hexagon_2.png','heptagon_2.png','pentagon_2.png','triangle_2.png',
            'circle_3.png','square_3.png','hexagon_3.png','heptagon_3.png','pentagon_3.png','triangle_3.png',
            'circle_4.png','square_4.png','hexagon_4.png','heptagon_4.png','pentagon_4.png','triangle_4.png']

    pattern_difficulties = [['01', '001','011', '0011', '0111', '0001'],
                            ['010', '012', '0012', '0112', '0122'],
                            ['0121','0120', '0110', '0012', '0010'],
                            [
                                ['01', '0011', '000111', '00001111'],
                                ['010', '0110', '01110', '011110'],
                                ['01', '001', '0001', '00001'],
                                ['010', '00100', '0001000', '000010000']
                             ]
                        ]
    pattern_template = random.choice(pattern_difficulties[difficult_level])
    break_index = []
    if isinstance(pattern_template, (list, tuple)):
        if pattern_scheme == 'row':
            j = 0
            for s in pattern_template:
                j += len(s)
                break_index.append(j)
        pattern = [int(c) for c in ''.join(pattern_template)]
    else:
        pattern = [int(c) for c in pattern_template] * 3
    picked_shapes = random.sample(shapes, len(set(pattern)))
    picture_pattern = [f'shapes/{picked_shapes[i]}' for i in pattern]
    size = len(picture_pattern)

    if pattern_scheme == 'repeat':
        question_title = 'Repeat the pattern above.'
        break_index = [size]
        missed_pic_index = random.sample(list(range(size, size*2)),size-prefill_count)
        picture_pattern = picture_pattern * 2
    elif pattern_scheme == 'row':
        question_title = 'Fill the last row by following the patterns.'
        missed_pic_index = random.sample(list(range(break_index[-2], break_index[-1])), break_index[-1] - break_index[-2] - prefill_count)
    elif pattern_scheme == 'maker':
        question_title = f'Use the shapes to make an {pattern_template.replace("0","A").replace("1","B").replace("2","c")} pattern.'
        missed_pic_index = list(range(2, size))
    else:
        question_title = 'Fill the empty box with the right picture to finish the pattern.'
        missed_pic_index = random.sample(range(size), missing_count)

    html_arguments = {'question_title': question_title,
                      'picture_pattern': list(enumerate(picture_pattern)),
                      'break_index': break_index,
                      'missed_pic_index': missed_pic_index,
                      'missed_picture_options': list(enumerate([f'shapes/{nm}' for nm in picked_shapes]))
                      }
    return html_arguments
