from airflow import DAG
from airflow.operators import dummy
from airflow.providers.google.cloud.operators import bigquery
from airflow.utils.edgemodifier import Label
from airflow.utils.task_group import TaskGroup

default_args = {
    "owner": "cda",
    "retries": 0,
    "depends_on_past": False,
    "start_date": "2021-03-01",
    "email": "12708da5.pch.com@amer.teams.ms",
    "email_on_failure": True,
    "email_on_retry": True,
}


with DAG(
    dag_id="user_persona.agg_fact_user_intrests",
    default_args=default_args,
    max_active_runs=1,
    tags=["fact", "retool", "personas", "agg_fact_user_intrests"],
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:
    with TaskGroup(group_id="pre_process") as pre_process:
        # start
        start = dummy.DummyOperator(
            task_id="start",
        )
        # _tmp_ds_create
        _tmp_ds_create = bigquery.BigQueryCreateEmptyDatasetOperator(
            task_id="_tmp_ds_create",
            dataset_id="tmp_ds_user_persona_agg_fact_user_intrests",
            gcp_conn_id="cda_goldusersummary",
        )
        # check_dependencies_it_user_persona_repo_personas_repo
        check_dependencies_it_user_persona_repo_personas_repo = bigquery.BigQueryCheckOperator(
            task_id="check_dependencies_it_user_persona_repo_personas_repo",
            sql="select count(1) from `it_user_persona_repo.personas_repo_current`\n where last_access_date = \u0027{{ macros.ds_add(ds,-1) }}\u0027\n",
            use_legacy_sql=False,
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # end
        end = dummy.DummyOperator(
            task_id="end",
        )
        (
            start
            >> check_dependencies_it_user_persona_repo_personas_repo
            >> Label("sys_chk_passed")
            >> _tmp_ds_create
            >> end
        )
    with TaskGroup(group_id="process") as process:
        # start
        start = dummy.DummyOperator(
            task_id="start",
        )
        # tmp_get_01_personas_repo_hema_id
        tmp_get_01_personas_repo_hema_id = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_01_personas_repo_hema_id",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_01_personas_repo_hema_id` as\nselect \n    uid, \n    cust_id, \n    _hema_id as hema_id, \n    age, \n    gender, \n    state, \n    dma_cd, \n    dma_cd_desc, \n    last_access_date, \n    personas, \n    tpd_personas,\n    segment,\n    emailable.user_clicks.indicators as emailable_click_ids,\nfrom `it_user_persona_repo.personas_repo_current` as _record_source  \nleft join unnest(hema_ids) as _hema_id;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_02_personas_repo_hema_id
        tmp_get_02_personas_repo_hema_id = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_02_personas_repo_hema_id",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_02_personas_repo_hema_id` as\nselect \n uid, \n cust_id, \n hema_id,\n (\n  select \n   profile_repo \n  from `it_user_persona_repo.hema_ids` _dim_online_only_users\n  where _record_source.hema_id = _dim_online_only_users.hema_id\n ) as gmt_profiles,\n age, \n gender, \n state, \n dma_cd, \n dma_cd_desc, \n last_access_date, \n personas,\n tpd_personas,\n segment,\n emailable_click_ids\nfrom `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_01_personas_repo_hema_id` as _record_source;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_03_personas_repo_hema_id_gmt
        tmp_get_03_personas_repo_hema_id_gmt = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_03_personas_repo_hema_id_gmt",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_03_personas_repo_hema_id_gmt` as\n select \n     uid, \n     cust_id, \n     hema_id,\n     _gmt_profile.global_member_token as global_member_token,\n     _gmt_profile.is_email_purged_ind as is_email_purged_ind,\n     _gmt_profile.last_access_date as online_last_access_date,\n     _record_source.age  as age,\n     _record_source.gender  as gender,\n     _record_source.state  as state,\n     _record_source.dma_cd  as dma_cd,\n     _record_source.dma_cd_desc  as dma_cd_desc,\n     _record_source.last_access_date  as overall_last_access_date,\n     _record_source.personas as personas,\n     _record_source.tpd_personas as tpd_personas ,\n     _record_source.segment,\n     _record_source.emailable_click_ids\n from `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_02_personas_repo_hema_id` as _record_source \n left join unnest(gmt_profiles) as _gmt_profile;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_04_personas_repo_hema_id_gmt
        tmp_get_04_personas_repo_hema_id_gmt = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_04_personas_repo_hema_id_gmt",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_04_personas_repo_hema_id_gmt` as \nselect \n  uid,\n  cust_id, \n  hema_id, \n  global_member_token,\n  current_date() as etl_load_date,\n  sha512(to_json_string(\n            struct(\n               uid,\n               cust_id, \n               hema_id, \n               global_member_token\n            )\n        )\n  ) as etl_user_ids_hash,\n  sha512(to_json_string(\n            struct(\n              age, \n              gender, \n              state, \n              dma_cd, \n              dma_cd_desc\n            )\n        )\n  ) as etl_user_personas_profiles_hash,\n  sha512(to_json_string(\n            struct(\n              overall_last_access_date\n            )\n        )\n  ) as etl_user_personas_last_access_dates_hash,\n  sha512(to_json_string(\n            struct(\n              personas\n            )\n        )\n  ) as etl_user_personas_hash,\n  sha512(to_json_string(\n            struct(\n              tpd_personas\n            )\n        )\n  ) as etl_user_tpd_personas_hash,\n  is_email_purged_ind,\n  overall_last_access_date, \n  online_last_access_date,\n  age, \n  gender, \n  state, \n  dma_cd, \n  dma_cd_desc, \n  personas as personas, \n  tpd_personas as tpd_personas,\n  segment,\n  emailable_click_ids\nfrom `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_03_personas_repo_hema_id_gmt`;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_05_personas_repo_dim_ids
        tmp_get_05_personas_repo_dim_ids = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_05_personas_repo_dim_ids",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids` \n partition by\n     overall_last_access_date\n cluster by \n   _fact_user_id,\n   _fact_cust_id,\n   _fact_hema_id,\n   _fact_global_member_token\n as\n select \n   etl_load_date,\n   unix_date(overall_last_access_date) etl_load_partitoin_id,\n   extract(year FROM overall_last_access_date) AS etl_load_partition_year,\n   etl_user_ids_hash,\n   abs(farm_fingerprint(to_json_string(etl_user_ids_hash))) _fact_user_id,\n   uid,\n   abs(farm_fingerprint(to_json_string(uid))) _fact_uid, \n   cust_id,\n   abs(farm_fingerprint(to_json_string(cust_id))) _fact_cust_id,\n   hema_id,\n   abs(farm_fingerprint(to_json_string(hema_id))) _fact_hema_id,\n   global_member_token,\n   abs(farm_fingerprint(to_json_string(global_member_token))) _fact_global_member_token,\n   is_email_purged_ind,\n   etl_user_personas_profiles_hash,\n   age,\n   abs(farm_fingerprint(to_json_string(age))) _dim_age_id,\n   gender,\n   abs(farm_fingerprint(to_json_string(gender))) _dim_gender_id, \n   state,\n   abs(farm_fingerprint(to_json_string(state))) _dim_state_id, \n   dma_cd, \n   dma_cd_desc,\n   abs(farm_fingerprint(to_json_string(struct(dma_cd,dma_cd_desc)))) _dim_dma_cd_id,\n   etl_user_personas_last_access_dates_hash, \n   overall_last_access_date,online_last_access_date,\n   personas,\n   array(  select \n             abs(farm_fingerprint(sha512(to_json_string(struct(_p as _fpd_raw_field_name))))) as _dim_fpd_persona_id\n           from \n             unnest(personas),\n             unnest(persona) _p\n           group by \n             _p\n         ) as _dim_persona_ids,\n   abs(farm_fingerprint(to_json_string(personas))) _dim_overall_persona_id,\n   tpd_personas,\n   abs(farm_fingerprint(to_json_string(tpd_personas))) _dim_overall_tpd_persona_id, \n   array(  select \n             abs(farm_fingerprint(sha512(to_json_string(struct(tpd_raw_field_name as _tpd_raw_field_name,tier))))) as _dim_tpd_persona_id\n           from \n            unnest(tpd_personas.personas),\n            unnest(tiers) tier\n        ) as _dim_tpd_persona_ids,\n   segment,\n   array(  select  abs(farm_fingerprint(to_json_string(_s)))  as _dim_segment_id\n           from \n             unnest(segment) _s\n           group by \n             _s\n         ) as _dim_segment_ids,\n   emailable_click_ids,\n   array(  select  abs(farm_fingerprint(to_json_string(_s)))  as _dim_emailable_click_ids\n           from \n             unnest(emailable_click_ids) _s\n           group by \n             _s\n         ) as _dim_emailable_click_ids,\n\n from `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_04_personas_repo_hema_id_gmt`\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_segments
        tmp_get_06_personas_repo_stg_agg_segments = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_segments",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_segments`\n      cluster by\n      _fact_user_id as\n      select \n      _fact_user_id,\n       _info.segment_id as segment_id,\n      from \n        `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids` _source \n      join \n        unnest(_source._dim_segment_ids)  as _source_dim_segment\n      join user_persona.dim_segment _info on   _info._dim_segment_id = _source_dim_segment\n      group by \n        1,\n        2;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_emailable_ind
        tmp_get_06_personas_repo_stg_agg_emailable_ind = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_emailable_ind",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_emailable_ind`\n      cluster by\n      _fact_user_id as\n      select \n      _fact_user_id,\n       _info.last_access_date_id as last_emailable_ind,\n      from \n        `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids` _source \n      join \n        unnest(_source._dim_emailable_click_ids)  as _source_dim_emailable_click_id\n      join user_persona.dim_last_access_date _info on   _info._dim_last_access_date_id = _source_dim_emailable_click_id\n      group by \n        1,\n        2;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_tpd_personas
        tmp_get_06_personas_repo_stg_agg_tpd_personas = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_tpd_personas",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_tpd_personas`\n cluster by\n _fact_user_id as\n with tpd_rolled_up as \n (\n   select _dim_tpd_persona_id,persona_id from `user_persona.dim_tpd_persona` _info  \n   union distinct\n   select c._dim_tpd_persona_id,p.persona_id  from user_persona.dim_tpd_persona c\n   join user_persona.dim_tpd_persona p on c.parent=p.persona_name and c.tier=p.tier and p.approved_entry=2  and c.approved_entry=1\n )\n select \n _fact_user_id,_info.persona_id as tpd_persona_id \n from \n `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids` _source \n join \n unnest(_source._dim_tpd_persona_ids)  as _source_dim_tpd_persona_ids\n join  tpd_rolled_up _info on _info._dim_tpd_persona_id =_source_dim_tpd_persona_ids\n group by \n 1,\n 2;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_dim
        tmp_get_06_personas_repo_stg_agg_dim = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_dim",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_dim`\n cluster by\n _fact_user_id as\n select \n _fact_user_id,\n _fact_cust_id,\n _fact_hema_id,\n _fact_global_member_token,\n is_email_purged_ind,\n (select age_id from `user_persona.dim_age` as _info where _source._dim_age_id = _info._dim_age_id ) as age_id,\n (select gender_id from `user_persona.dim_gender` as _info where _source._dim_gender_id = _info._dim_gender_id ) as gender_id,\n (select state_id from `user_persona.dim_state` as _info where _source._dim_state_id = _info._dim_state_id ) as state_id,\n (select dma_cd_id from `user_persona.dim_dma_cd` as _info where _source._dim_dma_cd_id = _info._dim_dma_cd_id ) as dma_cd_id,\n _dim_persona_ids,\n _dim_tpd_persona_ids,\n online_last_access_date,\n overall_last_access_date\n from `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids`  _source \n ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_fpd_personas
        tmp_get_06_personas_repo_stg_agg_fpd_personas = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_fpd_personas",
            configuration={
                "query": {
                    "query": "create or replace table `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_fpd_personas`\n   cluster by\n   _fact_user_id as\n   with fpd_rolled_up\n   as (\n   select _dim_fpd_persona_id,persona_id from `user_persona.dim_fpd_persona` _info  \n  union distinct\n  select c._dim_fpd_persona_id,p.persona_id  from user_persona.dim_fpd_persona c\n  join user_persona.dim_fpd_persona p on c.parent=p.persona_name and p.approved_entry=2 and c.approved_entry=1\n  )\n   select \n   _fact_user_id,\n    _info.persona_id as persona_id,\n   from \n     `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids` _source \n   join \n     unnest(_source._dim_persona_ids)  as _source_dim_persona_ids\n   join fpd_rolled_up _info on   _info._dim_fpd_persona_id = _source_dim_persona_ids\n   group by \n     1,\n     2;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_merge
        tmp_get_06_personas_repo_stg_agg_merge = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_merge",
            configuration={
                "query": {
                    "query": "CREATE OR REPLACE TABLE\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_merge`\nPARTITION BY\n  DATE_TRUNC(overall_last_access_date,year)\nCLUSTER BY\n  _fact_cust_id AS\nSELECT\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id,\n  ARRAY_AGG(DISTINCT\n  IF\n  (_fact_hema_id=1659971858173592857,NULL,_fact_hema_id) IGNORE NULLS) _fact_hema_ids,\n  ARRAY_AGG(DISTINCT\n  IF\n  (is_email_purged_ind=0\n    AND _fact_global_member_token!=1659971858173592857,_fact_global_member_token,NULL) IGNORE NULLS) _fact_unpurged_gmts,\n  ARRAY_AGG(DISTINCT CAST(persona_id AS string)  IGNORE NULLS) _activity_persona_ids,\n  ARRAY_AGG(DISTINCT CAST(tpd_persona_id AS string) IGNORE NULLS) _activity_tpd_persona_ids\nFROM\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_dim` src\nLEFT JOIN\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_fpd_personas` fpd\nON\n  src._fact_user_id=fpd._fact_user_id\nLEFT JOIN\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_tpd_personas` tpd\nON\n  src._fact_user_id=tpd._fact_user_id\nGROUP BY\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_segment_merge
        tmp_get_06_personas_repo_stg_agg_segment_merge = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_segment_merge",
            configuration={
                "query": {
                    "query": "CREATE OR REPLACE TABLE  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_segment_merge` AS\nwith  segment_extract AS (\nSELECT\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id,\n  ARRAY_AGG(DISTINCT\n  IF\n  (_fact_hema_id=1659971858173592857,NULL,_fact_hema_id) IGNORE NULLS) _fact_hema_ids,\n  ARRAY_AGG(DISTINCT\n  IF\n  (is_email_purged_ind=0\n    AND _fact_global_member_token!=1659971858173592857,_fact_global_member_token,NULL) IGNORE NULLS) _fact_unpurged_gmts,\n  ARRAY_AGG(DISTINCT CAST(segment_id AS string) IGNORE NULLS) _activity_segment_ids\nFROM\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_dim` src\nLEFT JOIN\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_segments` seg\nON\n  src._fact_user_id=seg._fact_user_id\nGROUP BY\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id\n   )\n   SELECT\n    SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_hema_ids) as x order by 1) ))),\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_unpurged_gmts) as x order by 1)))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) uniq_id,_activity_segment_ids\n    from segment_extract\n    --where _activity_segment_ids is not null\n    ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_emailable_merge
        tmp_get_06_personas_repo_stg_agg_emailable_merge = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_emailable_merge",
            configuration={
                "query": {
                    "query": "CREATE OR REPLACE TABLE  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_emailable_merge` AS\nwith  emailable_extract AS (\nSELECT\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id,\n  ARRAY_AGG(DISTINCT\n  IF\n  (_fact_hema_id=1659971858173592857,NULL,_fact_hema_id) IGNORE NULLS) _fact_hema_ids,\n  ARRAY_AGG(DISTINCT\n  IF\n  (is_email_purged_ind=0\n    AND _fact_global_member_token!=1659971858173592857,_fact_global_member_token,NULL) IGNORE NULLS) _fact_unpurged_gmts,\n  ARRAY_AGG(DISTINCT CAST(last_emailable_ind AS string) IGNORE NULLS) _last_emailable_inds\nFROM\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_dim` src\nJOIN\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_emailable_ind` seg\nON\n  src._fact_user_id=seg._fact_user_id\nGROUP BY\n  overall_last_access_date,\n  online_last_access_date,\n  age_id,\n  gender_id,\n  state_id,\n  dma_cd_id,\n  _fact_cust_id\n   )\n   SELECT\n    SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_hema_ids) as x order by 1) ))),\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_unpurged_gmts) as x order by 1)))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) uniq_id,_last_emailable_inds\n    from emailable_extract\n    ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg_unified_personas
        tmp_get_06_personas_repo_stg_agg_unified_personas = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg_unified_personas",
            configuration={
                "query": {
                    "query": "CREATE OR REPLACE TABLE `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_unified_personas`AS\nWITH\n  persona_extract AS (\n  SELECT\n    SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(_fact_hema_ids))),\n          abs(farm_fingerprint(to_json_string(_fact_unpurged_gmts))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) uniq_id,\n    ARRAY(\n    SELECT\n      _info.persona_id\n    FROM\n      user_persona.dim_persona _info\n    JOIN\n      UNNEST(_activity_tpd_persona_ids) AS _tpd_persona_id\n    ON\n      CAST(_info.tpd_persona_id AS string) = _tpd_persona_id ) AS _activity_unified_tpd_persona_ids,\n    ARRAY(\n    SELECT\n      _info.persona_id\n    FROM\n      user_persona.dim_persona _info\n    JOIN\n      UNNEST(_activity_persona_ids) AS _fpd_persona_id\n    ON\n      CAST(_info.fpd_persona_id AS string) = _fpd_persona_id ) AS _activity_unified_fpd_persona_ids\n  FROM\n    `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_merge` agg )\nSELECT\n  uniq_id,\n  ARRAY(\n  SELECT\n    DISTINCT CAST(_pid AS string)\n  FROM\n    UNNEST(ARRAY_CONCAT(_activity_unified_tpd_persona_ids,_activity_unified_fpd_persona_ids)) AS _pid) AS _activity_unified_persona_ids\nFROM\n  persona_extract;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # tmp_get_06_personas_repo_stg_agg
        tmp_get_06_personas_repo_stg_agg = bigquery.BigQueryInsertJobOperator(
            task_id="tmp_get_06_personas_repo_stg_agg",
            configuration={
                "query": {
                    "query": "CREATE OR REPLACE TABLE\n  `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg` AS\nSELECT\n  agg.*,\n  u_persona._activity_unified_persona_ids,\n  seg._activity_segment_ids,\n  email._last_emailable_inds\nFROM\n  tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_merge agg\nLEFT JOIN\n  tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_unified_personas u_persona\nON\n  SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(_fact_hema_ids))),\n          abs(farm_fingerprint(to_json_string(_fact_unpurged_gmts))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) =u_persona.uniq_id\nLEFT JOIN\n  tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_segment_merge seg\nON\n  SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_hema_ids) as x order by 1) ))),\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_unpurged_gmts) as x order by 1)))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) =seg.uniq_id\nLEFT JOIN\n  tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_emailable_merge email\nON\n  SHA512(TO_JSON_STRING(STRUCT( \n          _fact_cust_id,\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_hema_ids) as x order by 1) ))),\n          abs(farm_fingerprint(to_json_string(array(select x from unnest(_fact_unpurged_gmts) as x order by 1)))),\n          overall_last_access_date,\n          online_last_access_date,\n          age_id,\n          gender_id,\n          state_id,\n          dma_cd_id ))) =email.uniq_id\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # end
        end = dummy.DummyOperator(
            task_id="end",
        )
        start >> tmp_get_01_personas_repo_hema_id >> tmp_get_02_personas_repo_hema_id
        tmp_get_02_personas_repo_hema_id >> tmp_get_03_personas_repo_hema_id_gmt
        tmp_get_03_personas_repo_hema_id_gmt >> tmp_get_04_personas_repo_hema_id_gmt
        tmp_get_04_personas_repo_hema_id_gmt >> tmp_get_05_personas_repo_dim_ids
        (
            tmp_get_05_personas_repo_dim_ids
            >> [
                tmp_get_06_personas_repo_stg_agg_tpd_personas,
                tmp_get_06_personas_repo_stg_agg_dim,
                tmp_get_06_personas_repo_stg_agg_fpd_personas,
            ]
            >> tmp_get_06_personas_repo_stg_agg_merge
            >> tmp_get_06_personas_repo_stg_agg_unified_personas
            >> tmp_get_06_personas_repo_stg_agg
        )
        (
            tmp_get_05_personas_repo_dim_ids
            >> [
                tmp_get_06_personas_repo_stg_agg_dim,
                tmp_get_06_personas_repo_stg_agg_segments,
            ]
            >> tmp_get_06_personas_repo_stg_agg_segment_merge
            >> tmp_get_06_personas_repo_stg_agg
        )
        (
            tmp_get_05_personas_repo_dim_ids
            >> [
                tmp_get_06_personas_repo_stg_agg_dim,
                tmp_get_06_personas_repo_stg_agg_emailable_ind,
            ]
            >> tmp_get_06_personas_repo_stg_agg_emailable_merge
            >> tmp_get_06_personas_repo_stg_agg
        )
        tmp_get_06_personas_repo_stg_agg >> end
    with TaskGroup(group_id="update_process") as update_process:
        # start
        start = dummy.DummyOperator(
            task_id="start",
        )
        # agg_fact_user_intrests_delete
        agg_fact_user_intrests_delete = bigquery.BigQueryInsertJobOperator(
            task_id="agg_fact_user_intrests_delete",
            configuration={
                "query": {
                    "query": "truncate table `user_persona.agg_fact_user_intrests` ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # agg_fact_user_intrests_insert
        agg_fact_user_intrests_insert = bigquery.BigQueryInsertJobOperator(
            task_id="agg_fact_user_intrests_insert",
            configuration={
                "query": {
                    "query": "insert into `user_persona.agg_fact_user_intrests` \nSELECT \n  _fact_cust_id,\n  abs(farm_fingerprint(to_json_string(_fact_hema_ids))) overall_fact_hema_id,\n  abs(farm_fingerprint(to_json_string(_fact_unpurged_gmts))) overall_fact_unpurged_gmts_id,\n  cast('{{ ds }}' as date) as etl_load_date,\n  overall_last_access_date,\n  age_id, \n  gender_id, \n  state_id, \n  dma_cd_id,\n  _fact_hema_ids, \n  _fact_unpurged_gmts,\n  _activity_persona_ids,\n  _activity_tpd_persona_ids,\n  online_last_access_date,\n  _activity_unified_persona_ids,\n  _activity_segment_ids,\n  _last_emailable_inds\nfrom `tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg` ;\n",
                    "useLegacySql": False,
                },
                "labels": {
                    "biz_resource": "tmp_ds_user_persona_agg_fact_user_intrests",
                    "biz_execution": "_daily",
                    "dev_search_terms": "cust_profile_data",
                },
            },
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # end
        end = dummy.DummyOperator(
            task_id="end",
        )
        start >> agg_fact_user_intrests_delete >> agg_fact_user_intrests_insert >> end
    with TaskGroup(group_id="post_process") as post_process:
        # start
        start = dummy.DummyOperator(
            task_id="start",
        )
        # del_tmp_get_01_personas_repo_hema_id
        del_tmp_get_01_personas_repo_hema_id = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_01_personas_repo_hema_id",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_01_personas_repo_hema_id",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_02_personas_repo_hema_id
        del_tmp_get_02_personas_repo_hema_id = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_02_personas_repo_hema_id",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_02_personas_repo_hema_id",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_03_personas_repo_hema_id_gmt
        del_tmp_get_03_personas_repo_hema_id_gmt = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_03_personas_repo_hema_id_gmt",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_03_personas_repo_hema_id_gmt",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_04_personas_repo_hema_id_gmt
        del_tmp_get_04_personas_repo_hema_id_gmt = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_04_personas_repo_hema_id_gmt",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_04_personas_repo_hema_id_gmt",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_05_personas_repo_dim_ids
        del_tmp_get_05_personas_repo_dim_ids = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_05_personas_repo_dim_ids",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_05_personas_repo_dim_ids",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_06_personas_repo_stg_agg
        del_tmp_get_06_personas_repo_stg_agg = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_06_personas_repo_stg_agg",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_06_personas_repo_stg_agg_tpd_personas
        del_tmp_get_06_personas_repo_stg_agg_tpd_personas = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_06_personas_repo_stg_agg_tpd_personas",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_tpd_personas",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_06_personas_repo_stg_agg_dim
        del_tmp_get_06_personas_repo_stg_agg_dim = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_06_personas_repo_stg_agg_dim",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_dim",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # del_tmp_get_06_personas_repo_stg_agg_fpd_personas
        del_tmp_get_06_personas_repo_stg_agg_fpd_personas = bigquery.BigQueryDeleteTableOperator(
            task_id="del_tmp_get_06_personas_repo_stg_agg_fpd_personas",
            deletion_dataset_table="{{ var.value.get(\u0027s_cda_genvar_env\u0027, \u0027none\u0027) }}-gold-usersummary.tmp_ds_user_persona_agg_fact_user_intrests.tmp_get_06_personas_repo_stg_agg_fpd_personas",
            gcp_conn_id="cda_goldusersummary",
            location="US",
        )
        # _tmp_ds_delete
        _tmp_ds_delete = bigquery.BigQueryDeleteDatasetOperator(
            task_id="_tmp_ds_delete",
            dataset_id="tmp_ds_user_persona_agg_fact_user_intrests",
            gcp_conn_id="cda_goldusersummary",
            delete_contents=True,
        )
        # end
        end = dummy.DummyOperator(
            task_id="end",
        )
        (
            start
            >> Label("clnup_tasks")
            >> [
                del_tmp_get_01_personas_repo_hema_id,
                del_tmp_get_02_personas_repo_hema_id,
                del_tmp_get_03_personas_repo_hema_id_gmt,
            ]
            >> _tmp_ds_delete
            >> end
        )
        (
            start
            >> Label("clnup_tasks")
            >> [
                del_tmp_get_04_personas_repo_hema_id_gmt,
                del_tmp_get_05_personas_repo_dim_ids,
                del_tmp_get_06_personas_repo_stg_agg_fpd_personas,
                del_tmp_get_06_personas_repo_stg_agg_tpd_personas,
                del_tmp_get_06_personas_repo_stg_agg_dim,
                del_tmp_get_06_personas_repo_stg_agg,
            ]
            >> _tmp_ds_delete
            >> end
        )

pre_process >> process >> update_process >> post_process