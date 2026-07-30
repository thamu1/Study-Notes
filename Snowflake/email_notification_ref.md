Email Notification From Snowflake Notification Service:
-------------------------------------------------------
 
Step 1:
-------
Request to create Notification Service using this Link.
 
Step 2:
-------
CREATE OR REPLACE NOTIFICATION INTEGRATION <Snowflake Notification Service Name>
  TYPE = EMAIL
  ENABLED = TRUE
  ALLOWED_RECIPIENTS = ('<Mail ID which you want to Allow>');
 
 
desc notification integration <Snowflake Notification Service Name>;
 
-- Testing:
CALL SYSTEM$SEND_EMAIL(
    '<Snowflake Notification Service Name>',                     -- Integration Name
    '<Mail ID>',              -- Recipient(s)
    'Snowflake Query Status Alert',     -- Subject
    'The data processing query completed successfully.' -- Body
);
 
 
 
Step 3:
-------
DECLARE
    fine_tuned_status STRING;
    usecase STRING;
    sql_stmt STRING;
    use_case_log_status string;
    c CURSOR FOR
        SELECT use_case, model_provider, fine_tuned, frequency, model_version
        FROM db.schema.table_name;
 
BEGIN
 
    let a string := '';
 
    FOR rec IN c DO
 
        usecase := rec.use_case;
        IF (rec.fine_tuned = 'NO') THEN
            fine_tuned_status := ' IS NOT ';
        ELSE
            fine_tuned_status := ' IS ';
        END IF;
 

        IF (rec.frequency = 'DAILY') THEN
 
            -- Daily Notification Trigger
 
            use_case_log_status := (select status from db.schema.table_name 
                                                where use_case = :usecase 
                                                    and status = 'success' 
                                                    and log_dt::date = current_date() 
                                                );
 
        ELSEIF (rec.frequency = 'MONTHLY') THEN
 
            -- Monthly Notification Trigger
 
            use_case_log_status := (select status from db.schema.table_name 
                                                where use_case = :usecase 
                                                    and status = 'success' 
                                                    and to_char(log_dt, 'yyyy-mm') = to_char(current_date(), 'yyyy-mm') 
                                                );
        END IF;
 
 
        sql_stmt := 'CALL SYSTEM$SEND_EMAIL(
                    ''' || '<Snowflake Notification Service name>' || ''' ,
                    ''' || '<mail id>' || ''' ,
                    ''' || 'Notification' ||''' ,
                    ''' || 'Provider ' || rec.model_provider || fine_tuned_status || ' fine tuned for model ' || rec.model_version || '''
                ) ';
 
        -- a := a || '-' || use_case_log_status || ',';
        IF (use_case_log_status IS NULL) THEN
            BEGIN
 
                IF (sql_stmt IS NOT NULL AND sql_stmt <> '') THEN
 
                    EXECUTE IMMEDIATE sql_stmt;
 
                    INSERT INTO db.schema.table_name
                    VALUES(:usecase, CURRENT_DATE(), 'success', 'completed');
 
                END IF;
 
            EXCEPTION
                WHEN OTHER THEN
 
                    INSERT INTO db.schema.table_name
                    VALUES (:usecase, CURRENT_DATE(), 'failed', :SQLERRM );
            END;
        END IF;
    END FOR;
 
    -- RETURN a;
    RETURN 'Completed Successfully';
 
END;