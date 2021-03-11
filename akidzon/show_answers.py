from pyquery import PyQuery as pq


def show_answers_drag_drop(questionbody, answers):
    p = pq(questionbody)
    for k, v in answers.items():
        item = p(f"#{k}")
        item.attr.cell_checked = v
        child_content = item.find('.droppable_content')
        child_content.append(f'<img src="{v}" alt="" style="width:50px;">')
    return p.outer_html()