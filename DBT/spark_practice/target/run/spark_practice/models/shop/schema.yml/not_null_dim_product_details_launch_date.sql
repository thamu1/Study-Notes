
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select launch_date
from default.dim_product_details
where launch_date is null



  
  
      
    ) dbt_internal_test