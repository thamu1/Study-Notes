
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shop_id
from default.dim_shop_details
where shop_id is null



  
  
      
    ) dbt_internal_test