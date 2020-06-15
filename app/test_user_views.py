import os
from unittest import TestCase
from .users.forms import EditUserForm

from .models import db, connect_db, User


# Import db


from app import create_app

app = create_app('TestConfig')

class UserViewTestCase(TestCase):
    """ Test views for users """

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

    def test_dashboard(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username
            res = c.get('/user', follow_redirects=True)

            self.assertEqual(res.status_code, 200 )
            self.assertIn("Currently Watching", str(res.data))

    def test_profile(self):   
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username

            res = c.get(f'/user/{self.testuser.username}/profile')    
            self.assertEqual(res.status_code, 200)
            self.assertIn('Info', str(res.data))     

    def test_edit_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.testuser.username

            res = c.get(f'/user/{self.testuser.username}/edit')    
            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit your profile', str(res.data))                 
            

    def test_no_login(self):
        with self.client as c: 
            res = c.get('/user', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Please login to view this page', str(res.data))
