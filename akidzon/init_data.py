from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from models import QuestionCategory, Question, Student, Assessment, Base, question_assessment_association
# db_string = "postgres://postgres:59kgbmtx@localhost:5432/akidzon"
db_string = 'mysql+pymysql://akidzon:59kgbmtx@localhost:3306/akidzon'

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
# session.execute('''CREATE ALGORITHM=UNDEFINED DEFINER=`akidzon`@`%` SQL SECURITY DEFINER VIEW `akidzon`.`xakidzon_assessment_questions_view`
# AS select `q_1`.`id` AS `question_id`,`q_1`.`interpretable_arguments` AS `interpretable_arguments`,`q_1`.`html_arguments` AS `html_arguments`,
# `q_1`.`question_type` AS `question_type`,`q_1`.`question_title` AS `question_title`,`q_1`.`standard_answers` AS `standard_answers`,
# `q_1`.`question_judge_method` AS `question_judge_method`,`qa_1`.`id` AS `question_assessment_id`,`qa_1`.`max_score` AS `max_score`,
# `qa_1`.`energy_point` AS `energy_point`,`qa_1`.`question_difficulty_level` AS `question_difficulty_level`,`aa`.`assessment_id` AS `assessment_id`,
# `q_1`.`category_id` AS `category_id`,`c`.`grade` AS `grade`,`c`.`subject` AS `subject`,`c`.`sub_subject` AS `sub_subject`,
# `c`.`letter_index` AS `letter_index`,`c`.`topic` AS `topic`,`c`.`skill` AS `skill`,`c`.`description` AS `description`,
# `aa`.`assessment_starttime` AS `assessment_starttime`,`aa`.`assessment_endtime` AS `assessment_endtime`,`aa`.`assessment_score` AS `assessment_score`,
# `aa`.`is_finished` AS `is_finished`,`aa`.`comments` AS `comments`,`aa`.`student_id` AS `student_id`,`qa`.`id` AS `answer_id`,
# `qa`.`answer_starttime` AS `answer_starttime`,`qa`.`answer_submittime` AS `answer_submittime`,`qa`.`user_answers` AS `user_answers`,
# `qa`.`score_earned` AS `question_score_earned`,`qa`.`is_correct` AS `is_correct`,`qa`.`teacher_comments` AS `teacher_comments`
# from ((((`akidzon`.`xakidzon_student_assessment` `aa` left join `akidzon`.`xakidzon_question_assessment` `qa_1`
# on((`aa`.`assessment_id` = `qa_1`.`assessment_id`))) left join `akidzon`.`xakidzon_question` `q_1` on((`qa_1`.`question_id` = `q_1`.`id`)))
# left join `akidzon`.`xakidzon_questioncategory` `c` on((`q_1`.`category_id` = `c`.`id`))) left join `akidzon`.`xakidzon_useranswer` `qa`
# on(((`qa`.`question_id` = `q_1`.`id`) and (`qa`.`student_id` = `aa`.`student_id`) and (`qa`.`assessment_id` = `aa`.`assessment_id`))));
# ''')