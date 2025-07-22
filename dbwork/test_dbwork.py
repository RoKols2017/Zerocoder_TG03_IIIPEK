import os
import unittest
from dbwork import db_create, db_add, db_select

test_db = 'test_school_data.db'

class TestDBWork(unittest.TestCase):
    def setUp(self):
        # Удаляем тестовую БД, если она есть
        if os.path.exists(test_db):
            os.remove(test_db)
        db_create(test_db)

    def tearDown(self):
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_add_and_select(self):
        # Добавляем ученика
        data = {'name': 'Иван', 'age': 15, 'grade': '9А'}
        self.assertTrue(db_add(test_db, 'students', data))
        # Проверяем выборку
        result = db_select(test_db, 'students')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Иван')
        self.assertEqual(result[0][2], 15)
        self.assertEqual(result[0][3], '9А')

    def test_select_with_condition(self):
        db_add(test_db, 'students', {'name': 'Петр', 'age': 14, 'grade': '8Б'})
        db_add(test_db, 'students', {'name': 'Анна', 'age': 13, 'grade': '7А'})
        result = db_select(test_db, 'students', {'grade': '8Б'})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Петр')

if __name__ == '__main__':
    unittest.main() 