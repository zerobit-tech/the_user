from django.utils import timezone
from django.core.exceptions import ValidationError




from django.test import TestCase, TransactionTestCase


from ..models import *
 

"""
If you do something with the database in AppConfig.ready(), 
then during test runs it runs against the production db as it happens before django knows it's testing.
I don't think there's any way to change this, but it should be documented.



https://docs.djangoproject.com/en/1.11/topics/testing/tools/#provided-test-case-classes
"""
 
from django.test.utils import override_settings    
@override_settings(   )
class Test001(TestCase):
        multi_db = True
        databases = {'default', 'pci'}
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
        @classmethod
        def setUpTestData(cls):
            pass      


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------        
        def setUp(self):
            #print("setUp: Run once for every test method to setup clean data.")
            pass

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def tearDown(self):
            # Clean up run after every test method.
            pass
 