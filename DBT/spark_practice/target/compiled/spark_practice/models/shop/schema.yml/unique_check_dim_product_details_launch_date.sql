

    select product_name
        , category
        , count(1) as cnt 
    from  default.dim_product_details -- default.dim_product_details
    group by 1, 2 having count(1) > 1

