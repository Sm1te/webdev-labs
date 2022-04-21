### 1. What is the value of SQLAlchemy?

SQLAlchemy is a library that facilitates the communication between Python programs and databases.

It is great because it provides a good connection / pooling infrastructure; a good Pythonic query building infrastructure; and then a good ORM infrastructure that is capable of complex queries and mappings.

Also it is a python abstraction which means users could use the same commands to implement their ideas in both PostgreSQL, SQLite, MySQL, or some other relational database.

### 2. What is a model?

Model is a class within the SQLAlchemy project, it makes it easier to use SQLAlchemy within a Flask application.

It stores the SQLAlchemy instance user create in application and it behaves like a regular Python class but has a query attribute attacted that can be used to query the model.

### 3. What is a view?

A Flask ModelView that makes it a bit easier to manage views for SQLAlchemy Declarative models. FlaskView and supports all Flask-Classy FlaskView functionality.

We can use it like tables in the database, it has functions like delete, get, post we could write.