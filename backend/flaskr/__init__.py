import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def categories():
        selection = Category.query.all()
        categories = {category.id: category.format()
                      for category in selection}
        return jsonify({
            'success': True,
            'code': 200,
            'categories': categories
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def questions():
        selection_question = Question.query.all()
        selection_category = Category.query.all()
        questions = [question.format() for question in selection_question]
        categories = {category.id: category.format()
                      for category in selection_category}
        return jsonify({
            'success': True,
            'code': 200,
            'questions': questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': 'Sports',
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>/delete',  methods=['GET', 'DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).delete()
            selection_question = Question.query.all()
            selection_category = Category.query.all()
            questions = [question.format() for question in selection_question]
            categories = [category.format() for category in selection_category]
            db.session.commit()
        except Exception as e:
            errorFlag = True
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'code': 200,
                'questions': questions,
                'total_questions': len(questions),
                'categories': categories,
                'current_category': 'Sports',
            })

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the 'Add' tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the 'List' tab.
  '''
    @app.route('/questions/create',  methods=['GET', 'POST'])
    def create_question():
        try:
            new_question = request.get_json()
            question = Question(new_question['question'], new_question['answer'],
                                new_question['category'], new_question['difficulty'])
            db.session.add(question)
            db.session.commit()
        except Exception as e:
            print(e)
            errorFlag = True
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'code': 200,
                'current_category': 'Sports',  # todo what should I return here?
            })

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word 'title' to start.
  '''
    @app.route('/questions/search', methods=['GET', 'POST'])
    def search_questions():
        try:
            response = request.get_json()
            search_term_raw = response['searchTerm']
            search_term = '%{}%'.format(search_term_raw)
            search_results = Question.query.filter(
                func.lower(Question.question).like(func.lower(search_term))).all()
            questions = [question.format() for question in search_results]
        except Exception as e:
            print(e)
            errorFlag = True
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'code': 200,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': 'Sports',
            })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the 'List' tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        try:
            query_results = Question.query.filter(
                Question.category == category_id).all()
            questions = [question.format() for question in query_results]
            category = Category.query.get(category_id)

        except Exception as e:
            print(e)
            errorFlag = True
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category.type,
            })

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the 'Play' tab, after a user selects 'All' or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes/next-question', methods=['GET', 'POST'])
    def play_trivia():
        try:
            response = request.get_json()
            quiz_category = response.get('quiz_category')
            previous_questions = response.get('previous_questions')
            if quiz_category['id']:
                query = Question.query.filter(Question.category == quiz_category['id']).filter(
                    ~Question.id.in_(previous_questions))
            else:
                query = Question.query.filter(
                    ~Question.id.in_(previous_questions))
            query_results = query.all()
            questions = [question.format() for question in query_results]
            if len(questions):
                question = questions.pop()
            else:
                question = False
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True,
                'code': 200,
                'question': question,
            })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Server error'
        }), 500

    return app
