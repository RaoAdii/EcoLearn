"""
Quiz Engine for EcoLearn.
Handles quiz logic, question management, scoring, and streak tracking.
"""

import json
import random
from datetime import datetime
from database.db_setup import (
    Quiz,
    Question,
    Answer,
    QuizAttempt,
    Lesson,
    Course,
    User,
    Session,
)


class QuizEngine:
    """Main quiz engine for managing quizzes and scoring."""

    @staticmethod
    def _normalize_answer(answer: str) -> str:
        """Normalize answers for case-insensitive comparisons."""
        return (answer or '').strip().lower()

    @staticmethod
    def seed_sample_quizzes() -> dict:
        """Seed the database with beginner-friendly quizzes if they do not exist."""
        sample_quizzes = [
            {
                'title': 'Climate Change Basics',
                'description': 'Core concepts about global warming, causes, and solutions.',
                'passing_score': 70.0,
                'questions': [
                    {
                        'question_text': 'Which gas is the largest contributor to human-driven global warming?',
                        'question_type': 'multiple_choice',
                        'options': ['Carbon dioxide (CO2)', 'Nitrogen (N2)', 'Oxygen (O2)', 'Argon (Ar)'],
                        'correct_answer': 'Carbon dioxide (CO2)',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'True or False: Deforestation can increase atmospheric CO2 levels.',
                        'question_type': 'true_false',
                        'options': ['True', 'False'],
                        'correct_answer': 'True',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'What is the main goal of the Paris Agreement?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Limit global temperature rise to well below 2 degrees C',
                            'Ban all fossil fuels by 2030',
                            'Eliminate plastic waste globally',
                            'Stop all industrial activity',
                        ],
                        'correct_answer': 'Limit global temperature rise to well below 2 degrees C',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Which sector currently contributes the most global greenhouse gas emissions?',
                        'question_type': 'multiple_choice',
                        'options': ['Energy production', 'Libraries', 'Space exploration', 'Tourism brochures'],
                        'correct_answer': 'Energy production',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Which personal choice most directly helps reduce transport emissions?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Using public transport or cycling',
                            'Leaving devices on standby',
                            'Printing every document',
                            'Using more single-use plastics',
                        ],
                        'correct_answer': 'Using public transport or cycling',
                        'points': 1.0,
                    },
                ],
            },
            {
                'title': 'Biodiversity and Ecosystems',
                'description': 'Understand biodiversity, habitats, and ecosystem balance.',
                'passing_score': 70.0,
                'questions': [
                    {
                        'question_text': 'What does biodiversity refer to?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'The variety of life in an area',
                            'Only the number of trees',
                            'Only endangered species',
                            'Weather patterns in a region',
                        ],
                        'correct_answer': 'The variety of life in an area',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Why are pollinators like bees important?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'They help plants reproduce',
                            'They increase ocean salinity',
                            'They reduce rainfall',
                            'They make plastic biodegradable',
                        ],
                        'correct_answer': 'They help plants reproduce',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'True or False: Monoculture farming usually improves biodiversity.',
                        'question_type': 'true_false',
                        'options': ['True', 'False'],
                        'correct_answer': 'False',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'What is habitat fragmentation?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Breaking habitats into smaller isolated patches',
                            'Restoring damaged forests',
                            'A natural increase in species migration',
                            'The process of seed germination',
                        ],
                        'correct_answer': 'Breaking habitats into smaller isolated patches',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Which ecosystem service do mangroves provide for coastal areas?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Protection from storm surges and erosion',
                            'Increased use of fossil fuels',
                            'Faster glacier melting',
                            'Urban traffic control',
                        ],
                        'correct_answer': 'Protection from storm surges and erosion',
                        'points': 1.0,
                    },
                ],
            },
            {
                'title': 'Recycling and Waste Management',
                'description': 'Test your understanding of waste reduction and circular habits.',
                'passing_score': 70.0,
                'questions': [
                    {
                        'question_text': 'Which material can typically be recycled multiple times without losing quality?',
                        'question_type': 'multiple_choice',
                        'options': ['Aluminum', 'Styrofoam', 'Food waste', 'Ceramic tiles'],
                        'correct_answer': 'Aluminum',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'What is the first priority in the waste hierarchy?',
                        'question_type': 'multiple_choice',
                        'options': ['Reduce', 'Recycle', 'Incinerate', 'Landfill'],
                        'correct_answer': 'Reduce',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'True or False: Cleaning food containers before recycling can reduce contamination.',
                        'question_type': 'true_false',
                        'options': ['True', 'False'],
                        'correct_answer': 'True',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Composting is most suitable for which type of waste?',
                        'question_type': 'multiple_choice',
                        'options': ['Organic kitchen and garden waste', 'Glass bottles', 'Metal cans', 'Used batteries'],
                        'correct_answer': 'Organic kitchen and garden waste',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'How should e-waste such as old phones or chargers be handled?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Take to certified e-waste collection centers',
                            'Throw in regular trash',
                            'Burn in open air',
                            'Bury in soil',
                        ],
                        'correct_answer': 'Take to certified e-waste collection centers',
                        'points': 1.0,
                    },
                ],
            },
            {
                'title': 'Renewable Energy Essentials',
                'description': 'Learn how renewable technologies generate cleaner power.',
                'passing_score': 70.0,
                'questions': [
                    {
                        'question_text': 'How do solar photovoltaic panels generate electricity?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'By converting sunlight directly into electricity',
                            'By burning coal under panels',
                            'By using only moonlight',
                            'By storing wind in batteries',
                        ],
                        'correct_answer': 'By converting sunlight directly into electricity',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'True or False: Wind turbines capture kinetic energy from moving air.',
                        'question_type': 'true_false',
                        'options': ['True', 'False'],
                        'correct_answer': 'True',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Which of these is a renewable energy source?',
                        'question_type': 'multiple_choice',
                        'options': ['Geothermal energy', 'Diesel fuel', 'Coal gasification', 'Petrol generators'],
                        'correct_answer': 'Geothermal energy',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'Why is battery storage useful in renewable energy systems?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'It stores excess energy for later use',
                            'It increases carbon emissions',
                            'It blocks sunlight from solar farms',
                            'It replaces transmission lines entirely',
                        ],
                        'correct_answer': 'It stores excess energy for later use',
                        'points': 1.0,
                    },
                    {
                        'question_text': 'What is a key benefit of rooftop solar for households?',
                        'question_type': 'multiple_choice',
                        'options': [
                            'Lower grid electricity use and bills',
                            'Guaranteed 24/7 peak generation',
                            'No maintenance required forever',
                            'Higher fossil fuel dependence',
                        ],
                        'correct_answer': 'Lower grid electricity use and bills',
                        'points': 1.0,
                    },
                ],
            },
        ]

        session = Session()
        try:
            seed_teacher = session.query(User).filter(
                User.username == 'ecolearn_system_teacher'
            ).first()
            if not seed_teacher:
                seed_teacher = User(
                    username='ecolearn_system_teacher',
                    email='ecolearn_system_teacher@local',
                    password_hash='seeded_system_account',
                    role='teacher',
                    first_name='EcoLearn',
                    last_name='System',
                    is_active=False,
                )
                session.add(seed_teacher)
                session.flush()

            starter_course = session.query(Course).filter(
                Course.title == 'EcoLearn Starter Course'
            ).first()
            if not starter_course:
                starter_course = Course(
                    title='EcoLearn Starter Course',
                    description='Starter content with foundational environmental quizzes.',
                    instructor_id=seed_teacher.id,
                    category='Sustainability',
                    difficulty_level='beginner',
                    is_published=True,
                )
                session.add(starter_course)
                session.flush()

            quiz_lesson = session.query(Lesson).filter(
                Lesson.course_id == starter_course.id,
                Lesson.title == 'Environmental Foundations Quiz Pack',
            ).first()
            if not quiz_lesson:
                quiz_lesson = Lesson(
                    course_id=starter_course.id,
                    title='Environmental Foundations Quiz Pack',
                    content='Practice quizzes for climate, biodiversity, recycling, and renewable energy.',
                    order=1,
                    duration_minutes=30,
                    is_published=True,
                )
                session.add(quiz_lesson)
                session.flush()

            added_quizzes = 0
            added_questions = 0

            for quiz_data in sample_quizzes:
                quiz = session.query(Quiz).filter(
                    Quiz.lesson_id == quiz_lesson.id,
                    Quiz.title == quiz_data['title'],
                ).first()

                if not quiz:
                    quiz = Quiz(
                        lesson_id=quiz_lesson.id,
                        title=quiz_data['title'],
                        description=quiz_data['description'],
                        passing_score=quiz_data['passing_score'],
                        is_published=True,
                    )
                    session.add(quiz)
                    session.flush()
                    added_quizzes += 1
                elif not quiz.is_published:
                    quiz.is_published = True

                existing_questions = session.query(Question).filter(
                    Question.quiz_id == quiz.id
                ).order_by(Question.order).all()
                existing_texts = {question.question_text for question in existing_questions}
                next_order = len(existing_questions) + 1

                for question_data in quiz_data['questions']:
                    if question_data['question_text'] in existing_texts:
                        continue

                    question = Question(
                        quiz_id=quiz.id,
                        question_text=question_data['question_text'],
                        question_type=question_data['question_type'],
                        options=json.dumps(question_data['options']),
                        correct_answer=question_data['correct_answer'],
                        order=next_order,
                        points=question_data['points'],
                    )
                    session.add(question)
                    next_order += 1
                    added_questions += 1

            session.commit()

            return {
                'success': True,
                'added_quizzes': added_quizzes,
                'added_questions': added_questions,
            }

        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': f'Failed to seed sample quizzes: {str(e)}',
            }

        finally:
            session.close()
    
    @staticmethod
    def create_quiz(lesson_id: int, title: str, description: str = '', 
                   passing_score: float = 70.0) -> dict:
        """
        Create a new quiz.
        
        Args:
            lesson_id: Parent lesson ID
            title: Quiz title
            description: Quiz description
            passing_score: Minimum percentage to pass
            
        Returns:
            Dictionary with success status and quiz data
        """
        session = Session()
        try:
            quiz = Quiz(
                lesson_id=lesson_id,
                title=title,
                description=description,
                passing_score=passing_score,
                is_published=False
            )
            session.add(quiz)
            session.commit()
            
            return {
                'success': True,
                'message': 'Quiz created successfully',
                'quiz_id': quiz.id
            }
        
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to create quiz: {str(e)}'}
        
        finally:
            session.close()
    
    @staticmethod
    def add_question(quiz_id: int, question_text: str, question_type: str,
                    options: list, correct_answer: str, points: float = 1.0) -> dict:
        """
        Add a question to a quiz.
        
        Args:
            quiz_id: Parent quiz ID
            question_text: The question text
            question_type: Type of question (multiple_choice, true_false, short_answer)
            options: List of answer options (JSON format)
            correct_answer: The correct answer
            points: Points for this question
            
        Returns:
            Dictionary with success status
        """
        session = Session()
        try:
            # Get the next order number
            last_question = session.query(Question).filter(
                Question.quiz_id == quiz_id
            ).order_by(Question.order.desc()).first()
            
            next_order = (last_question.order + 1) if last_question else 1
            
            question = Question(
                quiz_id=quiz_id,
                question_text=question_text,
                question_type=question_type,
                options=json.dumps(options) if isinstance(options, list) else options,
                correct_answer=correct_answer,
                order=next_order,
                points=points
            )
            
            session.add(question)
            session.commit()
            
            return {
                'success': True,
                'message': 'Question added successfully',
                'question_id': question.id
            }
        
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to add question: {str(e)}'}
        
        finally:
            session.close()
    
    @staticmethod
    def get_quiz_questions(quiz_id: int) -> dict:
        """Get all questions for a quiz."""
        session = Session()
        try:
            quiz = session.query(Quiz).filter(Quiz.id == quiz_id).first()
            
            if not quiz:
                return {'success': False, 'message': 'Quiz not found'}
            
            questions = session.query(Question).filter(
                Question.quiz_id == quiz_id
            ).order_by(Question.order).all()
            
            questions_data = []
            for q in questions:
                questions_data.append({
                    'id': q.id,
                    'question_text': q.question_text,
                    'question_type': q.question_type,
                    'options': json.loads(q.options) if q.options else [],
                    'points': q.points,
                    'order': q.order
                })
            
            return {
                'success': True,
                'quiz': {
                    'id': quiz.id,
                    'title': quiz.title,
                    'description': quiz.description,
                    'passing_score': quiz.passing_score
                },
                'questions': questions_data
            }
        
        finally:
            session.close()

    @staticmethod
    def get_available_quizzes() -> dict:
        """Get all published quizzes that have at least one question."""
        session = Session()
        try:
            quizzes = session.query(Quiz).filter(
                Quiz.is_published == True
            ).order_by(Quiz.created_at.desc()).all()

            quizzes_data = []
            for quiz in quizzes:
                question_count = session.query(Question).filter(
                    Question.quiz_id == quiz.id
                ).count()

                if question_count == 0:
                    continue

                quizzes_data.append({
                    'id': quiz.id,
                    'title': quiz.title,
                    'description': quiz.description,
                    'passing_score': quiz.passing_score,
                    'question_count': question_count,
                })

            return {'success': True, 'quizzes': quizzes_data}

        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to fetch quizzes: {str(e)}',
                'quizzes': [],
            }

        finally:
            session.close()

    @staticmethod
    def submit_quiz(user_id: int, quiz_id: int, answers: dict, time_spent_seconds: int) -> dict:
        """Submit an entire quiz attempt in one transaction."""
        session = Session()
        try:
            quiz = session.query(Quiz).filter(Quiz.id == quiz_id).first()
            if not quiz:
                return {'success': False, 'message': 'Quiz not found'}

            questions = session.query(Question).filter(
                Question.quiz_id == quiz_id
            ).order_by(Question.order).all()

            if not questions:
                return {'success': False, 'message': 'Quiz has no questions'}

            attempt = QuizAttempt(
                user_id=user_id,
                quiz_id=quiz_id,
                started_at=datetime.utcnow(),
            )
            session.add(attempt)
            session.flush()

            total_possible_points = sum(question.points for question in questions)
            total_points_earned = 0.0
            correct_count = 0
            question_breakdown = []

            for question in questions:
                raw_answer = answers.get(question.id, answers.get(str(question.id), ''))
                user_answer = raw_answer if isinstance(raw_answer, str) else str(raw_answer or '')

                is_correct = (
                    QuizEngine._normalize_answer(user_answer)
                    == QuizEngine._normalize_answer(question.correct_answer)
                )

                awarded_score = question.points if is_correct else 0.0
                total_points_earned += awarded_score
                correct_count += 1 if is_correct else 0

                answer = Answer(
                    question_id=question.id,
                    quiz_attempt_id=attempt.id,
                    user_answer=user_answer,
                    is_correct=is_correct,
                    score=awarded_score,
                )
                session.add(answer)

                question_breakdown.append({
                    'question_id': question.id,
                    'question_text': question.question_text,
                    'user_answer': user_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': is_correct,
                })

            score_percentage = (
                (total_points_earned / total_possible_points) * 100
                if total_possible_points > 0 else 0
            )
            passed = score_percentage >= quiz.passing_score

            attempt.score = score_percentage
            attempt.passed = passed
            attempt.completed_at = datetime.utcnow()
            attempt.time_spent_seconds = max(int(time_spent_seconds), 0)

            session.commit()

            return {
                'success': True,
                'attempt_id': attempt.id,
                'score': round(score_percentage, 2),
                'passed': passed,
                'correct_answers': correct_count,
                'total_questions': len(questions),
                'time_spent': max(int(time_spent_seconds), 0),
                'question_breakdown': question_breakdown,
            }

        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to submit quiz: {str(e)}'}

        finally:
            session.close()
    
    @staticmethod
    def start_quiz_attempt(user_id: int, quiz_id: int) -> dict:
        """Start a new quiz attempt."""
        session = Session()
        try:
            attempt = QuizAttempt(
                user_id=user_id,
                quiz_id=quiz_id,
                started_at=datetime.utcnow()
            )
            session.add(attempt)
            session.commit()
            
            return {
                'success': True,
                'attempt_id': attempt.id,
                'started_at': attempt.started_at.isoformat()
            }
        
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to start quiz: {str(e)}'}
        
        finally:
            session.close()
    
    @staticmethod
    def submit_answer(attempt_id: int, question_id: int, user_answer: str, 
                     is_correct: bool, score: float = 0.0) -> dict:
        """Record a user's answer to a question."""
        session = Session()
        try:
            answer = Answer(
                question_id=question_id,
                quiz_attempt_id=attempt_id,
                user_answer=user_answer,
                is_correct=is_correct,
                score=score if is_correct else 0.0
            )
            session.add(answer)
            session.commit()
            
            return {
                'success': True,
                'answer_id': answer.id,
                'score': score if is_correct else 0.0
            }
        
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to submit answer: {str(e)}'}
        
        finally:
            session.close()
    
    @staticmethod
    def finish_quiz_attempt(attempt_id: int, time_spent_seconds: int) -> dict:
        """Finalize a quiz attempt and calculate score."""
        session = Session()
        try:
            attempt = session.query(QuizAttempt).filter(
                QuizAttempt.id == attempt_id
            ).first()
            
            if not attempt:
                return {'success': False, 'message': 'Quiz attempt not found'}
            
            # Get all answers for this attempt
            answers = session.query(Answer).filter(
                Answer.quiz_attempt_id == attempt_id
            ).all()
            
            # Calculate total score
            total_points_earned = sum(a.score for a in answers)
            
            # Get total possible points
            questions = session.query(Question).filter(
                Question.quiz_id == attempt.quiz_id
            ).all()
            total_possible_points = sum(q.points for q in questions)
            
            # Calculate percentage score
            score_percentage = (total_points_earned / total_possible_points * 100) if total_possible_points > 0 else 0
            
            # Check if passed
            quiz = session.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
            passed = score_percentage >= quiz.passing_score
            
            # Update attempt
            attempt.score = score_percentage
            attempt.passed = passed
            attempt.completed_at = datetime.utcnow()
            attempt.time_spent_seconds = time_spent_seconds
            
            session.commit()
            
            return {
                'success': True,
                'attempt_id': attempt_id,
                'score': round(score_percentage, 2),
                'passed': passed,
                'time_spent': time_spent_seconds,
                'total_questions': len(questions)
            }
        
        except Exception as e:
            session.rollback()
            return {'success': False, 'message': f'Failed to complete quiz: {str(e)}'}
        
        finally:
            session.close()
    
    @staticmethod
    def get_user_quiz_stats(user_id: int) -> dict:
        """Get user's quiz statistics."""
        session = Session()
        try:
            attempts = session.query(QuizAttempt).filter(
                QuizAttempt.user_id == user_id
            ).all()
            
            if not attempts:
                return {
                    'success': True,
                    'total_attempts': 0,
                    'average_score': 0,
                    'total_passed': 0,
                    'quiz_attempts': []
                }
            
            total_attempts = len(attempts)
            total_passed = sum(1 for a in attempts if a.passed)
            average_score = sum(a.score for a in attempts if a.score is not None) / total_attempts if total_attempts > 0 else 0
            
            attempts_data = []
            for attempt in attempts:
                quiz = session.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
                attempts_data.append({
                    'quiz_id': attempt.quiz_id,
                    'quiz_title': quiz.title if quiz else 'Unknown',
                    'score': attempt.score,
                    'passed': attempt.passed,
                    'completed_at': attempt.completed_at.isoformat() if attempt.completed_at else None,
                    'time_spent': attempt.time_spent_seconds
                })
            
            return {
                'success': True,
                'total_attempts': total_attempts,
                'average_score': round(average_score, 2),
                'total_passed': total_passed,
                'quiz_attempts': attempts_data
            }
        
        finally:
            session.close()


class QuestionBank:
    """Manages the question database and filtering."""
    
    @staticmethod
    def get_questions_by_category(category: str, difficulty: str = None) -> list:
        """Get questions filtered by category and optionally difficulty."""
        session = Session()
        try:
            # This is a placeholder - would need to extend Question model with category/difficulty
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_random_questions(quiz_id: int, count: int = 10) -> list:
        """Get random questions from a quiz."""
        session = Session()
        try:
            questions = session.query(Question).filter(
                Question.quiz_id == quiz_id
            ).all()
            
            return random.sample(questions, min(count, len(questions)))
        
        finally:
            session.close()
