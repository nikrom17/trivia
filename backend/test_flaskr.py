import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

unittest.TestLoader.sortTestMethodsUsing = lambda self, a, b: (a > b) * -1


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], None)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_search_questions(self):
        res = self.client().get('/questions/search',
                                json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(data['current_category'], 'Science')

    def test_get_quiz_next_questions(self):
        res = self.client().get('/quizzes/next-question',
                                json={'quiz_category': {'id': 1, 'type': 'Science'}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['categories'])

    def test_delete_question(self):
        res = self.client().get('/questions/10/delete')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 18)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
