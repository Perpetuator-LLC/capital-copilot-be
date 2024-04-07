# Run Tests

```shell
python manage.py test
```

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
