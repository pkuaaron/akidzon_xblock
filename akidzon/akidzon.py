"""TO-DO: Write a description of what this XBlock is."""

import pdb
from akidzon.init_data import session
from akidzon import database
from akidzon.counting import *
import yaml
from xblockutils.resources import ResourceLoader
from xblock.fields import Integer, String, Scope, Dict, List, Boolean
from web_fragments.fragment import Fragment
import pkg_resources
from akidzon.models import QuestionCategory, Question, Student
from akidzon.models import Assessment, Base, question_assessment_association, answer_question_association, \
    student_assessment_association
from datetime import date
import math
from pyquery import PyQuery as pq
from xblock.core import XBlock, XBlockAside
import pprint
from django.template.loader import render_to_string
import os

loader = ResourceLoader(__name__)  # pylint: disable=invalid-name

question_status_color_pair = {True: 'success', False: 'secondary', None: 'danger'}

class AkidzonXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )
    questions_answered = Integer(
        default=0, scope=Scope.user_state,
        help="How many questions the user has answered",
    )
    scores = Integer(
        default=0, scope=Scope.user_state,
        help="Scores the user has got",
    )

    questionbody = ""

    category_id = Integer(
        default=764, scope=Scope.user_state,
        help="The category id for the questions",
    )

    assessment_id = Integer(
        default=1, scope=Scope.user_state,
        help="The assessment id the student is testing",
    )

    question_id = Integer(
        default=0, scope=Scope.user_state,
        help="The question id the student is testing",
    )

    question_id_list = List(
        default=[], scope=Scope.user_state,
        help="The list of question for current student",
    )

    question_link_list = List(
        default=[], scope=Scope.user_state,
        help="The list of question for current student",
    )

    question_list_html = ""

    category_list_html = ""

    questionbody = ""

    question_assessment_id = Integer(
        default=0, scope=Scope.user_state,
        help="The assessement assigned id",
    )

    student_id = Integer(
        default=1, scope=Scope.user_state,
        help="The assessement assigned id",
    )

    standard_answers = Dict(
        default={}, scope=Scope.user_state,
        help="standard answer diction",
    )

    user_answers = Dict(
        default={}, scope=Scope.user_state,
        help="user answer diction",
    )

    show_answers = False

    def get_standard_answer(self, questionbody):
        standard_answers = {}
        items = pq(questionbody)(".form_to_be_checked")
        for item in items:
            pq_item = pq(item)
            item_id = pq_item.attr('id')
            if item_id is not None:
                standard_answers[item_id] = pq_item.attr('value_to_check')
        return standard_answers

    def get_questionbody(self, question_id=0, show_answers=False):
        """ Get the question body and question list based on the category id.
        Parameters
        ----------
        question_id : The question id to load
        show_answers : whether to show the answers
        Returns
        -------
        questionbody : The html of question body;
        """
        path = os.path.join(os.path.dirname(__file__), 'templates/question_category.yml')
        pyml = yaml.load(open(path, 'r', 1))  #
        category_id = pyml['QuestionCategory'][self.category_id].get('same_as',self.category_id)
        print(f'get_questionbody self.category: {self.category_id}')
        print(f'get_questionbody self.question_id: {self.question_id}')

        html_template_path = pyml['QuestionCategory'][category_id].get('html_template_path', 'questions_templates/simple_question.html')
        # html_template_path = os.path.join(os.path.dirname(__file__), 'templates', html_template_path)
        cmd = pyml['QuestionCategory'][category_id]['scripts']
        displayanswer_cmd = pyml['QuestionCategory'][category_id].get('displayanswer_scripts', None)

        # pdb.set_trace()
        question_difficulty_level = 1
        assessment_id = self.assessment_id
        question = None
        questionbody = None

        if question_id != 0:
            question = database.load_question(self.student_id, assessment_id, question_id)

        if question is not None:
            html_arguments = eval(question['html_arguments'])
            self.user_answers = eval(question['user_answers'] or '{}')
            self.question_id = question['question_id']
            self.standard_answers = eval(question['standard_answers'] or '{}')
            html_arguments['user_answers'] = self.user_answers if not show_answers else self.standard_answers
            pprint.pprint(f'Before update answers html_arguments: {html_arguments}')
            html_arguments.update(akidzon_class.generate_answer_options(**html_arguments))
            # pdb.set_trace()
            pprint.pprint(f'After update answers html_arguments: {html_arguments}')
            questionbody = render_to_string(html_template_path, html_arguments)
            # questionbody = render_to_string(html_template_path, {})

        if questionbody is None:
            _locals = locals()
            _globals = globals()
            _globals['student_id'] = self.student_id
            _globals['assessment_id'] = assessment_id
            _globals['question_difficulty_level'] = question_difficulty_level
            print(self.category_id)
            exec(cmd, _globals, _locals)
            interpretable_arguments = _locals.get('interpretable_arguments', {})
            html_arguments = _locals['html_arguments']
            html_arguments['category_id'] = self.category_id
            html_arguments['is_show_question_title'] = True

            question_score = 1
            energy_point = 100
            # pdb.set_trace()
            pprint.pprint(f'html_arguments: {html_arguments}')
            questionbody = render_to_string(html_template_path, html_arguments)
            # questionbody = render_to_string(html_template_path, {})

            self.standard_answers = self.get_standard_answer(questionbody)
            html_arguments_to_save = {k: v for k, v in html_arguments.items() if
                                      not k.endswith('answer_option_objects')}
            question = database.create_new_question(assessment_id, self.category_id, interpretable_arguments,
                                                    html_arguments_to_save, self.standard_answers,
                                                    question_score, energy_point, question_difficulty_level)

            self.question_id = question.id
            self.question_id_list.append(self.question_id)
            self.question_link_list.append(question_status_color_pair.get(None, 'danger'))

        if displayanswer_cmd is None:
            p = pq(questionbody)
            for k, v in self.user_answers.items():
                item = p(f"#{k}")
                item.val(v)
            questionbody = p.outer_html()
        else:
            _locals = locals()
            _globals = globals()
            _globals['answers'] = self.standard_answers if show_answers else self.user_answers
            _globals['questionbody'] = questionbody
            exec(displayanswer_cmd, _globals, _locals)
            questionbody = _locals.get('updated_questionbody', questionbody)
        self.questionbody = questionbody
        return questionbody

    def get_question_list_html(self, columns=4):
        rows = []
        indexes = list(range(len(self.question_id_list)))
        index_list = [indexes[i * columns:(i + 1) * columns] for i in range(math.ceil(len(self.question_id_list) / columns))]
        # pdb.set_trace()
        for row_list in index_list:
            columns_text = []
            for col_index in row_list:
                tmp_id = self.question_id_list[col_index]
                link_type = self.question_link_list[col_index] if self.question_id != tmp_id else 'warning'
                columns_text.append(
                    f'''<td><a class="XAkidzonQuestionLink btn btn-{link_type} btn-sm active"  href="" data-question_id='{tmp_id}'>{tmp_id}</a></td>''')
            row_content = "\n".join(columns_text)
            rows.append(f'''
              <tr align="center">
              {row_content}
              </tr>''')
        table_contents = '\n'.join(rows)
        self.question_list_html = f'''
        <table border="1" class="dataframe">
          <thead>
            <tr style="text-align: center;">
              <th colspan="{columns}">Question</th>
            </tr>
          </thead>
          <tbody>
          {table_contents}
          </tbody>
        </table>'''

        return self.question_list_html

    def get_category_list_html(self):
        # if self.category_list_html:
        #     return self.category_list_html
        # pdb.set_trace()
        cats = database.get_question_category()  # session.query(QuestionCategory).filter_by(has_implemented=True)
        # cats.sort_values(by=['topic'], inplace=True)
        topics = []
        skills = []
        k = 0
        for topic in cats['topic'].unique():
            if k == 0:
                topics.append(
                    f'''<a class="list-group-item list-group-item-action active" id="list-{topic}-list" data-toggle="list"
                     href="#list-{topic}" role="tab" aria-controls="{topic}">{topic}</a>''')
            else:
                topics.append(
                    f'''<a class="list-group-item list-group-item-action" id="list-{topic}-list" data-toggle="list" 
                    href="#list-{topic}" role="tab" aria-controls="{topic}">{topic}</a>''')
            topic_df = cats[cats['topic'] == topic]
            links = []
            for cat_id, cat_skill in zip(topic_df['id'].tolist(), topic_df['skill'].tolist()):
                links.append(f'''<li class="list-group-item"> <a class="XAkidzonCategoryLink btn btn-sm active" data-dismiss="modal"
                    href="" data-category_id='{cat_id}'>{cat_id} {cat_skill}</a></li>''')
            link_list = '\n'.join(links)
            if k == 0:
                skills.append(
                    f'''<div class="tab-pane fade show active" id="list-{topic}" role="tabpanel" aria-labelledby="list-{topic}-list">{link_list}</div>''')
            else:
                skills.append(
                    f'''<div class="tab-pane fade" id="list-{topic}" role="tabpanel" aria-labelledby="list-{topic}-list">{link_list}</div>''')
            k = k + 1

        topic_list = '\n'.join(topics)
        link_panels = '\n'.join(skills)
        self.category_list_html = f'''<div class="row">
              <div class="col-4">
                <div class="list-group" id="list-tab" role="tablist">   
                {topic_list}   
                </div>
              </div>
              <div class="col-8">
                <div class="tab-content" id="nav-tabContent">
                {link_panels}
                </div>
              </div>
            </div>'''
        return self.category_list_html

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def init_assessment(self):
        assessment = session.query(Assessment).get(self.assessment_id)
        if not assessment:
            assessment = Assessment(self.assessment_id, total_score=100, description='Assessment example',
                                    effective_time=None, deadline=None, id=self.assessment_id)
            session.add(assessment)
            session.commit()
        student = session.query(Student).get(self.student_id)
        if not student:
            student = Student(self.student_id, relationship=0, student_name='Isaac Chen',
                              register_date=date(2021, 1, 15),
                              student_birthday=date(2013, 4, 15), student_gender=0, student_grade=2,
                              student_school='Elon Park Elementary School', id=self.student_id)
            student.assessments = [assessment]
            session.add(student)
            session.commit()
        assigned = database.get_student_assessment(self.student_id, self.assessment_id)
        if assigned.empty:
            student_assessment = student_assessment_association(self.student_id, self.assessment_id,
                                                                assessment_starttime=date.today())
            session.add(student_assessment)
            session.commit()

    def student_view(self, context=None):
        """
        The primary view of the AkidzonXBlock, shown to students
        when viewing courses.
        """
        self.student_id = 4
        # time.sleep(4)
        # self.category_list_updated = True
        self.get_category_list_html()
        # pdb.set_trace()

        self.init_assessment()
        print(f'student_view self.category: {self.category_id}')
        print(f'student_view self.question_id: {self.question_id}')
        questionbody = self.get_questionbody(question_id=self.question_id)
        context = {'questions_answered': self.questions_answered,
                   'scores': self.scores,
                   'is_show_submit_btn': True,
                   'questionbody': questionbody,
                   'category_id': self.category_id,
                   'question_list_html': self.get_question_list_html(),
                   'category_list_html': self.category_list_html,
                   'question_id': self.question_id}

        # html_str = self.resource_string("static/html/akidzon.html")
        # frag = Fragment(str(html_str).format(self=self))
        frag = Fragment()
        frag.add_content(loader.render_django_template('templates/akidzon_django.html', context=context))
        frag.add_css(self.resource_string("static/css/akidzon.css"))
        frag.add_javascript(self.resource_string("static/js/src/akidzon.js"))
        frag.initialize_js('AkidzonXBlock')
        return frag

    @XBlock.json_handler
    def select_question_link(self, data, suffix=''):
        user_answers = data.get('user_answers', {})
        pprint.pprint(f'select_question_link user_answers:{user_answers}')
        pprint.pprint(f'select_question_link self.user_answers:{self.user_answers}')
        if user_answers != self.user_answers:
            self.save_answers(user_answers)
        question_id = int(data.get('question_id', self.question_id))
        self.question_id = question_id
        self.force_save_fields(['question_id'])
        self.get_questionbody(self.question_id)
        print(f'select_question_link self.category: {self.category_id}')
        print(f'select_question_link self.question_id: {self.question_id}')
        return {'questions_answered': self.questions_answered,
             'scores': self.scores,
             'questionbody': self.questionbody,
             'category_id': self.category_id,
             'user_answers': self.standard_answers,
             'standard_answers': self.standard_answers,
             'question_list_html': self.get_question_list_html(),
             'category_list_html': self.category_list_html,
             'question_id': self.question_id}

    @XBlock.json_handler
    def select_category_link(self, data, suffix=''):
        # pdb.set_trace()
        category_id = int(data.get('new_category_id', self.category_id))
        print(f'select_category_link self.category: {self.category_id}')
        if category_id == -1:
            return 0
        self.assessment_id = category_id
        self.category_id = category_id
        self.init_assessment()
        df = database.get_assessment_questions(self.student_id, self.assessment_id)
        if not df.empty:
            self.question_id_list = df['question_id'].to_list()
            self.question_id = self.question_id_list[-1]
            self.question_link_list = [question_status_color_pair.get(x, 'danger') for x in df['is_correct'].to_list()]
        else:
            self.question_id_list = []
            self.question_link_list = []
            self.question_id = 0
        self.force_save_fields(['assessment_id', 'category_id', 'question_id', 'question_link_list', 'question_id_list'])
        self.get_questionbody(self.question_id)
        return {'questions_answered': self.questions_answered,
             'scores': self.scores,
             'questionbody': self.questionbody,
             'category_id': self.category_id,
             'user_answers': self.standard_answers,
             'standard_answers': self.standard_answers,
             'question_list_html': self.get_question_list_html(),
             'category_list_html': self.category_list_html,
             'question_id': self.question_id}

    @XBlock.json_handler
    def submit_user_answer(self, data, suffix=''):
        user_answers = data.get('user_answers', {})
        show_answers = data.get('show_answers', 'false')
        if show_answers == 'true':
            show_answers = True
            questionbody=self.get_questionbody(question_id=self.question_id, show_answers=show_answers)
            return {'questions_answered': self.questions_answered,
             'scores': self.scores,
             'questionbody': questionbody,
             'category_id': self.category_id,
             'user_answers': self.standard_answers,
             'standard_answers': self.standard_answers,
             'question_list_html': self.get_question_list_html(),
             'category_list_html': self.category_list_html,
             'question_id': self.question_id}

        self.save_answers(user_answers)

        question_id = 0
        index = self.question_id_list.index(self.question_id)
        if index < len(self.question_id_list) - 1:
            question_id = self.question_id_list[index + 1]
        self.question_id = question_id

        print(f'submit_user_answer self.category: {self.category_id}')
        print(f'submit_user_answer self.question_id: {self.question_id}')
        self.force_save_fields(['question_id'])
        context = {'questions_answered': self.questions_answered,
                   'scores': self.scores,
                   'questionbody': self.get_questionbody(question_id=question_id),
                   'category_id': self.category_id,
                   'user_answers': self.user_answers,
                   'standard_answers': self.standard_answers,
                   'question_list_html': self.get_question_list_html(),
                   'category_list_html': self.category_list_html,
                   'question_id': self.question_id}
        return context

    def save_answers(self, user_answers):
        is_answered, is_correct = utils.check_user_answer(user_answers, self.standard_answers)
        index = self.question_id_list.index(self.question_id)
        self.question_link_list = self.question_link_list[:index] + [
            question_status_color_pair.get(is_correct)] + self.question_link_list[index + 1:]
        if is_answered:
            p = session.query(Question).get(self.question_id)
            # p.standard_answers = str(standard_answers)
            score_earned = int(is_correct)
            answers = session.query(answer_question_association).filter(
                answer_question_association.assessment_id == self.assessment_id,
                answer_question_association.student_id == self.student_id,
                answer_question_association.question_id == self.question_id)

            if answers.all():
                answer = answers.first()
                answer.user_answers = str(user_answers)
                answer.score_earned = score_earned
                answer.is_correct = is_correct
                session.commit()
            else:
                self.questions_answered = self.questions_answered + 1
                answer = answer_question_association(user_answers=str(user_answers), is_correct=is_correct,
                                                     score_earned=score_earned,
                                                     assessment_id=self.assessment_id, question_id=self.question_id,
                                                     student_id=self.student_id)
                session.add(answer)
                session.commit()

            self.scores = self.scores + score_earned


    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AkidzonXBlock",
             """<akidzon/>
             """),
            ("Multiple AkidzonXBlock",
             """<vertical_demo>
                <akidzon/>
                <akidzon/>
                <akidzon/>
                </vertical_demo>
             """),
        ]


class AkidzonAside(AkidzonXBlock, XBlockAside):
    """
    An XBlockAside with thumbs-up/thumbs-down voting.

    Vote totals are stored for all students to see.  Each student is recorded
    as has-voted or not.

    This demonstrates multiple data scopes and ajax handlers.

    NOTE: Asides aren't ready yet, so this is currently not being installed in
    setup.py.  When we get back to working on asides, we'll come up with a more
    sophisticated mechanism to enable this for the developers that want to see
    it.

    """
    @XBlockAside.aside_for('student_view')
    def student_view_aside(self, block, context=None):  # pylint: disable=unused-argument
        """
        Allow the thumbs up/down-voting to work as an Aside as well as an XBlock.
        """
        fragment = self.student_view(context)
        fragment.initialize_js('AkidzonXBlock')
        return fragment