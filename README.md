# Technical test

## Background:

Our focus is on creating wedding lists for couples. In a simplified scenario a couple creates a wedding list and adds different types of products to that which become available to their wedding guests for purchase as a present. After the wedding the couple can create their order and decide which gifts to have delivered to them from all the guests’ purchases. Your task is to implement this scenario on a basic level.

## The challenge:

Write a program to the best of your knowledge which will allow the user to manage a single list of wedding gifts. 

The user must be able to:

- Add a gift to the list
- Remove a gift from the list
- List the already added gifts of the list 
- Purchase a gift from the list
- Generate a report from the list which will print out the gifts and their statuses.
  - The report must include two sections:
    - Purchased gifts: each purchased gift with their details.
    - Not purchased gifts: each available gift with their details.

You can find some provided products in the `products.json` file.

You can spend as much time as you wish to come up with a solution that you’re proud of. To pass the test, you won’t need to care about multiple users, multiple gift lists, data storage, authentication, or checkout. 

Think of this as an open source project in that sense that if you stumbled across it on a community such as GitHub, what would you want it to look like? The only requirement is that the solution is written in Python. Frameworks, or lack thereof, is entirely up to you.

_Hint: We’re looking for a high-quality submission with great application architecture, not a “just get it done”-like approach. Stay away from frameworks/boilerplates that handle everything for you, or use them only as a thin layer, so we can see how you structure applications yourself._

## Extra mile bonus points

- Application logging
- Containerisation
- Authentication
- API client documentation (for example swagger)
- Build script / CI
- Data storage
- Anything else you feel may benefit your solution from a technical perspective.

## What we will be assessing


| Area | Max score |
|----|----:|
| Functionality (does it work?) | 5 points|
| Code Quality |5 points|
| Solution Design |5 points|
| Problem Solving |5 points|
| Automated Tests |5 points|
|**Overall Score**|**25 points**|


Scoring algorithm:

```python

def have_you_passed_the_test(overall_score, bonus_points):
    if overall_score >= 19:
        return True
    elif overall_score > 16:
        return overall_score + bonus_points >= 19

    return False
```

## Improvements

Given more time, what improvements, if any, would you make to your code? Please include this in your repository.

## Submitting

When you’re ready to submit, upload the repository to Github and share it with us!

## Configuration
There are few dependencies to be installed as before running the application:
- Postgres
- WkhtmlToPDF
- Python libraries

In order to do this, here are the commands that will be required to have everything install and ready to be used.

```shell script
$ apt update
$ apt install postgresql-client
$ wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
$ tar xf  wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
$ cd ./wkhtmltox/bin/
$ sudo cp -R ./* /usr/bin/
$ wkhtmltopdf -V
$ pip install -r requirements.txt
```

Before you run the application, there is one environment variable that will need to be set up, `PSQL_DATABASE_URI`.
Example: `PSQL_DATABASE_URI=postgresql://localhost:5432/wedding_list`.

For demo/local purpose, it is recommended to run the tests locally as it will import the products JSON file.

## Postman
In this project there is a folder called "Postman" which contains a JSON file. It could be used to import current
API documentation for testing purposes.

## Next steps.
There are at least two important bits that were skipped due to lack of time:
- User portal -> Create the templates to run the same actions that can be done from the API documentation in a user
friendly website.
- Authentication -> Every single endpoint except by healthcheck should go to the authentication preprocessor,
checking both, valid token and access to the resource. In order to create the token, it was planned to use JWT getting
the signature from AWS Secrets Manager with daily rotation (using boto3 library for implementation and moto for tests).