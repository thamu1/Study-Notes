# Python Revision

---

## Core Python

* Interpreter vs Compiler
* Data Types - int, float, str, bool, complex, None
* Type Casting - int(), str(), list(), tuple(), set(), dict(), float(), bool()
* Operators - arithmetic, comparison, logical, bitwise, assignment, identity, membership
* mutable vs Immutable
* from <> import <>
* Conditions - if, elif, else, match
* Loop - for, while, break, continue, pass
* Functions - def, return, *args, **kwargs, func()(), lambda, Recursion
* Decorators - @staticmethod, @classmethod, @property, custom decorators
* try, except, finally, raise, custom exceptions
* Scope - Local, Global, Nonlocal, LEGB rule
* Pass by Value vs Pass by Reference
* Docstrings, comments, PEP 8
* Dataclasses - @dataclass, field(), __post_init__, frozen, slots, kw_only
* Type Hints - annotations, Optional, Union, List, Dict, Tuple, TypeVar, Generic, Protocol, Literal, TypedDict
* Context Managers - with, __enter__, __exit__, contextlib, @contextmanager, ExitStack

## Data Structures

* string - CRUD, slicing, indexing, methods, f-string, format(), strip(), split(), join(), replace(), upper(), lower()
* tuple - CRUD, immutable sequence, packing/unpacking
* list - CRUD, append, extend, insert, pop, remove, sort, reverse, slicing, list multiplication
* dict - CRUD, keys(), values(), items(), get(), setdefault(), update(), pop(), comprehension
* set - CRUD, union, intersection, difference, symmetric difference
* Comprehension - list, dict, tuple, set
    * [i**2 if i%2==0 else 'odd' for i in [1, 2, 3, 4]]
    * [j for i in range(3, 6) for j in range(1, 3)]
    * [i:i**2 if i%2==0 else 'odd' for i in [1, 2, 3, 4]]
* map(func, iterable), filter(func, iterable), reduce(func, iterable)
* any(boolean Iterable), all(boolean Iterable)
* zip, enumerate, sorted, reversed, slice notation
* shallow copy vs deep copy - copy.copy(), copy.deepcopy()
* Iterable vs Iterator vs Generator
* list/tuple/dict/set difference in memory and behavior
* defaultdict, Counter, deque, OrderedDict, ChainMap
* heapq, bisect, bisect_left, bisect_right
* pathlib.Path, PurePath, glob, rglob
* more-itertools patterns - chunking, sliding windows, unique_everseen

## Object-Oriented Programming

* Class - Attributes, methods, self, __init__
* Inheritance - super().__init__(), Class_name.__init__(self), multiple inheritance
* Polymorphism - Method Overloading (Not Allowed), Method Overriding
* Encapsulation - public, protected(_), private (__), Name Mangling :: obj_ClassName.__()
* Abstract - from abc import ABC, abstractmethod (@-decor over func)
* Staticmethod, Classmethod, Property
* __str__, __repr__, dunder methods
* __slots__
* MRO - Method Resolution Order
* Composition vs Inheritance
* __len__, __iter__, __next__, __getitem__, __setitem__, __contains__
* property(), setter, deleter, descriptors
* __enter__, __exit__, __aenter__, __aexit__
* dataclass vs regular class
* ABC vs Protocol
* mixins and duck typing

## Advanced Python Concepts

* Iterator, Iterable, Generator, Yield
* Closure, Nested Functions
* Lambda Functions
* Recursion, base case, recursion limit
* Exception Handling - try, except, else, finally
* Custom Exception Classes
* Memory Management - reference counting, GC, garbage collection
* Mutable default arguments issue
* Sequence unpacking - a, b, *rest = list
* Packing/Unpacking arguments - *args, **kwargs
* Sorting - key parameter, reverse=True
* Regular Expressions - re module, match, search, findall, split, sub
* String formatting - % formatting, f-string, format()
* Hashing, hashable objects
* __name__ == "__main__"
* Module vs Package
* Virtual Environment - venv, pip install, requirements.txt
* __all__ and package exports
* importlib, sys.path, relative vs absolute imports
* functools - lru_cache, wraps, partial, reduce
* itertools - product, permutations, combinations, cycle, tee, groupby
* contextlib - suppress, redirect_stdout, ExitStack
* walrus operator :=
* operator module, itemgetter, attrgetter
* weakref, weakref.WeakValueDictionary, finalizers
* `match`/`case` advanced pattern matching, guard clauses

## File Handling and I/O

* open(), read(), write(), append(), close()
* with open(...) as f:
* file modes - r, w, a, rb, wb, r+
* CSV, JSON, XML, Pickle
* os and pathlib modules
* working with directories - os.listdir(), os.getcwd(), os.path.join(), os.makedirs()
* encoding, newline handling
* pathlib.Path read_text(), write_text(), exists(), mkdir(), glob(), rglob()
* tempfile.NamedTemporaryFile, TemporaryDirectory
* shutil.copy2(), move(), rmtree()
* streaming reads and writes for large files
* atomic writes and file locking

## Built-in Functions and Modules

* Inbuilt Functions:
    * print, input, len, type, abs, range, reversed, enumerate, zip, help, sum, max, min, map, filter, all, any, sorted, bin, bool, ord, chr, eval, isinstance, super, __import__(), id, hash, round, complex, pow
* Modules
    * Numpy
    * Pandas
    * datetime -> date, datetime, timedelta, timezone, tz_info, time
    * requests -> get, post, put, urllib3
    * os -> getcwd, getenv, open, system, sys, path
    * smtplib -> SMTP_SSL
    * collections -> defaultdict, deque, Counter, namedtuple, ChainMap
    * heapq -> heapify, heappop, heappush, heappushpop, heapreplace, merge, nlargest, nsmallest
    * itertools -> combinations, permutations, product, cycle, tee, groupby
    * functools -> lru_cache, wraps, partial, total_ordering, singledispatch
    * dataclasses -> dataclass, field, asdict, astuple, replace
    * typing -> Optional, Union, List, Dict, Tuple, TypeVar, Generic, Protocol, Literal, TypedDict, Annotated, Final, ClassVar
    * contextlib -> contextmanager, asynccontextmanager, suppress, ExitStack, nullcontext
    * pathlib -> Path, PosixPath, PurePath, glob, rglob
    * subprocess -> run, Popen, check_output
    * math -> sqrt, floor, ceil, factorial, gcd, prod
    * random -> randint, choice, shuffle, sample
    * json -> loads, dumps, load, dump
    * re -> match, search, findall, split, sub, compile
    * logging -> logging.basicConfig(filename="app.log", encoding="utf-8", filemode="a", level=logging.WARNING, format="{asctime} - {levelname} - {message}", style="{")
        - logging.debug("This is a debug message (will not show if level is INFO)")
        - logging.info("The application has started successfully.")
        - logging.warning("Low disk space warning.")
        - logging.error("An error occurred while processing data.")
        - logging.critical("The system has crashed!")

## Concurrency and Async Programming

* Threading vs Multiprocessing
* GIL (Global Interpreter Lock)
* multithreading - Thread, Lock, RLock, Queue, Semaphore, Event
* multiprocessing - Process, Pool, Pipe, Manager, shared memory
* ThreadPoolExecutor, ProcessPoolExecutor
* async/await, coroutine
* Event Loop, asyncio module
* Future, Task, TaskGroup
* asyncio.create_task(), gather(), wait(), as_completed(), timeout(), shield()
* cancellation and exception propagation in async code
* Concurrency vs Parallelism
* deadlock, race condition, livelock, starvation
* thread safety and locks vs atomic operations

## Testing, Debugging and Best Practices

* Unit Testing, Integration Testing, Regression Testing
* pytest, unittest
* assert statement
* debugging - pdb, print debugging, breakpoints
* try/except/finally for error handling
* code readability, readability over cleverness
* time complexity and Big-O basics
* list vs set membership performance
* avoid repeated computation, optimize loops
* logging vs print for production debugging
* avoid broad except, preserve traceback, use custom exceptions
* prefer immutability, dataclasses, and clear naming over clever code
* use type hints and tests to reduce bugs in large codebases

## Interview Questions to Revise

* What is the difference between list, tuple, set, and dict?
* What is the difference between mutable and immutable objects?
* What is the difference between shallow copy and deep copy?
* What is the difference between iterator and iterable?
* What is a generator and when is it useful?
* What is the purpose of *args and **kwargs?
* What is the use of decorators in Python?
* What is the difference between classmethod and staticmethod?
* What is method overriding and method overloading in Python?
* How does Python handle memory management and garbage collection?
* What is the GIL and why does it matter?
* What is the difference between multiprocessing and multithreading?
* What is async/await and when would you use it?
* What is the difference between normal function and lambda function?
* What is the purpose of the with statement in file handling?
* What is the difference between deep copy and shallow copy?
* How do you handle exceptions in Python?
* What are list comprehension and dict comprehension?
* How does Python import modules and packages?
* What is a virtual environment and why is it important?
* What is a dataclass and when is it better than a normal class?
* What is the difference between a class variable and an instance variable?
* Why do we use `__slots__` and when can it help?
* What is the difference between Iterable, Iterator, and Generator?
* What is the difference between a list and a deque in Python?
* Why are type hints useful, and what is the difference between `Optional[T]` and `T | None`?
* What is the purpose of `contextlib` and `@contextmanager`?
* What is a race condition and how do locks prevent it?
* What is `TaskGroup` in asyncio and why is it safer than manually managing tasks?
* What is the difference between `threading` and `asyncio`?
* What is the difference between `map`, `filter`, and list comprehensions in real-world use?
* Why should we avoid mutable default arguments?
* What does `__all__` do in a package?

---
