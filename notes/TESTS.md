# Capturing data for Mocks

It is generally best for GraphQL data mocks to run the test without the mock and capture the data that is returned. Just
set a breakpoint in the schema and run the test. Then copy the data from the response and use it in the mock.

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

## Pre-Commit Setup

This project uses `pre-commit` to run the above tools before each commit. If we are not at a certain percentage of
coverage we can fail the commit, and a browser will open to show the coverage report. This is accomplished via the
`.pre-commit-config.yaml` file which contains:

```shell
coverage run --source='.' manage.py test && coverage html || (open htmlcov/index.html && false)
```

To run the pre-commit hooks manually, use the following command:

```shell
pre-commit run django-coverage
```
