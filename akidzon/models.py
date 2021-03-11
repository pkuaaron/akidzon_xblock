from sqlalchemy import Column, String, Integer, SmallInteger, Date, DateTime, Float, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship as SQLRelationship
from sqlalchemy.ext.declarative import declarative_base
import random
import pandas as pd
from datetime import date, datetime

GRADE = (
    (-1, 'Pre-K'),
    (0, 'K'),
    (1, 'First Grade'),
    (2, 'Second Grade'),
    (3, 'Third Grade'),
    (4, 'Forth Grade'),
    (5, 'Fifth Grade'),
    (6, 'Sixth Grade'),
    (7, 'Seventh Grade'),
    (8, 'Eighth Grade'),
    (9, 'Ninth Grade'),
    (10, 'Tenth Grade'),
    (11, 'Eleventh Grade'),
    (12, 'Twelvth Grade'),
    (13, 'Thirteenth Grade'),
    (14, 'Forteenth Grade'),
    (15, 'Fifteenth Grade'),
    (16, 'Sixteenth Grade'),
)
SUBJECT = (
    (0, 'Math'),
    (1, 'Reading'),
    (2, 'Language'),)

GENDER = (
    (0, 'Male'),
    (1, 'Female'))

RELATIONSHIP = ((0, 'parent child'), (1, 'teacher student'), (2, 'other'))
PROBLEM_TYPE = ((0, 'SingleChoice'), (1, 'MultipleChoice'), (2, 'FreeText'), (3, 'Number'), (4, 'List'))
LEVEL = ((0, 'Easy'), (1, 'Middle'), (2, 'Difficult'), (3, 'Challenge'), (4, 'Olympic'))
Base = declarative_base()

# student_assessment_association = Table(
#     'xakidzon_student_assessment', Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('assessment_id', Integer, ForeignKey('xakidzon_assessment.id',ondelete="CASCADE"), nullable=True),
#     Column('student_id', Integer, ForeignKey('xakidzon_student.id',ondelete="CASCADE"), nullable=True),
#     Column('assessment_starttime', DateTime),
#     Column('assessment_endtime', DateTime),
#     Column('assessment_score', Float),
#     Column('is_finished', Boolean),
#     Column('comments', String(512))
# )
class student_assessment_association(Base):
    __tablename__ = 'xakidzon_student_assessment'
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('xakidzon_assessment.id',ondelete="CASCADE"), nullable=True)
    student_id = Column(Integer, ForeignKey('xakidzon_student.id',ondelete="CASCADE"), nullable=True)
    assessment_starttime = Column(DateTime)
    assessment_endtime = Column(DateTime)
    assessment_score = Column(Float)
    is_finished = Column(Boolean)
    comments = Column(String(512))

    def __init__(self, student_id, assessment_id, assessment_score=100, assessment_starttime=None, assessment_endtime=None,is_finished=False, comments=None):
        self.assessment_id = assessment_id
        self.student_id = student_id
        self.assessment_starttime = assessment_starttime
        self.assessment_endtime = assessment_endtime
        self.assessment_score = assessment_score
        self.is_finished = is_finished
        self.comments = comments


class question_assessment_association(Base):
    __tablename__ = 'xakidzon_question_assessment'
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('xakidzon_assessment.id',ondelete="CASCADE"), nullable=True)
    question_id = Column(Integer, ForeignKey('xakidzon_question.id',ondelete="CASCADE"), nullable=True)
    energy_point = Column(SmallInteger)
    question_difficulty_level = Column(SmallInteger)
    max_score = Column(Float)

    def __init__(self, assessment_id, question_id, energy_point=None, max_score=None, question_difficulty_level=None):
        self.assessment_id = assessment_id
        self.question_id = question_id
        self.energy_point = energy_point
        self.max_score = max_score
        self.question_difficulty_level = question_difficulty_level


# question_assessment_association = Table(
#     'xakidzon_question_assessment', Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('assessment_id', Integer, ForeignKey('xakidzon_assessment.id',ondelete="CASCADE"), nullable=True),
#     Column('question_id', Integer, ForeignKey('xakidzon_question.id',ondelete="CASCADE"), nullable=True),
#     Column('energy_point', SmallInteger),
#     Column('question_difficulty_level', SmallInteger),
#     Column('max_score', Float)
# )

class answer_question_association(Base):
    __tablename__ = 'xakidzon_useranswer'
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('xakidzon_assessment.id', ondelete="SET NULL"), nullable=True)
    student_id = Column(Integer, ForeignKey('xakidzon_student.id',ondelete="SET NULL"), nullable=True)
    question_id = Column(Integer, ForeignKey('xakidzon_question.id',ondelete="CASCADE"), nullable=True)
    answer_starttime = Column(DateTime)
    answer_submittime = Column(DateTime)
    score_earned = Column(Float)
    is_correct = Column(Boolean)
    max_score = Column(Float)
    teacher_comments = Column(String(1024))
    user_answers = Column(String(4096))


    def __init__(self, assessment_id, student_id, question_id, answer_starttime=None, answer_submittime=None,
                 score_earned=None, is_correct=None, max_score=None, teacher_comments=None, user_answers=None):
        self.assessment_id =assessment_id
        self.student_id = student_id
        self.question_id = question_id
        self.answer_starttime = answer_starttime
        self.answer_submittime = answer_submittime
        self.score_earned = score_earned
        self.is_correct = is_correct
        self.max_score = max_score
        self.teacher_comments = teacher_comments
        self.user_answers = user_answers

# answer_question_association = Table(
#     'xakidzon_useranswer', Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('assessment_id', Integer, ForeignKey('xakidzon_assessment.id',ondelete="SET NULL"), nullable=True),
#     Column('student_id', Integer, ForeignKey('xakidzon_student.id',ondelete="SET NULL"), nullable=True),
#     Column('question_id', Integer, ForeignKey('xakidzon_question.id',ondelete="CASCADE"), nullable=True),
#     Column('answer_starttime', DateTime),
#     Column('answer_submittime', DateTime),
#     Column('score_earned', Float),
#     Column('is_correct', Boolean),
#     Column('max_score', Float),
#     Column('teacher_comments', String(1024)),
#     Column('user_answers', String(8192))
# )


class Question(Base):
    __tablename__ = 'xakidzon_question'
    id = Column(Integer, primary_key=True)

    interpretable_arguments = Column(String(512))
    html_arguments = Column(String(8192))
    question_type = Column(SmallInteger)
    question_title = Column(String(1024))

    standard_answers = Column(String(4096))
    question_judge_method = Column(String(1024))
    category_id = Column(Integer, ForeignKey('xakidzon_questioncategory.id',ondelete="SET NULL"), nullable=True)

    def __init__(self, interpretable_arguments=None, html_arguments=None, question_type=None, question_title=None,
                 standard_answers=None, question_judge_method=None):
        self.interpretable_arguments = interpretable_arguments
        self.html_arguments = html_arguments
        self.question_type = question_type
        self.question_title = question_title
        self.standard_answers = standard_answers
        self.question_judge_method = question_judge_method

    def __str_(self):
        return self.question_title

    def to_dict(self):
        return {
            'id': self.id,
            'interpretable_arguments': self.interpretable_arguments,
            'question_type': self.question_type,
            'question_html': self.question_html,
            'standard_answers': self.standard_answers
        }


class QuestionCategory(Base):
    __tablename__ = 'xakidzon_questioncategory'
    id = Column(Integer, primary_key=True)
    grade = Column(SmallInteger)
    subject = Column(SmallInteger)
    sub_subject = Column(String(64))
    letter_index = Column(String(2))
    topic = Column(String(64))
    skill = Column(String(128))
    description = Column(String(128))
    has_implemented = Column(Boolean)

    def __init__(self, grade, subject, sub_subject, letter_index, topic, skill, description,id=None, has_implemented=False):
        if id is not None:
            self.id=id
        self.grade = grade
        self.subject = subject
        self.sub_subject = sub_subject
        self.letter_index = letter_index
        self.topic = topic
        self.skill = skill
        self.description = description
        self.has_implemented = has_implemented


class Assessment(Base):
    __tablename__ = 'xakidzon_assessment'
    id = Column(Integer, primary_key=True)
    assessment_owner = Column(Integer)

    total_score = Column(Float)
    description = Column(String(512))
    effective_time = Column(DateTime)
    deadline = Column(DateTime)
    questions = SQLRelationship(Question, secondary="xakidzon_question_assessment")

    def __init__(self, assessment_owner, total_score=100, description='Assessment example', effective_time=None, deadline=None, id=None):
        if id is not None:
            self.id=id
        self.assessment_owner = assessment_owner
        self.total_score = total_score
        self.description = description
        self.effective_time = effective_time or datetime.now()
        self.deadline = deadline or date(9999, 12, 31)


class Student(Base):
    """docstring for Student."""
    __tablename__ = 'xakidzon_student'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    relationship = Column(SmallInteger)
    student_name = Column(String(64))
    register_date = Column(Date)
    student_birthday = Column(Date)
    student_gender = Column(SmallInteger)
    student_grade = Column(SmallInteger)
    student_school = Column(String(128))

    assessments = SQLRelationship(Assessment, secondary="xakidzon_student_assessment")

    def __init__(self, customer_id, relationship, student_name, register_date,
                 student_birthday, student_gender, student_grade, student_school, id=None):
        if id is not None:
            self.id = id
        self.customer_id = customer_id
        self.relationship = relationship
        self.student_name = student_name
        self.register_date = register_date
        self.student_birthday = student_birthday
        self.student_gender = student_gender
        self.student_grade = student_grade
        self.student_school = student_school


class WordQuestion(Base):
    __tablename__ = 'xakidzon_wordquestion'
    id = Column(Integer, primary_key=True)
    question_body = Column(String(1024))
    question_type = Column(String(64))
    question_factors = Column(SmallInteger)
    answer_formula = Column(String(128))

    def __str__(self):
        return eval(self.question_body)

    def get_question_instance(self):
        df = pd.read_csv('/home/aaron/projects_other/ejile/akidzon/templates/person_names.csv')
        rows = df.to_dict(orient='rows')
        picked_persons = random.sample(rows, 3)

        try:
            qb = eval(self.question_body)
        except Exception as e:
            qb = self.question_body
        for i, person in enumerate(picked_persons):
            for p in ['person_name', 'person_objective', 'person_possessive', 'person_subjective']:
                qb = qb.replace('{'+p+str(i+1)+'}', person[p])
        return qb
