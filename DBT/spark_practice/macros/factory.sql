

-- dbt run-operation create_db --args '{db_name: shop}'

{% macro create_db(db_name) %}
    {% set query %}
        create database if not exists {{db_name}} 
    {% endset %}

    {% if execute %}
        {% do run_query(query) %}
    {% endif %}

{% endmacro%}


-- dbt run-operation create_dim_shop_details_tbl --args '{tbl_name: dim_shop_details}'

{% macro create_dim_shop_details_tbl(tbl_name) %} -- 
    {% set query %}
        CREATE TABLE shop.{{tbl_name}} (
            shop_id INT,
            shop_name string,
            location string,
            open_date DATE,
            shop_type string,
            is_active BOOLEAN,
            owner_name string
        )
    {% endset %}

    {% if execute %}
        {% do run_query(query) %}
    {% endif %}

{% endmacro%}

