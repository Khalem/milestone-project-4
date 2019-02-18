import unittest
import run
from flask import Flask, render_template, redirect, session, request, url_for, Blueprint
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "milestone-project-4"
app.config["MONGO_URI"] = "mongodb://admin:helloworld123@ds161894.mlab.com:61894/milestone-project-4"

mongo = PyMongo(app)

class test_run(unittest.TestCase):
    """
        Test suite for Milestone Project 4
    """
    
    def test_check_for_input(self):
        """
            Testing if check_for_input works as intended
        """
        
        self.assertNotEqual(run.check_for_input(False), False)
        self.assertEqual(run.check_for_input(False), {"$exists": True})
        self.assertEqual(run.check_for_input(""), {"$exists": True})
        self.assertEqual(run.check_for_input([]), {"$exists": True})
        self.assertEqual(run.check_for_input(["Test"]), {"$in": ["Test"]})
        self.assertEqual(run.check_for_input("Hello"), "Hello")
    
    def test_get_records(self):
        """
            Testing if get_records works as intended. Testing length of returned list to check that pagination works.
        """
        
        self.assertNotEqual(len(run.get_records(mongo.db.recipes.find(), 2, 1)), 5)
        self.assertEqual(len(run.get_records(mongo.db.recipes.find(), 5, 1)), 5)