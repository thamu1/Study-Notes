create or replace view default.my_second_dbt_model
  
  
  as
    -- Use the `ref` function to select from other models

select *
from default.my_first_dbt_model
where id = 1
