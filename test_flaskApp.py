import unittest
from flask import Flask, session, jsonify, redirect, url_for
from unittest.mock import patch, MagicMock
from flaskApp import flaskApp 

class FlaskAppTests(unittest.TestCase):

    @patch('db_interface.find_events')
    @patch('db.get_categories_of_user')
    @patch('db.get_transactions_of_user')
    def test_landing_page_logged_in(self, mock_get_transactions, mock_get_categories, mock_find_events):
        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/')
            self.assertEqual(response.status_code, 302)

    def test_landing_page_not_logged_in(self):
        with flaskApp.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    @patch('my_auth.create_user')
    def test_signup_success(self, mock_create_user):
        mock_create_user.return_value = True
        with flaskApp.test_client() as client:
            response = client.post('/signup/', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertIn('signup_success', sess['_flashes'][0][1])

    @patch('my_auth.create_user')
    def test_signup_failure(self, mock_create_user):
        mock_create_user.return_value = False
        with flaskApp.test_client() as client:
            response = client.post('/signup/', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertIn('signup_error', sess['_flashes'][0][1])

    @patch('my_auth.login_user_from_form')
    def test_login_success(self, mock_login_user):
        mock_login_user.return_value = {'id': 1, 'username': 'testuser'}
        with flaskApp.test_client() as client:
            response = client.post('/login/', data={
                'username': 'testuser',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertEqual(sess['user_id'], 1)

    @patch('my_auth.login_user_from_form')
    def test_login_failure(self, mock_login_user):
        mock_login_user.return_value = None
        with flaskApp.test_client() as client:
            response = client.post('/login/', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertIn('login_error', sess['_flashes'][0][1])

    @patch('db_interface.find_events')
    def test_calendar_logged_in(self, mock_find_events):
        mock_find_events.return_value = []
        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/calendar/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('calendar.html', response.data.decode())

    @patch('db_interface.find_events')
    def test_calendar_not_logged_in(self, mock_find_events):
        with flaskApp.test_client() as client:
            response = client.get('/calendar/')
            self.assertEqual(response.status_code, 302)

    @patch('db.get_categories_of_user')
    @patch('db.get_transactions_of_user')
    @patch('suggestions.get_budget_tips')
    def test_tips(self, mock_get_budget_tips, mock_get_transactions, mock_get_categories):
        mock_get_categories.return_value = [{'ID': 1, 'name': 'Rent'}]
        mock_get_transactions.return_value = [{'category_id': 1, 'amount': '1000', 'title': 'Rent', 'expense': True}]
        mock_get_budget_tips.return_value = "Keep your rent within 30% of your income."

        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/tips/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Keep your rent within 30% of your income.', response.data.decode())

    @patch('db.save_user_budget')
    def test_budget_update(self, mock_save_user_budget):
        mock_save_user_budget.return_value = True
        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.post('/budget/', data={'total-budget': '5000'})
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertIn('Your budget has been updated!', sess['_flashes'][0][1])

    def test_logout(self):
        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/logout/')
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertNotIn('user_id', sess)

    @patch('db_interface.add_transaction')
    def test_add_event(self, mock_add_transaction):
        mock_add_transaction.return_value = True
        with flaskApp.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.post('/add_event/', data={
                'name': 'Test Event',
                'description': 'This is a test',
                'amount': '100',
                'category': 'test_category',
                'type': 'expense',
                'date': '2025-05-01'
            })
            self.assertEqual(response.status_code, 302)
            with client.session_transaction() as sess:
                self.assertIn('Event added successfully!', sess['_flashes'][0][1])

if __name__ == '__main__':
    unittest.main()