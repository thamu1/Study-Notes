# Python Revision

---

## Core Python

* Interpreter vs Compiler
* Data Types
* Type Casting - int(), str(), list(), etc..
* Operators
* mutable vs Immutable
* from <> import <>
* Conditions - if, elif, else, match
* Loop - for, while
* Functions - *args, **kwargs, func()(), @Decorators, lambda x : Expression, Recursion
* try, except, finally, raise

## Data Structures

* string - CRUD, f'string', functions, f'{n:.2f}', f'{now: %d-%m-%y %H:%M:%S}'
* tuple - CRUD
* list - CURD, functions, []*n,
* dict - CURD, functions, dict(list(dict.items()).sort(key = lambda x: x[1]))
* set - CURD, functions
* Comprehension - list, dict, tuple, set
    * [i**2 if i%2==0 else 'odd' for i in [1, 2, 3, 4]]
    * [j for i in range(3, 6) for j in range(1, 3)]
    * [i:i**2 if i%2==0 else 'odd' for i in [1, 2, 3, 4]]
* map(func, iterable), filter(func, iterable), any(boolean Iterable), all(boolean Iterable)

## Object-Oriented Programming

* Class - Inheritance, Polymorphism, encapsulation, abstraction,
* Inheritance - super().__init__(), Class_name.__init__(self)
* Polymorphism - Method Overloading (Not Allowed), Method Overriding
* Encapsulation - public, protected(_), private (__), Name Mangling :: obj_ClassName.__()
* Abstract - from abc import ABC, abstractmethod (@-decor over func)

## Built-in Functions and Modules

* Inbuilt Functions:
    * print, input, len, type, abs, range, reversed, enumerate, zip, help, sum, max, min, map, filter, all, any, sorted, bin, bool, ord, chr, eval, isinstance, super, __import__()
* Modules
    * Numpy
    * Pandas
    * datetime -> date, datetime, timedelta, timezone, tz_info, time
    * requests -> get, post, put, urllib3,
    * os -> getcwd, getenv, open, system, sys,
    * smtplib -> SMTP_SSL,
    * collections -> defaultdict, deque, Counter
    * heapq -> heapify, heappop, heappush, heappushpop, heapreplace, merge, nlargest, nsmallest
    * itertools -> combinations, permutations
    * subprocess -> run, Popen
    * logging -> logging.basicConfig(filename="app.log", encoding="utf-8", filemode="a", level=logging.WARNING, format="{asctime} - {levelname} - {message}", style="{")
        - logging.debug("This is a debug message (will not show if level is INFO)")
        - logging.info("The application has started successfully.")
        - logging.warning("Low disk space warning.")
        - logging.error("An error occurred while processing data.")
        - logging.critical("The system has crashed!")



