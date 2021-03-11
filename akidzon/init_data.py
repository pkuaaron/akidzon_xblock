from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from models import QuestionCategory, Question, Student, Assessment, Base, question_assessment_association
# db_string = "postgres://postgres:59kgbmtx@localhost:5432/akidzon"
db_string = 'mysql+pymysql://akidzon:59kgbmtx@34.226.11.227:3306/akidzon'

engine = create_engine(db_string)

# engine = create_engine(db_string)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
#
# result_set = postgre_engine.execute('''select a.*, case when a.has_implemented is true then 1 else 0 end as has_implemented1 from xakidzon_questioncategory as a''')
session = sessionmaker(bind=engine)()
#
# for r in result_set:
#     q=QuestionCategory(r.grade, r.subject, r.sub_subject, r.letter_index, r.topic, r.skill, r.description, id=r.id, has_implemented=r.has_implemented1)
#     session.add(q)
# # # for r in result_set:
# # # print(r.interpretable_arguments)
# s = Student(1, 0, 'Isaac Chen', date(2021, 1, 15), date(2013, 4, 15), 0, 2, 'Elon Park Elementary School')
# # # 10 - commit and close session
# #
# a = Assessment(0, total_score=100, description='Assessment example', effective_time=None, deadline=None)
# # p = session.query(Question).first()
#
# # a.questions = [p]
# session.add(a)
#
# s.assessments = [a]
# session.add(s)
# session.commit()
# session.close()
