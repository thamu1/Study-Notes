
CREATE OR REPLACE FILE FORMAT FF_JSON
	TYPE = JSON
	NULL_IF = ()
	STRIP_OUTER_ARRAY = TRUE
;

create or replace table LOAD.L_COLLATE_TABLE_RAW
(
  col datatype, etc..
);

create stage @db.schema.<stage-name>;

create or replace pipe PIPE_COLLATE_TABLE_RAW auto_ingest=false 
as 
COPY INTO LOAD.L_COLLATE_TABLE_RAW
FROM (
    SELECT 
        $1 as raw,
        $1:batch_id:: varchar,
        $1:_loaded_date::varchar,
        $1:_loaded_by::varchar,
        METADATA$FILENAME as filename 
    FROM '@<stage-name>/collate/table/'
    (FILE_FORMAT => 'LOAD.FF_JSON')
);
