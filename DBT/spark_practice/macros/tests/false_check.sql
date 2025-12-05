
{% test false_check(model, column_name) %}

    select *
    from default.dim_shop_details
    where is_active = False

{% endtest %}



{% test false_check_with_arg(model, column_name, flag) %}

    select *
    from default.dim_shop_details
    where shop_type = {{ flag }}

{% endtest %}
