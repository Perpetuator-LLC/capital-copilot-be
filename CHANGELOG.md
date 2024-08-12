# Changelog from v0.3.0 to v0.4.0

In this new version, we have made significant improvements to our financial research web application. We have introduced
a new feature that adds Keltner Channels to our GraphQL API. This enhancement will provide users with more comprehensive
technical analysis of stock prices, particularly in relation to the Squeeze indicator.

## Enhancements

- Keltner Channels have been added to the GraphQL API. This feature will provide a more robust technical analysis of
  stock prices.

## Cleanups

- No cleanups were made in this version.

# Changelog from v0.2.0 to v0.3.0

In this new version, we have made significant improvements to our financial research web application. The most notable
enhancement is the addition of the squeeze data feature. This new feature will provide users with more comprehensive
technical analysis of stock prices.

## Enhancements

- Added squeeze data feature for improved technical analysis of stock prices.

## Cleanups

- No cleanups were performed in this version.

# Changelog from v0.1.0 to v0.2.0

This update brings a number of enhancements and cleanups to the project. The logging system has been changed to use
Django's system, and testing with coverage support has been added, aiming for over 90% coverage. The API now includes
data retrieval with authentication, new icons, an Insomnia profile, and documentation about Plotly and the frontend,
which has been switched to the Angular repository. The license has been switched from GPL v3 to MIT. Chart.js has been
removed in favor of Plotly, which is integrated with OpenBB.

## Enhancements

- Added a test to cover the GraphQL API Schema.
- Added an API to get data with authentication, new icons, an Insomnia profile, and documentation about Plotly and the
  frontend (now switched to Angular repo).
- Changed the logging system to use Django's and added testing with coverage support aiming for over 90% coverage.
- Added testing and coverage support.
- Added tests to pre-commit.
- Added logging support integrated from OpenBB.
- Removed Chart.js and switched to Plotly, which is integrated with OpenBB.

## Cleanups

- Switched the license in pyproject.toml to MIT per previous change.
- Added a test and catch removal of common_tags code where the copyright update removed that code.
- Switched to using the MIT license away from GPL v3. As the sole contributor, this conversion was approved and all of
  the code in this project is to be released as MIT.
