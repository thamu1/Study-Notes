

{% test unique_check(model, column_name, a, b) %}

    select product_name
        , category
        , count(1) as cnt 
    from  {{ model }} -- default.dim_product_details
    where {{ a }} = {{ b }}
    group by 1, 2 having count(1) > 1

{% endtest %}