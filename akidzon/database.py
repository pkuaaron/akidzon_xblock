from akidzon.models import QuestionCategory, Question, Student, Assessment, Base, question_assessment_association
from akidzon.init_data import session
import pandas as pd


def get_assessment_questions(student_id, assessment_id, question_id=None):
    question_id_filter = 'question_id={}'.format(question_id) if question_id else 'question_id is not NULL'
    sql = f'''SELECT question_id, interpretable_arguments,
        html_arguments, question_type, question_title,
        standard_answers, question_judge_method,
        category_id, question_assessment_id,
        max_score, energy_point, question_difficulty_level,
        assessment_id,
        assessment_score, is_finished,
        student_id, answer_id, answer_starttime, answer_submittime,
        user_answers, question_score_earned, is_correct,
        teacher_comments
    	FROM xakidzon_assessment_questions_view
        where student_id={student_id} and assessment_id={assessment_id} and {question_id_filter}'''
    print(sql)
    df = pd.read_sql_query(sql, session.bind)
    return df


def get_question_category():
    df = pd.read_sql_query(session.query(QuestionCategory).filter(QuestionCategory.has_implemented == 1).statement, session.bind)
    df.sort_values(['id'], inplace=True)
    return df


def get_question_by_category(question_category_id, student_id, answered=False):
    is_answered = 'user_answers is NOT NULL' if answered else 'user_answers is NULL'
    sql = f'''SELECT question_id, interpretable_arguments,
        html_arguments, question_type, question_title,
        standard_answers, question_judge_method,
        category_id, question_assessment_id,
        max_score, energy_point, question_difficulty_level,
        assessment_id,
        assessment_score, is_finished,
        student_id, answer_id, answer_starttime, answer_submittime,
        user_answers, question_score_earned, is_correct,
        teacher_comments
    	FROM xakidzon_assessment_questions_view where student_id={student_id}
        and category_id={question_category_id} and {is_answered}'''

    df = pd.read_sql_query(sql, session.bind)
    return df


def get_question_answers(student_id, assessment_id, question_id):
    sql = f'''SELECT * FROM xakidzon_useranswer where student_id={student_id} and assessment_id={assessment_id} and question_id={question_id}'''
    df = pd.read_sql_query(sql, session.bind)
    return df

def get_student_assessment(student_id, assessment_id):
    sql = f'''SELECT * FROM xakidzon_student_assessment where student_id={student_id} and assessment_id={assessment_id}'''
    df = pd.read_sql_query(sql, session.bind)
    return df


def load_unfinished_question(student_id, category_id):
    questions = get_question_by_category(question_category_id=category_id, student_id=student_id)
    if not questions.empty:
        question = questions.to_dict(orient='rows')[-1]
        return question
    else:
        return None


def load_question(student_id, assessment_id, question_id):
    questions = get_assessment_questions(student_id=student_id, assessment_id=assessment_id, question_id=question_id)
    if not questions.empty:
        question = questions.to_dict(orient='rows')[-1]
        return question
    else:
        return None


def create_new_question(assessment_id, category_id, interpretable_arguments, html_arguments,standard_answers,
                       question_score, energy_point, question_difficulty_level):
    question = Question(interpretable_arguments=str(interpretable_arguments), html_arguments=str(html_arguments), standard_answers=str(standard_answers))
    session.add(question)
    session.commit()

    question_assessment = question_assessment_association(assessment_id=assessment_id, question_id=question.id,
                       energy_point=energy_point, max_score=question_score,
                       question_difficulty_level=question_difficulty_level)
    session.add(question_assessment)
    session.commit()
    # assessment = session.query(answer_question_association).filter_by(assessment_id=assessment_id, question_id=question.id)
    # pdb.set_trace()
    return question

def database_initialize():
    result_set = session.execute('''select * from akidzon_questioncategory''')
    for r in result_set:
        q=QuestionCategory(r.grade, r.subject, r.sub_subject, r.letter_index, r.topic, r.skill, r.description,id=r.question_category_id)
        session.add(q)
    session.commit()