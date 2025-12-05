
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  

    select count(1) as cnt 
    from default.dim_shop_details
    where is_active = true


  
  
      
    ) dbt_internal_test