
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  

    select *
    from default.dim_shop_details
    where is_active = False


  
  
      
    ) dbt_internal_test