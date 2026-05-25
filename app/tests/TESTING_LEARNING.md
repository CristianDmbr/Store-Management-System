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
Django's test are built on top of.