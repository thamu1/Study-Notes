# SQL Revision

---

## SQL Fundamentals

* SQL - Structured Query Language; declarative: describe what data is needed, not how to fetch it
* Database vs DBMS vs RDBMS
* Schema, table, row/record, column/attribute, relation, view
* SQL command families:
    * DQL - `SELECT`
    * DML - `INSERT`, `UPDATE`, `DELETE`, `MERGE`
    * DDL - `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`
    * DCL - `GRANT`, `REVOKE`
    * TCL - `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION`
* SQL is case-insensitive for keywords; identifiers and string comparisons may be dialect/collation dependent
* Statement terminator `;`, comments `-- comment`, `/* block comment */`
* `NULL` means unknown/missing, not zero, empty string, or false
* Three-valued logic: `TRUE`, `FALSE`, `UNKNOWN`
* This revision uses two dialects: MySQL 8+ and BigQuery GoogleSQL
* Identifier quoting: MySQL uses backticks, for example `` `order` ``; BigQuery also uses backticks for table paths

## Data Types

* Numeric: `SMALLINT`, `INT`, `BIGINT`, `DECIMAL(p, s)`, `NUMERIC`, `FLOAT64`
* MySQL exact money type: `DECIMAL(p, s)`; BigQuery exact numeric type: `NUMERIC` or `BIGNUMERIC`
* Character: MySQL `CHAR`, `VARCHAR`, `TEXT`; BigQuery `STRING`
* MySQL date/time: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`; BigQuery: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`
* Boolean: MySQL `BOOLEAN` is treated as `TINYINT(1)`; BigQuery uses `BOOL`
* Binary: MySQL `BINARY`, `VARBINARY`, `BLOB`; BigQuery `BYTES`
* Semi-structured: MySQL `JSON`; BigQuery `JSON`, `ARRAY`, and `STRUCT`
* BigQuery also supports `GEOGRAPHY`; MySQL supports spatial types
* Precision and scale: `DECIMAL(10, 2)` allows 10 total digits and 2 fractional digits
* Choose the smallest safe type, but do not trade correctness for tiny storage savings
* Avoid storing comma-separated lists in one column; use a related table

## Database Design and Relationships

* Entity, attribute, relationship, cardinality: one-to-one, one-to-many, many-to-many
* Primary key (PK): unique row identity; one per table, can be composite
* Foreign key (FK): references a candidate/primary key in another table
* Candidate key, alternate key, natural key, surrogate key
* `UNIQUE` constraint: prevents duplicate non-null values; null behavior varies by database
* `NOT NULL`: value must exist
* `DEFAULT`: value used when a column is omitted, not generally when `NULL` is explicitly supplied
* `CHECK`: validates a row-level predicate; enforcement varies in older database versions
* Referential actions: `CASCADE`, `RESTRICT`, `NO ACTION`, `SET NULL`, `SET DEFAULT`
* Many-to-many relationship needs a junction/bridge table with two FKs
* Composite key: order matters for indexes and joins
* Normalize for integrity; denormalize deliberately for measured read performance

## Normalization

* Normalization means splitting data into sensible tables so that we do not repeat the same information unnecessarily
* Main goals: avoid duplicate data, prevent update mistakes, and keep data easy to insert/delete
* Example of a bad table:
    * `StudentID | StudentName | Course1 | Course2 | TeacherName`
    * Problems: multiple course columns, repeated teacher names, and difficulty adding a third course
* 1NF (First Normal Form): each cell contains one value; do not store lists or repeating columns
    * Bad: `StudentID | StudentName | Courses` -> `1 | Ravi | SQL, Python`
    * Better: one row per student-course: `1 | Ravi | SQL` and `1 | Ravi | Python`
* 2NF (Second Normal Form): first satisfy 1NF, then make sure every non-key column depends on the whole primary key
    * Example key: `(StudentID, CourseID)`
    * `StudentName` depends only on `StudentID`, so move it to `Students(StudentID, StudentName)`
    * Keep student-course data in `Enrollments(StudentID, CourseID, Mark)`
* 3NF (Third Normal Form): first satisfy 2NF, then non-key columns must not depend on another non-key column
    * Bad: `Courses(CourseID, CourseName, TeacherID, TeacherName)`
    * `TeacherName` depends on `TeacherID`, not directly on `CourseID`
    * Move it to `Teachers(TeacherID, TeacherName)` and keep `TeacherID` in `Courses`
* Easy memory rule: 1NF = one value per cell; 2NF = depends on the whole key; 3NF = depends only on the key
* Functional dependency: `A -> B` means knowing A tells us exactly which B belongs to it; example: `StudentID -> StudentName`
* Anomalies caused by poor design:
    * Insert anomaly: cannot add a teacher until a course exists
    * Update anomaly: teacher name must be changed in many rows
    * Delete anomaly: deleting the last course also deletes the teacher information
* BCNF, 4NF, and 5NF are advanced forms used for special dependency problems; learn 1NF to 3NF first for most interviews
* Normalization does not mean “make as many tables as possible”; split tables when it improves correctness, then join them with keys

## MySQL Essentials

* MySQL is usually used as an OLTP database: many small inserts/updates and application transactions
* Default storage engine for normal tables: InnoDB; it supports transactions, row locks, foreign keys, and crash recovery
* Create a database: `CREATE DATABASE app_db;` then select it with `USE app_db;`
* Common table definition:
    * `CREATE TABLE users (id BIGINT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE = InnoDB;`
* Auto-generated number: `AUTO_INCREMENT`; gaps are normal after failed inserts or rollbacks
* Upsert: `INSERT ... ON DUPLICATE KEY UPDATE ...`
* MySQL null-safe equality: `a <=> b`
* MySQL conditional helper: `IF(condition, true_value, false_value)`; portable option is `CASE`
* MySQL string concatenation: `CONCAT(first_name, ' ', last_name)`; `+` is numeric addition, not string concatenation
* MySQL date helpers: `NOW()`, `CURDATE()`, `DATE_ADD()`, `DATEDIFF()`, `TIMESTAMPDIFF()`
* MySQL JSON helpers: `JSON_EXTRACT()`, `JSON_SET()`, `JSON_OBJECT()`; exact syntax depends on the operation
* MySQL supports `FULL OUTER JOIN` neither directly nor with a single keyword; simulate it with matching left/right joins and `UNION ALL`
* MySQL supports `EXPLAIN`, `EXPLAIN ANALYZE`, indexes, stored procedures, triggers, and events
* Use `SHOW CREATE TABLE table_name;`, `SHOW INDEX FROM table_name;`, and `DESCRIBE table_name;` when inspecting a schema
* MySQL default isolation is commonly `REPEATABLE READ`; always verify the server configuration
* MySQL transaction example: `START TRANSACTION; ... COMMIT;` or `ROLLBACK;`

## BigQuery Essentials

* BigQuery is a serverless, columnar analytics warehouse: it is designed for large scans and aggregations, not frequent single-row transactions
* BigQuery table path: `` `project_id.dataset_name.table_name` ``
* BigQuery uses GoogleSQL; use backticks for table names and single quotes for string values
* BigQuery has no normal `USE database` flow; qualify tables with project and dataset when needed
* BigQuery table definition:
    * ``CREATE TABLE `project.dataset.users` (user_id INT64, email STRING, created_at TIMESTAMP);``
* BigQuery integer and floating types: `INT64`, `FLOAT64`; text type: `STRING`; boolean type: `BOOL`
* BigQuery exact numeric types: `NUMERIC`, `BIGNUMERIC`; timestamps are stored as instants in UTC
* BigQuery nested/repeated data: `STRUCT` stores a record and `ARRAY` stores multiple values
* Flatten an array with `UNNEST`: ``FROM `project.dataset.orders`, UNNEST(items) AS item``
* BigQuery has `QUALIFY` for filtering window-function results: `QUALIFY ROW_NUMBER() OVER (...) = 1`
* BigQuery supports `CREATE OR REPLACE TABLE`, `CREATE TABLE AS SELECT` (CTAS), views, materialized views, and temporary tables
* BigQuery supports `MERGE`, `INSERT`, `UPDATE`, and `DELETE`, but these are not a replacement for high-volume OLTP transactions
* BigQuery primary/foreign key constraints are generally `NOT ENFORCED`; do not assume the warehouse will prevent duplicates or invalid references
* BigQuery does not use traditional MySQL-style indexes; use partitioning, clustering, and good filters instead
* BigQuery table partitioning example: partition by `DATE(created_at)`; clustering example: `CLUSTER BY user_id, status`
* BigQuery partition filter: `WHERE created_at >= TIMESTAMP('2026-01-01')`; this can reduce bytes scanned when aligned with the partition
* BigQuery query cost depends mainly on bytes processed; select only required columns and avoid unnecessary full-table scans
* Preview cost with a dry run, inspect the query plan, and use `LIMIT` for output testing; `LIMIT` alone may not reduce bytes read
* BigQuery scripting supports variables, `IF`, loops, transactions, and temporary tables for multi-step jobs
* BigQuery time helpers: `CURRENT_DATE()`, `CURRENT_TIMESTAMP()`, `DATE_TRUNC()`, `TIMESTAMP_TRUNC()`, `DATE_DIFF()`
* BigQuery access is controlled through Google Cloud IAM, dataset/table permissions, authorized views, and row/column policies

## BigQuery Stored Procedures and Scripting

* A stored procedure is a named group of GoogleSQL statements saved inside a BigQuery dataset
* Use a procedure when you need several steps, variables, decisions, loops, temporary tables, or DML in one reusable routine
* A procedure is not the same as a function:
    * Procedure: called with `CALL`; can modify data and can return values through `OUT`/`INOUT` parameters or a result set from `SELECT`
    * SQL UDF/function: used inside `SELECT`; returns a value and cannot modify tables
* Basic structure:
    * ``CREATE OR REPLACE PROCEDURE `project.dataset.procedure_name`(parameters) BEGIN statements; END;``
    * Call it with ``CALL `project.dataset.procedure_name`(arguments);``
* Parameter modes:
    * Input parameter: write only `name STRING`; the procedure reads the value
    * `OUT` parameter: procedure writes a value back to the caller
    * `INOUT` parameter: procedure reads the starting value and writes a new value back
* Variables:
    * `DECLARE total NUMERIC DEFAULT 0;`
    * A variable without `DEFAULT` starts as `NULL`
    * `DECLARE` statements must appear at the start of the procedure or at the start of a `BEGIN` block
    * Change a variable with `SET total = total + 1;`
    * Assign multiple values with `SET (a, b) = (value_a, value_b);`
* Variable scope: a variable declared inside a block is available inside that block and nested blocks, but not outside it

### Complete Procedure Example

* This example demonstrates input, output values, variables, `IF`/`ELSEIF`/`ELSE`, a `WHILE` loop, and exception handling:

    ```sql
    CREATE OR REPLACE PROCEDURE `project.analytics.process_customer`(customer_id INT64, OUT message STRING, OUT loop_count INT64)
    BEGIN
      DECLARE customer_total NUMERIC DEFAULT 0;
      DECLARE customer_status STRING;
      DECLARE i INT64 DEFAULT 0;
      BEGIN
        SET (customer_status, customer_total) = (
          SELECT AS STRUCT status, COALESCE(total_spend, 0)
          FROM project.analytics.customers 
          WHERE id = customer_id LIMIT 1 
        );
        IF customer_status IS NULL THEN
          SET message = 'Customer was not found';
        ELSEIF customer_total >= 10000 THEN
          SET message = 'VIP customer';
        ELSEIF customer_total >= 1000 THEN
          SET message = 'Regular customer';
        ELSE
          SET message = 'New or low-spend customer';
        END IF;
        WHILE i < 3 DO
          SET i = i + 1;
        END WHILE;
        SET loop_count = i;
      EXCEPTION WHEN ERROR THEN
        SET message = CONCAT('Failed: ', @@error.message);
        SET loop_count = 0;
      END;
    END;
    ```
* Call the procedure and receive the output values:
    * `DECLARE output_message STRING;`
    * `DECLARE output_count INT64;`
    * ``CALL `project.analytics.process_customer`(101, output_message, output_count);``
    * `SELECT output_message, output_count;`
* `OUT` variables must be passed as variables, not literal values: use `output_message`, not `'some message'`
* The example catches the error and continues. Add `RAISE;` inside the exception handler when the caller must also receive the failure

### Conditions: IF, ELSEIF, ELSE

* Syntax:
    * `IF condition THEN statements;`
    * `ELSEIF another_condition THEN statements;`
    * `ELSE statements;`
    * `END IF;`
* BigQuery checks conditions from top to bottom and runs only the first true branch
* Always handle `NULL` deliberately; `IF amount > 0` is not true when `amount` is `NULL`
* `CASE` is useful when choosing a value; `IF` is useful when choosing a group of statements
* `CASE` expression: `SET label = CASE WHEN score >= 80 THEN 'A' ELSE 'Needs improvement' END;`

### Loops

* `WHILE`: checks the condition before each iteration
    * `WHILE counter < 10 DO SET counter = counter + 1; END WHILE;`
* `REPEAT`: runs at least once, then stops when the `UNTIL` condition becomes true
    * `REPEAT SET counter = counter + 1; UNTIL counter >= 10 END REPEAT;`
* `LOOP`: runs forever until `BREAK` or `LEAVE`
    * `LOOP SET counter = counter + 1; IF counter >= 10 THEN LEAVE; END IF; END LOOP;`
* `BREAK` and `LEAVE` stop the current loop completely:

    ```sql
    LOOP
      SET counter = counter + 1;
      IF counter = 5 THEN BREAK; END IF;
    END LOOP;
    ```

    * Here, the loop ends when `counter` becomes 5.
* `CONTINUE` and `ITERATE` skip the remaining statements in the current iteration and start the next iteration:

    ```sql
    SET counter = 0;
    WHILE counter < 5 DO
      SET counter = counter + 1;
      IF MOD(counter, 2) = 0 THEN CONTINUE; END IF;
      SELECT counter AS odd_number;
    END WHILE;
    ```
    
    * Output: `1`, `3`, `5`; even numbers are skipped.
* Combined example:

    ```sql
    LOOP
      SET counter = counter + 1;
      IF counter < 3 THEN CONTINUE; END IF;
      IF counter = 5 THEN BREAK; END IF;
      SELECT counter;
    END LOOP;
    ```

    * `CONTINUE` skips values 1 and 2; values 3 and 4 are processed; `BREAK` stops the loop at 5.
* `LEAVE` is a synonym for `BREAK`; `ITERATE` is a synonym for `CONTINUE`
* `FOR...IN` loops through rows returned by a query; the loop variable is a `STRUCT`:
    * `FOR row IN (SELECT id, email FROM customers ORDER BY id) DO`
    * `  SELECT row.id, row.email;`
    * `END FOR;`
* Add a label when nested loops need to exit or continue an outer loop: `outer_loop: LOOP ... LEAVE outer_loop; END LOOP;`
* Prefer one set-based `INSERT`, `UPDATE`, or `MERGE` over a row-by-row loop for large data; loops can be slower and create many child jobs

### Returning Values and Results

* A BigQuery procedure does not use `RETURNS data_type` like a function
* Use `OUT` for a value produced by the procedure:
    * `CREATE PROCEDURE dataset.get_count(OUT row_count INT64) BEGIN SET row_count = (SELECT COUNT(*) FROM dataset.table); END;`
    * `DECLARE count_value INT64; CALL dataset.get_count(count_value); SELECT count_value;`
* Use `INOUT` when the procedure receives a value and changes it:
    * `CREATE PROCEDURE dataset.add_bonus(INOUT amount NUMERIC) BEGIN SET amount = amount + 100; END;`
* Use `SELECT` when the procedure should return a result set to the caller:
    * `CREATE PROCEDURE dataset.list_active_users() BEGIN SELECT * FROM dataset.users WHERE active = TRUE; END;`
* `RETURN;` stops the current multi-statement script/procedure early; it does not return a value:
    * `IF input_id IS NULL THEN SET message = 'ID is required'; RETURN; END IF;`
* If you need a reusable scalar value inside a query, create a SQL UDF with `CREATE FUNCTION ... RETURNS ... AS (...)`

### Exception Handling

* Wrap risky statements in:
    * `BEGIN`
    * `  statements that may fail;`
    * `EXCEPTION WHEN ERROR THEN`
    * `  statements to handle the error;`
    * `END;`
* When an error occurs, BigQuery skips the rest of the `BEGIN` section and runs the exception handler
* Useful error variables:
    * `@@error.message`: readable error message
    * `@@error.statement_text`: statement that failed
    * `@@error.stack_trace`: structured call stack for debugging
    * `@@error.formatted_stack_trace`: readable stack trace for display
* Error messages may change; use `@@error.stack_trace` and `@@error.statement_text` for programmatic logging instead of parsing the message
* `RAISE;` inside an exception handler re-throws the original error and preserves its stack trace
* `RAISE USING MESSAGE = 'Custom error';` creates a custom error; use it for validation failures
* Variables declared inside the `BEGIN` section are not available in its exception handler; declare values needed by the handler before `BEGIN`
* If the exception handler itself fails, use an outer exception block to handle that second error

### Dynamic SQL and Transactions

* `EXECUTE IMMEDIATE` runs SQL created at runtime, for example when the table name is stored in a variable
* Pass values safely with `USING`; do not concatenate untrusted values into SQL:
    * ``EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM `project.analytics.customers` WHERE status = @s' INTO count_value USING 'ACTIVE' AS s;``
* `EXECUTE IMMEDIATE` can run a query, DDL, DML, or DCL statement, but it cannot dynamically execute control statements such as `IF` or `WHILE`
* BigQuery multi-statement transaction shape:
    * `BEGIN TRANSACTION;`
    * `  INSERT/UPDATE/DELETE/MERGE statements;`
    * `COMMIT TRANSACTION;`
    * In an exception handler, use `ROLLBACK TRANSACTION;`
* BigQuery transactions are for supported operations on BigQuery tables; they are not a replacement for MySQL-style high-volume OLTP transactions

### Procedure Design Rules and Limits

* Use `CREATE OR REPLACE PROCEDURE` for repeatable deployments; keep procedures in a dedicated routines dataset when appropriate
* Call a routine with `CALL`; calling a procedure introduces small overhead and each statement runs as a child job
* Use authorized routines when users should call a procedure without direct access to the underlying tables; configure IAM carefully
* BigQuery allows a maximum nesting level of 50 for blocks and conditional statements, and procedure call depth is limited to 50 frames
* Procedures are tied to dataset location; referenced tables and routines must be available in a compatible location
* Do not put a large row-by-row loop inside a procedure when a set-based query can do the work
* Log useful business context and error metadata, but do not expose sensitive values in error messages
* Test success, no matching row, `NULL` input, boundary values, DML failure, rollback behavior, and repeated calls
* Official references: [SQL stored procedures](https://docs.cloud.google.com/bigquery/docs/procedures), [GoogleSQL procedural language](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language), and [SQL UDFs](https://docs.cloud.google.com/bigquery/docs/user-defined-functions)

## DDL: Creating and Changing Objects

* MySQL: `CREATE DATABASE`, `CREATE TABLE`, `CREATE VIEW`, `CREATE INDEX`; BigQuery: datasets, tables, views, and partitioned/clustered tables
* `CREATE TABLE users (id BIGINT PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, created_at TIMESTAMP NOT NULL);`
* `CREATE TABLE orders (id BIGINT PRIMARY KEY, user_id BIGINT REFERENCES users(id), total DECIMAL(12, 2) CHECK (total >= 0));`
* MySQL: `ALTER TABLE ... ADD/MODIFY/ALTER/DROP COLUMN`; BigQuery supports `ALTER TABLE` but has different schema-change rules
* Add constraints with `CONSTRAINT constraint_name ...`
* `DROP TABLE`: removes table definition and data; dependency behavior varies
* `TRUNCATE TABLE`: removes all rows quickly, usually minimally logged, and has transaction/identity differences
* `DELETE FROM table`: row-level DML, supports `WHERE`, can usually be rolled back in a transaction
* `RENAME`, `COMMENT`, sequences, identity columns, generated/computed columns
* `IF EXISTS` and `IF NOT EXISTS` improve repeatable migrations where supported
* Never run destructive DDL in production without a backup, migration review, and rollback strategy

## SELECT Basics

* Basic shape: `SELECT columns FROM table WHERE condition ORDER BY column LIMIT n;`
* `SELECT *` is convenient for exploration but fragile and expensive in application code
* Aliases: `FROM users AS u`, `SELECT u.email AS user_email`
* Expressions: arithmetic, concatenation, `CASE`, casts, functions
* `DISTINCT` removes duplicate result rows; it is not a fix for an incorrect join
* `WHERE` filters rows before grouping
* `ORDER BY col ASC|DESC`; use a deterministic tie-breaker for pagination
* Pagination: MySQL uses `LIMIT 20 OFFSET 40`; BigQuery is better suited to bounded analytical results than deep application pagination
* SQL execution order (logical): `FROM/JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT/OFFSET`
* Physical execution order is chosen by the optimizer and may differ

## Filtering, NULL, and Operators

* Comparisons: `=`, `<>`/`!=`, `<`, `>`, `<=`, `>=`
* Boolean: `AND`, `OR`, `NOT`; parentheses remove ambiguity
* Range: `BETWEEN low AND high` is inclusive at both ends
* Set membership: `IN (...)`, `NOT IN (...)`
* Pattern matching: `LIKE 'A%'`, `LIKE '_a%'`; escape wildcard characters when needed
* Regular expressions are dialect-specific
* Null checks: `IS NULL`, `IS NOT NULL`; never use `= NULL`
* Null replacement: `COALESCE(a, b, 0)`; two-argument `COALESCE` equivalent is often `IFNULL`/`ISNULL`
* Null-safe equality: MySQL `<=>`; in BigQuery use explicit `IS NULL`/`IS NOT NULL` logic
* `NOT IN` with a `NULL` in its subquery can return no rows; prefer `NOT EXISTS`
* `WHERE` does not keep rows for which the predicate is `UNKNOWN`

## INSERT, UPDATE, DELETE, MERGE

* `INSERT INTO table (a, b) VALUES (1, 'x');`
* Insert multiple rows with multiple `VALUES` tuples
* `INSERT INTO target (...) SELECT ... FROM source ...`
* Upsert: MySQL `ON DUPLICATE KEY UPDATE`; BigQuery `MERGE`
* Always name insert columns; never depend on physical column order
* `UPDATE table SET value = ... WHERE id = ...`; missing `WHERE` updates every row
* `DELETE FROM table WHERE ...`; missing `WHERE` deletes every row
* Use a restrictive `SELECT` first with the same `WHERE` before `UPDATE`/`DELETE`
* For affected rows, use the MySQL client result or BigQuery job metadata; do not assume a `RETURNING` clause
* Batch large writes to reduce locks, log growth, and transaction duration

## Joins

* `INNER JOIN`: only matching rows
* `LEFT [OUTER] JOIN`: every left row plus matching right data, otherwise right columns are `NULL`
* `RIGHT JOIN`: reverse of left join; often rewritten as left join for readability
* `FULL OUTER JOIN`: matched and unmatched rows from both sides; not supported everywhere
* `CROSS JOIN`: Cartesian product; use intentionally
* Self join: table joined to itself, useful for hierarchies and comparisons
* Join condition belongs in `ON`; post-join filtering belongs in `WHERE` unless preserving unmatched rows matters
* `LEFT JOIN ... WHERE right.id IS NOT NULL` behaves like an inner join
* A one-to-many join multiplies parent rows; aggregate or use `EXISTS` when only existence is needed
* Join on compatible, indexed keys; avoid functions/casts on join columns when possible
* Never omit a join predicate accidentally: it creates a Cartesian product

## Aggregation and Grouping

* Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, standard deviation/variance by dialect
* `COUNT(*)` counts rows; `COUNT(column)` ignores nulls; `COUNT(DISTINCT column)` counts unique non-null values
* `GROUP BY` forms groups; every selected non-aggregate column normally must be grouped
* `HAVING` filters groups after aggregation; `WHERE` filters input rows before aggregation
* Conditional aggregation: `SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END)`
* `COUNT(CASE WHEN condition THEN 1 END)` counts matching rows
* `SUM`/`AVG` over no qualifying rows may return `NULL`; use `COALESCE` when appropriate
* Grouping by a unique key is different from grouping by a display name
* Avoid selecting columns not in `GROUP BY` unless the dialect explicitly and safely supports functional dependency

## Subqueries and Set Operations

* Scalar subquery: returns one value; multiple rows cause an error
* Correlated subquery: references the outer query and may execute conceptually once per outer row
* `EXISTS` checks whether at least one row exists and can short-circuit
* `NOT EXISTS` is usually safer than `NOT IN` when nulls are possible
* Derived table: subquery in `FROM`; must have an alias in many systems
* Common table expression (CTE): `WITH name AS (...) SELECT ...`
* Recursive CTE: `WITH RECURSIVE` for trees, graphs, sequences; include a termination condition
* CTE readability is valuable, but materialization/optimization differs by database and version
* `UNION` combines and removes duplicates; `UNION ALL` combines without deduplication and is usually faster
* `INTERSECT` returns common rows; `EXCEPT`/`MINUS` returns rows in the first query only
* Set operands need compatible column counts and compatible types; order is not guaranteed without `ORDER BY`

## Conditional and Built-in Functions

* Conditional: `CASE WHEN condition THEN value ELSE value END`, `NULLIF(a, b)`, `COALESCE(...)`
* String: `LOWER`, `UPPER`, `LENGTH`, `TRIM`, `SUBSTRING`, `REPLACE`, concatenation (`||` or `CONCAT`)
* Numeric: `ROUND`, `CEILING/CEIL`, `FLOOR`, `ABS`, `MOD`
* Date/time: current date/time, extract parts, add/subtract intervals, date difference; syntax is dialect-specific
* Conversion: both support `CAST(value AS type)`; MySQL also has `CONVERT`, while BigQuery has `SAFE_CAST`
* JSON functions and operators vary substantially by database
* Functions on indexed columns can prevent index seeks; consider expression/function-based indexes or computed columns
* Locale, collation, timezone, daylight-saving, and Unicode behavior must be explicit in critical systems

## Window Functions

* Window functions calculate across related rows without collapsing them
* Shape: `function(...) OVER (PARTITION BY ... ORDER BY ... [frame])`
* Ranking: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`
* Navigation: `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`
* Aggregates as windows: `SUM(amount) OVER (...)`, running totals, moving averages
* `ROW_NUMBER` has no ties; `RANK` leaves gaps after ties; `DENSE_RANK` does not
* Top row per group: rank within each partition, then filter in an outer query/CTE
* Window functions run after `WHERE`/`GROUP BY` logically; filter their result in a subquery or CTE
* Window `ORDER BY` does not order final output; add a final query `ORDER BY`
* Window frame (`ROWS` vs `RANGE`) changes running and peer-row behavior; specify it when correctness matters
* Running frame: `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; BigQuery interval frame syntax differs from MySQL, so verify before using `RANGE`

## Views, Temporary Objects, and Programmability

* View: stored query abstraction; ordinary views usually do not store result data
* Materialized/indexed view: stores or maintains results; refresh and write restrictions vary
* Temporary table: MySQL session-scoped table or BigQuery query/script-scoped table for intermediate data
* Temporary table vs CTE: choose based on reuse, statistics, indexing, scope, and optimizer behavior
* Stored procedure: callable server-side program; syntax and transaction behavior are dialect-specific
* Function: reusable expression, often with return value; deterministic/side-effect restrictions vary
* Trigger: runs automatically on insert/update/delete or other events; use sparingly because side effects are hidden
* Cursor: row-by-row processing; prefer set-based operations unless procedural logic is genuinely required
* MySQL `AUTO_INCREMENT` generates keys; BigQuery commonly uses application-generated IDs or UUIDs; generated IDs can have gaps

## Transactions and ACID

* MySQL transaction: logical unit of work; `START TRANSACTION`, statements, `COMMIT` or `ROLLBACK`
* BigQuery multi-statement transaction: supported for specific tables and operations; it is not the same as a MySQL long-running OLTP transaction
* ACID:
    * Atomicity: all operations succeed or none do
    * Consistency: constraints and invariants remain valid
    * Isolation: concurrent transactions appear controlled
    * Durability: committed data survives failure according to the engine's guarantees
* MySQL savepoints: `SAVEPOINT name`, `ROLLBACK TO SAVEPOINT name`, `RELEASE SAVEPOINT name`; do not assume the same behavior in BigQuery
* Autocommit: each statement may be its own transaction; know the driver/session setting
* Keep transactions short; do not hold locks while waiting for user input or network calls
* DDL transaction behavior differs by database
* Idempotency matters for retries: avoid duplicate side effects when a client repeats a request

## Isolation and Concurrency

* Read phenomena: dirty read, non-repeatable read, phantom read, lost update, write skew
* Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable
* Snapshot/MVCC isolation uses row versions in many systems; it does not remove every conflict
* MySQL pessimistic locking: `SELECT ... FOR UPDATE`; BigQuery is not designed around application row locks
* Optimistic concurrency: version/timestamp column checked in the update predicate
* MySQL uses row/key/table locks depending on the query and index; BigQuery uses a warehouse execution model rather than MySQL-style row locking
* Deadlock: transactions wait in a cycle; database aborts one transaction; retry safely
* Prevent deadlocks with consistent access order, short transactions, and suitable indexes
* Dirty reads are not “faster correct reads”; they can return impossible data
* Serializable gives the strongest standard isolation but may reduce concurrency

## Indexes

* MySQL index: an auxiliary B-tree structure that speeds reads but uses storage and slows writes
* MySQL composite index `(a, b, c)`: the leftmost-prefix rule commonly applies; column order matters
* MySQL covering index: contains all columns needed by a query, reducing table lookups
* MySQL indexes: primary, unique, normal, full-text, spatial, and prefix indexes
* MySQL foreign key columns often need indexes for joins and parent updates/deletes; InnoDB may create one when needed
* BigQuery does not use traditional indexes; it improves performance with partitioning and clustering
* BigQuery partitioning splits a table by date, timestamp, integer range, or ingestion time; filter the partition column
* BigQuery clustering sorts storage by up to four chosen columns; it helps when queries filter or group by those columns
* Indexes slow MySQL writes; partitioning and clustering affect BigQuery storage layout and query cost instead
* Do not add MySQL indexes or BigQuery partitions/clusters without measuring the workload

## Query Performance and Execution Plans

* MySQL: use `EXPLAIN` and `EXPLAIN ANALYZE`; BigQuery: use the query plan, job details, bytes processed, and dry-run estimate
* Read estimated vs actual rows, access method, join algorithm, sort/hash cost, memory, spills, and loops
* MySQL plan details: table scan, index scan/lookup, join order, rows examined, and temporary/filesort work
* BigQuery plan details: stages, shuffle, slot time, bytes read, and records written
* MySQL searchable predicate: `created_at >= '2026-01-01'` is usually better than `DATE(created_at) = ...`
* BigQuery partition pruning: filter the partition column directly instead of wrapping it in a function
* MySQL leading wildcard searches (`LIKE '%term'`) usually cannot use a normal B-tree index
* Both systems benefit from matching data types in predicates and joins
* Return only needed columns and rows; in BigQuery, avoid `SELECT *` because bytes processed matter
* Replace unnecessary `DISTINCT`, repeated correlated work, and accidental Cartesian joins
* Statistics/cardinality estimates guide the optimizer; stale statistics can produce poor plans
* Parameter sniffing/plan caching can help or hurt depending on data distribution and database
* Performance workflow: reproduce, measure baseline, inspect plan, make one change, measure again

## Security

* SQL injection: never concatenate untrusted input into SQL
* Use parameterized queries/prepared statements: `WHERE email = ?` or named parameters
* Stored procedures do not automatically prevent injection if they build dynamic SQL unsafely
* Dynamic identifiers cannot usually be bound as values; allow-list and safely quote them
* Principle of least privilege: separate read, write, migration, and administration roles
* `GRANT`, `REVOKE`, roles, schemas, row-level security, views for controlled access
* Do not expose database credentials in source code; rotate secrets and use secure configuration
* Encrypt connections; protect backups, logs, exports, and query parameters containing sensitive data
* Mask/tokenize sensitive data; apply retention and deletion requirements
* Audit privileged access and schema changes

## Common SQL Interview Patterns

* Second highest value: `DENSE_RANK` or a distinct ordered subquery; handle ties and fewer than two values
* Top N per group: `ROW_NUMBER()`/`DENSE_RANK()` partitioned by group
* Find duplicates: `GROUP BY columns HAVING COUNT(*) > 1`
* Remove duplicates: rank rows and delete where rank is greater than one; preserve the intended survivor
* Rows without a match: `NOT EXISTS` or left anti-join with `right.id IS NULL`
* Customers with all required items: relational division via grouped counts or double `NOT EXISTS`
* Consecutive dates/sequence gaps: `LAG`, `LEAD`, calendar table, or gaps-and-islands technique
* Gaps and islands: subtract a row number from an ordered value or use change flags and cumulative sums
* Running total: `SUM(value) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
* Latest row per entity: rank by timestamp and filter rank 1; add a unique tie-breaker
* Pivot rows to columns: conditional aggregation or dialect-specific `PIVOT`
* Unpivot columns to rows: `UNION ALL`, `UNPIVOT`, or JSON/table functions
* Compare periods: conditional aggregation, self join, `LAG`, or calendar table
* Recursive hierarchy: recursive CTE with anchor and recursive member
* Pagination: keyset using `(sort_key, id) > (?, ?)` is stable and scalable

## Data Quality and Operations

* Enforce invariants in the database with PK, FK, `NOT NULL`, `UNIQUE`, and `CHECK`
* Validate at application and database boundaries; application validation alone is not concurrency-safe
* Use UTC storage for instants and convert at the presentation boundary; distinguish date-only values
* Define collation and case-sensitivity requirements for identifiers and search
* Use migration tooling, versioned migrations, review, and tested rollback/forward-fix procedures
* Backups: full, incremental, point-in-time recovery; test restoration, not just backup creation
* Replication is not the same as backup
* Monitor slow queries, locks, deadlocks, failed jobs, connection pool use, storage, and replication lag
* Archive or partition large time-series tables based on measured access and maintenance needs
* Partition pruning only works when predicates align with the partition key and optimizer can recognize them
* Avoid N+1 queries; fetch in batches or use suitable joins/preloading

## SQL Tricks and Tips

* Start with a plain `SELECT`; add joins, filters, grouping, and windows one step at a time
* Qualify columns with aliases in joins to avoid ambiguity and accidental column changes
* Use half-open time ranges: `timestamp >= start AND timestamp < end`; safer for time precision and adjacent windows
* Use `UNION ALL` unless duplicate removal is required
* Prefer `EXISTS` when you only need to test presence, especially for one-to-many relationships
* Use `CASE` for portable conditional logic; do not rely on a database's non-standard boolean coercion
* Use explicit column lists in views, inserts, and production queries
* Never assume row order without a final `ORDER BY`
* Never assume `LIMIT`/`TOP` without ordering is deterministic
* Use `NULLIF(denominator, 0)` to avoid divide-by-zero, then decide how to represent the null result
* Use `COALESCE` deliberately; replacing unknown with zero can change business meaning
* Compare dates using typed parameters, not formatted strings
* For money, store fixed-point values and define rounding policy; avoid floating-point currency arithmetic
* Test empty input, duplicate values, nulls, ties, boundary dates, negative values, and very large data
* Check whether a fix changes semantics under concurrent writes, not only whether it works on sample data
* Prefer readable SQL; a slightly longer query is often easier to review and tune

## SQL Traps to Remember

* `NULL = NULL` is `UNKNOWN`; use `IS NULL`
* `NOT IN (subquery)` can fail unexpectedly when the subquery contains `NULL`
* `COUNT(column)` ignores nulls, while `COUNT(*)` does not
* `AVG` is affected by null exclusion and integer/decimal type rules
* `BETWEEN` is inclusive; it is risky for adjacent timestamp ranges
* Filtering the right table in `WHERE` after a `LEFT JOIN` can turn it into an inner join
* `WHERE` cannot normally reference a select-list alias; use a subquery/CTE or dialect feature
* Aggregate filters use `HAVING`, not `WHERE`
* `DISTINCT` hides duplicate rows caused by a bad join instead of fixing the join
* `UNION` sorts/deduplicates in many plans; `UNION ALL` usually avoids that cost
* Foreign keys do not automatically guarantee an index on the child column
* Indexes do not guarantee use; cost, statistics, selectivity, and query shape decide
* `TRUNCATE`, `DELETE`, and `DROP` have different logging, locking, identity, trigger, and rollback behavior by dialect
* Auto-generated IDs can have gaps after rollback or failed inserts
* `ORDER BY` inside a subquery/CTE does not guarantee outer order
* A query that is fast on ten rows may be slow at production scale
* Always verify syntax and behavior against the target database engine and version

## MySQL and BigQuery Quick Reference

* Table names: MySQL `database.table`; BigQuery `` `project.dataset.table` ``
* Limit rows: both use `LIMIT n`; BigQuery result ordering still requires a final `ORDER BY`
* String concatenation: both support `CONCAT(...)`; MySQL also has `CONCAT_WS(...)`
* Current time: MySQL `NOW()`; BigQuery `CURRENT_TIMESTAMP()`
* Auto-generated key: MySQL `AUTO_INCREMENT`; BigQuery usually uses an application-generated ID, UUID, or generated value in a load query
* Upsert: MySQL `INSERT ... ON DUPLICATE KEY UPDATE`; BigQuery `MERGE`
* JSON: MySQL JSON functions; BigQuery JSON functions plus `STRUCT`/`ARRAY` for typed nested data
* Performance: MySQL indexes and `EXPLAIN`; BigQuery partitioning, clustering, dry runs, and bytes processed
* Transactions: central to MySQL OLTP; limited and workload-specific in BigQuery
* Always state “MySQL” or “BigQuery GoogleSQL” when answering a syntax-specific interview question

