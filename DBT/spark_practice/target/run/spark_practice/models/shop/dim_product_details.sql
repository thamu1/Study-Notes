
  
    
        create table default.dim_product_details
      
      
      
      
      
      
      
      

      as
      

SELECT 101 AS product_id, 'UltraPhone X' AS product_name, 'Electronics' AS category, 799.99 AS price,
       TRUE AS in_stock, 'Tech Suppliers' AS supplier, DATE '2021-06-10' AS launch_date
UNION ALL
SELECT 102, 'Eco Blender', 'Home Appliances', 129.99, TRUE, 'Home Goods Inc', DATE '2020-11-25'
UNION ALL
SELECT 103, 'Running Shoes', 'Sportswear', 89.99, FALSE, 'FitGear', DATE '2019-04-15'
UNION ALL
SELECT 104, 'Organic Coffee', 'Grocery', 14.99, TRUE, 'Coffee Co', DATE '2022-01-05'
UNION ALL
SELECT 105, 'LED Desk Lamp', 'Home Decor', 45.00, TRUE, 'BrightLights', DATE '2021-09-12'
UNION ALL
SELECT 106, 'Yoga Mat', 'Sportswear', 35.50, TRUE, 'FitGear', DATE '2023-03-01'
UNION ALL
SELECT 107, 'Noise-Canceling Headphones', 'Electronics', 199.99, TRUE, 'Tech Suppliers', DATE '2022-07-20'
UNION ALL
SELECT 108, 'Smart Watch', 'Electronics', NULL, TRUE, 'Tech Suppliers', DATE '2022-10-15'
UNION ALL
SELECT 109, 'Eco Blender', 'Home Appliances', 129.99, TRUE, 'Home Goods Inc', DATE '2020-11-25'
UNION ALL
SELECT 110, 'Running Shoes', 'Sportswear', 89.99, NULL, 'FitGear', DATE '2019-04-15'
UNION ALL
SELECT 111, 'Portable Charger', 'Electronics', 29.99, TRUE, NULL, DATE '2021-12-01'
UNION ALL
SELECT 112, 'Yoga Mat', 'Sportswear', 35.50, TRUE, 'FitGear', NULL
UNION ALL
SELECT 113, 'Noise-Canceling Headphones', 'Electronics', 199.99, TRUE, 'Tech Suppliers', DATE '2022-07-20';
  