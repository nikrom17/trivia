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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

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

    @app.route('/categories')
    def categories():
        selection = Category.query.all()
        categories = {category.id: category.format()
                      for category in selection}
        return jsonify({'categories': categories})

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

    @app.route('/questions')
    def questions():
        selection_question = Question.query.all()
        selection_category = Category.query.all()
        questions = [question.format() for question in selection_question]
        categories = {category.id: category.format()
                      for category in selection_category}
        return jsonify({
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
    @app.route('/questions/<question_id>/delete',  methods=['GET', 'DELETE'])
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

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions/create',  methods=['GET', 'POST'])
    def create_question():
        try:
            question = request.get_json()
            print(question)
            db.session.commit()
        except Exception as e:
            errorFlag = True
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'current_category': 'Sports',  # todo what should I return here?
            })

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search',  methods=['GET, POST'])
    def search_questions():
        search_term = request.get_json()
        print(search_term)
        search_results = Question.query.filter(
            func.lower(Question.question).like(func.lower(search_term)))
        print(search_results)
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    return app
