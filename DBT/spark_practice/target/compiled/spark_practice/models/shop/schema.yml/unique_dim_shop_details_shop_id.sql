
    
    

select
    shop_id as unique_field,
    count(*) as n_records

from default.dim_shop_details
where shop_id is not null
group by shop_id
having count(*) > 1


