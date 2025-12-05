


SELECT 1 AS shop_id, 'FreshMart' AS shop_name, 'New York, NY' AS location, DATE '2020-03-15' AS open_date,
       'Grocery' AS shop_type, TRUE AS is_active, 'Alice Johnson' AS owner_name
UNION ALL
SELECT 2, 'TechZone', 'San Francisco', DATE '2019-11-01', 'Electronics', TRUE, 'Bob Smith'
UNION ALL
SELECT 3, 'BookBarn', 'Chicago, IL', DATE '2018-07-22', 'Bookstore', FALSE, 'Karen Wright'
UNION ALL
SELECT 4, 'StyleHub', 'Los Angeles', DATE '2021-05-10', 'Fashion', TRUE, 'David Lin'
UNION ALL
SELECT 5, 'PetWorld', 'Austin, TX', DATE '2022-09-30', 'Pet Store', TRUE, 'Rachel Green'
UNION ALL
SELECT 6, 'BakeHouse', 'Portland, OR', DATE '2020-12-05', 'Bakery', FALSE, 'James Miller'
UNION ALL
SELECT 7, 'MobileMania', 'Miami, FL', DATE '2023-01-20', 'Electronics', TRUE, 'Sunil Patel';