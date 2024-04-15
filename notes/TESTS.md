# Run Tests

```shell
python manage.py test
python manage.py test users
python manage.py test users.tests_social_accounts
python manage.py test users.tests_social_accounts.AddSocialAccountTests
python manage.py test users.tests_social_accounts.AddSocialAccountTests.test_add_social_account_success
```

To run all tests in a specific file: ./manage.py test yourapp.tests.test_module To run a specific test case class:
./manage.py test yourapp.tests.test_module.YourTestClass To run a single test method: ./manage.py test
yourapp.tests.test_module.YourTestClass.test_method

# Run Tests with Coverage

In PyCharm can enable coverage via:

- Settings | Build, Execution, Deployment | Coverage
- Check the bundled coverage.py and set the path to the coverage.py in the virtual environment

Instead of that we install the package `coverage`.

Then we run the tests with coverage.\`

```shell
coverage run --source='.' manage.py test
coverage report
coverage html
```
