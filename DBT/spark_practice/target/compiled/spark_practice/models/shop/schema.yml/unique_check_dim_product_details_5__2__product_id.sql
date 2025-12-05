

    select product_name
        , category
        , count(1) as cnt 
    from  default.dim_product_details -- default.dim_product_details
    where 5 = 2
    group by 1, 2 having count(1) > 1

