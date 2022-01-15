# Commerce

This project was inspired by [CS50 Web Programming with Python and JavaScript](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/).

[Full project specification](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

## Setup

The first thing to do is clone this repository:
```bash
git clone https://github.com/dark-dave007/cs50w-commerce
cd commerce
```

Install dependencies:
```bash
python3 -m pip install Django
```

Migrate:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

To run the development server:
```bash
python3 manage.py runserver
```

If you would like to create an admin user, run the following:
```bash
python3 manage.py createsuperuser
```
And follow the instructions given by Django.

### Details
The project I made is an e-commerce, ebay like website that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a watchlist.

This project was made using [Django](https://www.djangoproject.com/).

