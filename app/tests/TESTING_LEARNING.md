Testing provides sanity-checks for developers working in teams and when branches are merged it ensures existing functionality is not affected. (Key part of CI/CD processes)

# TDD ( Test Driven Development )
Writing tests before we write actual code, and then wring just enough code to make the test pass.

# Types of tests:
1. Unit Tests : focus on testing individual components or units of code. (e.g. single functions or method).
Goal : ensure each individual component works correct by itself.
Packages : unittest(Python), TestCase(Django)
2. Integration Tests : verify that multiple components of the app work together correctly. Involves combining units (functions,classe or modules) and testing them as a group to ensure they interact properly.
Packages : TestCase(Django)
3. End to End Tests: simulate a complete user journey, testing the entire flow of the application to ensure entire system behaves correctly from start to finish.
Packages : Django's LiveServerTestCase, Selenium, Cypress
4. Smoke Tests : basic tests on most crucial features on an application work, often after deployment
Packages : unittests, pytest, Selenium

# The unittest (Unit testing framework)
Django's test are built on top of and adds more utilities on top of it.
It supports object oriented concepts.
 
- Test fixture : preperation needed to perform one or more tests, any cleanup actions. (e.g. creating temporary proxy or data or starting a server process).
- TestCase : The individual unit of testing. Checks for a specific response to a particular set of inputs. 
- Test suite : A collection of test cases. Used to aggregate tests that should be executed together.
- Test runner : Component that orchestrates the execution of tests and provides outcome to the user. Could be a graphical interface, texture interface or return special value to indicate result of executing the tests.

# Assertions
Checks inside tests that verify your code behaves as expected.

Main assert methods:
1. Equality: self.assertEquality(a,b) a == b
2. True/False self.assertTrue(condition) self.assertFalse(condition) 
3. None self.assertIsNone(value) self.assertIsNotNone(value)
4. Exception testing:
< with self.assertRaises(ValidationError) >
example of :
< with self.assertRaises(ValidationError):
    validate_calories(5000) > 
Means this must raise ValidationError so because we cant have more than 1000 kcal then 5000 unit test will be true since it fails the test. If it doesnt raise a error then it will return False
5. Contains self.assertIn("pizza",list)

# Ways to run tests:
1. Run all tests < python manage.py tests >
2. One specific file < python manage.py test app.tests >
3. One specific file inside a tests folder < python manage.py test app.tests.test_validators > 
4. One specific class < python manage.py test app.tests.test_validators.RestaurantValidatorsTests.test_duplicate_restaurant_name_fails >

