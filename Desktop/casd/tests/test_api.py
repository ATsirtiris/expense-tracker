

import unittest
import requests
import json
import os
from datetime import datetime, timedelta

# API base URL - can be overridden with environment variable
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5001')

class ExpenseTrackerAPITest(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a test user
        self.user_data = {
            'username': f'testuser_{datetime.now().timestamp()}',
            'email': f'test_{datetime.now().timestamp()}@example.com',
            'password': 'testpassword123'
        }
        
        # Create test user
        response = requests.post(
            f'{API_BASE_URL}/api/users',
            json=self.user_data
        )
        
        # Store user ID for tests
        if response.status_code == 201:
            self.user_id = response.json()['user']['id']
        else:
            raise Exception(f"Failed to create test user: {response.text}")
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = requests.get(f'{API_BASE_URL}/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')
    
    def test_metrics_endpoint(self):
        """Test the metrics endpoint."""
        response = requests.get(f'{API_BASE_URL}/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('http_requests_total' in response.text)
    
    def test_get_categories(self):
        """Test retrieving expense categories."""
        response = requests.get(f'{API_BASE_URL}/api/categories')
        self.assertEqual(response.status_code, 200)
        categories = response.json()['categories']
        self.assertTrue(len(categories) > 0)
        self.assertTrue('id' in categories[0])
        self.assertTrue('name' in categories[0])
    
    def test_expense_lifecycle(self):
        """Test creating, retrieving, updating, and deleting an expense."""
        # Create a new expense
        expense_data = {
            'user_id': self.user_id,
            'category_id': 1,  # Assuming Food category exists with ID 1
            'amount': 25.75,
            'description': 'Lunch at restaurant',
            'expense_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # 1. Create expense
        create_response = requests.post(
            f'{API_BASE_URL}/api/expenses',
            json=expense_data
        )
        self.assertEqual(create_response.status_code, 201)
        created_expense = create_response.json()['expense']
        expense_id = created_expense['id']
        
        # 2. Get the expense
        get_response = requests.get(f'{API_BASE_URL}/api/expenses/{expense_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()['expense']['id'], expense_id)
        
        # 3. Update the expense
        update_data = {
            'amount': 30.50,
            'description': 'Updated: Dinner at restaurant'
        }
        update_response = requests.put(
            f'{API_BASE_URL}/api/expenses/{expense_id}',
            json=update_data
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(float(update_response.json()['expense']['amount']), 30.5)
        self.assertEqual(update_response.json()['expense']['description'], 'Updated: Dinner at restaurant')
        
        # 4. Delete the expense
        delete_response = requests.delete(f'{API_BASE_URL}/api/expenses/{expense_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify deletion
        get_deleted_response = requests.get(f'{API_BASE_URL}/api/expenses/{expense_id}')
        self.assertEqual(get_deleted_response.status_code, 404)
    
    def test_get_expenses_by_category(self):
        """Test retrieving expenses by category."""
        # Create test expenses in two different categories
        for i, category_id in enumerate([1, 2]):  # Food and Entertainment
            expense_data = {
                'user_id': self.user_id,
                'category_id': category_id,
                'amount': 10.50 + i,
                'description': f'Test expense in category {category_id}',
                'expense_date': datetime.now().strftime('%Y-%m-%d')
            }
            requests.post(f'{API_BASE_URL}/api/expenses', json=expense_data)
        
        # Get expenses for category 1 (Food)
        response = requests.get(
            f'{API_BASE_URL}/api/expenses/by_category/1',
            params={'user_id': self.user_id}
        )
        self.assertEqual(response.status_code, 200)
        expenses = response.json()['expenses']
        self.assertTrue(len(expenses) > 0)
        for expense in expenses:
            self.assertEqual(expense['category_id'], 1)
            self.assertEqual(expense['user_id'], self.user_id)
    
    def test_expense_summary(self):
        """Test expense summary by category."""
        # Create test expenses in different categories
        categories = [1, 2, 3]  # Food, Entertainment, Transportation
        for i, category_id in enumerate(categories):
            for j in range(2):  # Create 2 expenses per category
                expense_data = {
                    'user_id': self.user_id,
                    'category_id': category_id,
                    'amount': 15.75 + i + j,
                    'description': f'Test expense {j} in category {category_id}',
                    'expense_date': datetime.now().strftime('%Y-%m-%d')
                }
                requests.post(f'{API_BASE_URL}/api/expenses', json=expense_data)
        
        # Get expense summary
        response = requests.get(
            f'{API_BASE_URL}/api/expenses/summary/by_category',
            params={'user_id': self.user_id}
        )
        self.assertEqual(response.status_code, 200)
        summary = response.json()['summary']
        
        # Verify summary contains entries for all categories
        category_ids = [item['category_id'] for item in summary]
        for category_id in categories:
            self.assertIn(category_id, category_ids)
        
        # Verify summary calculations
        for item in summary:
            if item['category_id'] in categories:
                self.assertEqual(item['transaction_count'], 2)  # 2 expenses per category
                self.assertTrue(item['total_amount'] > 0)

if __name__ == '__main__':
    unittest.main()