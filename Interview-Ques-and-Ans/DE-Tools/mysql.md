
# Stored Procedure:

```sql

-- Basic Structure --

DELIMITER $$

create or replace procedure <procedure-name> ([IN | OUT | INOUT] parameter_name datatype[(length)])
BEGIN
  sql_statement_list
EXCEPTION WHEN ERROR THEN
  sql_statement_list :: SELECT @@error.message, @@error.statement_text, @@error.formatted_stack_trace
END $$

DELIMITER

;


CALL <procedure-name>();

-- Eg: 
CALL GetOrderCountByStatus('Shipped',@total);
SELECT @total;



-- Variable Declaration and setting --

declare <var> <data-type> default <value> -- to set normal value
declare <var> cursor for <select-query>

set <var> = <value>;
select count(*) into <var> from <tbl>;
<var> := (<select-query>)




-- Condition --

IF condition THEN [sql_statement_list]
  [ELSEIF condition THEN [sql_statement_list]]
  [...]
  [ELSE [sql_statement_list]]
END IF;


CASE
  WHEN boolean_expression THEN sql_statement_list
  [...]
  [ELSE sql_statement_list]
END CASE;



-- Looping --

<label_name>: LOOP
    statements;
    LEAVE / ITERATE <label_name>;
END LOOP <label_name>


<label_name> WHILE search_condition DO
    statement_list;
    LEAVE / ITERATE <label_name>;
END WHILE <label_name>;


label_name: REPEAT
  loop_statement_list
  UNTIL boolean_condition
END REPEAT <label_name>;


FOR loop_variable_name IN (<table_expression / sql statement>)
DO
  sql_expression_list
END FOR;



```

```sql

WITH LocationData AS (
    SELECT 1 AS EmpId, 'Gaurav' AS Name, 'Pune' AS Location1, 'Bangalore' AS Location2, 'Hyderabad' AS Location3
    UNION ALL
    SELECT 2, 'Risabh', 'Mumbai', 'Bangalore', 'Pune'
)
SELECT EmpId, Name, 'Location1' AS LocationSequence, Location1 AS LocationName FROM LocationData
UNION ALL
SELECT EmpId, Name, 'Location2' AS LocationSequence, Location2 AS LocationName FROM LocationData
UNION ALL
SELECT EmpId, Name, 'Location3' AS LocationSequence, Location3 AS LocationName FROM LocationData
ORDER BY EmpId, LocationSequence;


```

