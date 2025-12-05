
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  

    select product_name
        , category
        , count(1) as cnt 
    from  default.dim_product_details -- default.dim_product_details
    where 2 = 2
    group by 1, 2 having count(1) > 1


  
  
      
    ) dbt_internal_test