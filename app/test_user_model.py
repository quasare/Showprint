import os
from unittest import TestCase
from sqlalchemy import exc

from .models import db, connect_db, User


from app import create_app

app = create_app('TestConfig')


class UserViewTestCase(TestCase):
    """ Test model for users """

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        registerd = User.register("testuser", "password")
        self.testuser = User(username=registerd.username, password=registerd.password,
                             email='testuser@test.com', first_name='Test', last_name='user')
        db.session.add(self.testuser)
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model(self):
        u = User(username='test2', password='hased_pass',
                 email='testu2@test.com', first_name='Test2', last_name='user2')

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.shows), 0)

    def test_valid_register(self):
        registerd = User.register("testuser3", "password")
        testuser = User(username=registerd.username, password=registerd.password,
                        email='testuser3@test.com', first_name='Test', last_name='user')
        db.session.add(testuser)
        db.session.commit()

        u_test = User.query.get('testuser3')
        self.assertIsNotNone(testuser)
        self.assertEqual(u_test.username, "testuser3")
        self.assertEqual(u_test.email, "testuser3@test.com")
        self.assertNotEqual(u_test.password, "password")

        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username(self):
        testuser = User(username=None, password='fewfwefw',
                        email='testuser3@test.com', first_name='Test', last_name='user')
        db.session.add(testuser)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_valid_authentication(self):
        u = User.authenticate(self.testuser.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.username, self.testuser.username)      

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.testuser.username, "badpassword"))     
