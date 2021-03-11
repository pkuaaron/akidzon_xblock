import math
import json
import itertools


class Answer(object):
    html_tag_id = ''
    html_tag_css = ''
    html_tag_type = ''
    html_tag_data_on = ''
    html_tag_data_off = ''
    html_tag_width = ''
    value_to_check = ''
    standard_answer = ''
    user_answer = ''
    new_cell = ''
    eval_method = ''
    td_style = ''

    def __init__(self, attrs):
        for k, v in attrs.items():
            setattr(self, k, v)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def generate_answer_options(**kwargs):
    html_answer_options = []
    answer_options = kwargs.get('answer_options', []) or []
    break_index = kwargs.get('break_index', []) or []
    total = 0
    is_list_of_list = False
    # import pdb
    # pdb.set_trace()
    for k in answer_options:
        if isinstance(k, (list, tuple)):
            is_list_of_list = True
            total = total + len(k)
            break_index.append(total)
    if is_list_of_list:
        answer_options = list(itertools.chain(*answer_options))

    correct_value_index = kwargs.get('correct_value_index', []) or []
    missing_index = kwargs.get('missing_index', []) or []
    html_tag_css = kwargs.get('html_tag_css', 'one_option_checkbox')
    input_type = kwargs.get('input_type', 'number')
    style = kwargs.get('style', '')
    user_answers = kwargs.get('user_answers', {})
    option_type = kwargs.get('option_type', 'inputbox')
    option_width = kwargs.get('option_width', '')
    returned_dict = {}

    if option_type == 'cells':
        cell_values = kwargs.get('cell_values', [])
        anchor_index = kwargs.get('anchor_index', [])
        correct_index = kwargs.get('correct_index', [])
        checkable = kwargs.get('checkable', False)
        html_answer_options = generate_answer_table(cell_values, break_index, anchor_index, correct_index, missing_index, checkable=checkable, user_answers=user_answers)

    elif option_type == 'input_box_dicts':
        html_answer_options = generate_answer_options_from_dicts(answer_options, user_answers=user_answers)
    else:
        for i, v in enumerate(answer_options):
            a = Answer({})
            a.html_tag_id = 'input_answer_{}'.format(i)
            a.option_type = option_type
            a.html_tag_css = html_tag_css
            a.html_tag_data_on = v
            a.html_tag_data_off = v
            a.value_to_display = v
            a.html_body = v
            a.img_src = v
            a.html_tag_width = option_width
            a.style = style
            a.new_cell = True
            if option_type.endswith('checkbox'):
                a.html_tag_type = 'checkbox'
                a.value_to_check = 'true' if i in correct_value_index else 'false'
            else:
                a.html_tag_type = input_type
                a.value_to_check = v
                if i in missing_index:
                    a.html_tag_css = ' form_to_be_checked'
                elif option_type.endswith('inputbox'):
                    a.kwargs = 'readonly'
                    a.user_answer = v
                    # TODO: set the type based on the correct value
                    a.html_tag_type = 'text'

            if i in break_index:
                a.new_row = True
            if user_answers:
                if option_type.endswith('checkbox'):
                    a.user_answer = 'checked' if user_answers.get(a.html_tag_id, 'false') == 'true' else ''
                else:
                    a.user_answer = user_answers.get(a.html_tag_id, a.user_answer)
            html_answer_options.append(a)
    returned_dict['answer_option_objects'] = html_answer_options

    return returned_dict


def generate_answer_table(cell_values, break_index, anchor_index, correct_index, missing_index, checkable=False, user_answers=''):
    html_answer_options = []
    for i, v in enumerate(cell_values):
        a = Answer({})
        tag_id = 'input_answer_{}'.format(i)
        a.option_type = 'table_inputbox'
        a.html_tag_id = tag_id
        a.value_to_check = v
        a.value_to_display = v
        a.html_tag_editable = 'false'
        if i in anchor_index:
            a.html_tag_css = 'bg-secondary'
        if i in correct_index:
            a.html_tag_css = ' form_to_be_checked'
        if i in break_index:
            a.new_row = True

        if i in missing_index:
            a.html_tag_editable = 'true'
            if user_answers:
                a.value_to_display = user_answers.get(a.html_tag_id, '')
            else:
                a.value_to_display = ''
            a.html_tag_css = ' form_to_be_checked bg-success'

        if checkable:
            a.html_tag_css = a.html_tag_css + ' form_to_be_checked checkable'
            a.value_to_check = 'true' if i in correct_index else 'false'
            a.eval_method = "item.attributes['cell_checked'].value"
            if user_answers:
                if user_answers.get(a.html_tag_id, 'false') == 'true':
                    a.user_answer = 'true'
                    a.html_tag_css = a.html_tag_css + ' bg-success'
                else:
                    a.user_answer = 'false'
        else:
            a.eval_method = "item.textContent"

        html_answer_options.append(a)
    return html_answer_options


def generate_answer_options_from_dicts(answers, option_type=None, user_answers=None):
    html_answer_options = []
    for answer in answers:
        a = Answer(answer)
        a.new_cell = True
        v = a.value_to_check
        a.html_tag_width = int(len(str(v))//2+1)*30
        if user_answers:
            a.user_answer = user_answers.get(a.html_tag_id, a.user_answer)
        # a.option_type = option_type
        html_answer_options.append(a)
    return html_answer_options
