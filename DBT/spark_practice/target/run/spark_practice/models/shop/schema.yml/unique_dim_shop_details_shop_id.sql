
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    shop_id as unique_field,
    count(*) as n_records

from default.dim_shop_details
where shop_id is not null
group by shop_id
having count(*) > 1



  
  
      
    ) dbt_internal_test