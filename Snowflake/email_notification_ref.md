Email Notification From Snowflake Notification Service:
-------------------------------------------------------

```sql

SHOW USERS;


SELECT 
    user_id, name, login_name, email, type, is_email_verified, DISABLED
FROM snowflake.ACCOUNT_USAGE.USERS
WHERE EMAIL IS NOT NULL
    and name in ('TC@abc.COM','RRATHORE@abc.COM', 'YCHEN279@abc.COM', 'JGANDHI@abc.COM')
; -- Check the User is verified or not | Use the **Email field for the notification**



desc notification integration <Snowflake Notification Service Name>;

```
 
Step 1:
-------
Request to create Notification Service using this Link.
 
Step 2:
-------
CREATE OR REPLACE NOTIFICATION INTEGRATION <Snowflake Notification Service Name>
  TYPE = EMAIL
  ENABLED = TRUE
  ALLOWED_RECIPIENTS = ('<Mail ID which you want to Allow>')
  ;  -- If we do not give any recipient -> All verified user can receive mail.
 
 
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

        /*
        sql_stmt := 'CALL SYSTEM$SEND_EMAIL(
                ''' || rec.notification_service_name || ''',
                ''' || rec.to_mail || ''',
                ''' || rec.subject || ''',
                ''' || '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
                    <tr>
                        <th>Usecase</th>
                        <th>Provider</th>
                        <th>Fine-Tuned Status</th>
                        <th>Model Version</th>
                        <th>Max Threshold</th>
                        <th>Current Threshold</th>
                    </tr>
                    <tr>
                        <td>' || :usecase || '</td>
                        <td>' || rec.model_provider || '</td>
                        <td>' || fine_tuned_status || '</td>
                        <td>' || rec.model_version || '</td>
                        <td>' || rec.max_threshold || '</td>
                        <td style="color: red; font-weight: bold;">' || rec.current_usage || '</td>
                    </tr>
                </table>' || ''',
                ''' || text_format || '''
            )';

           */
 
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
