-- sql_queries/add_stock.sql

-- Step 1: Identify Confirmed Sales Orders Created via CLI (Partner: 'CLI Client')
WITH cli_sales_orders AS (
    SELECT so.id
    FROM sale_order so
    JOIN res_partner rp ON so.partner_id = rp.id
    WHERE rp.name ILIKE 'CLI Client'  -- Case-insensitive match
      AND so.state = 'sale'            -- Confirmed SOs
),

-- Step 2: Aggregate Quantities per Product from CLI-Created SOs
product_sales AS (
    SELECT
        sol.product_id,
        SUM(sol.product_uom_qty) AS total_quantity
    FROM sale_order_line sol
    JOIN cli_sales_orders cs ON sol.order_id = cs.id
    GROUP BY sol.product_id
),

-- Step 3: Retrieve Stock Location ID for 'WH/Stock'
stock_location AS (
    SELECT sl.id AS location_id
    FROM stock_location sl
    WHERE sl.complete_name = 'WH/Stock'
)

-- Step 4: Insert Aggregated Quantities into stock_quant
INSERT INTO stock_quant (
    product_id,
    location_id,
    quantity,
    reserved_quantity,
    in_date,
    company_id
)
SELECT
    ps.product_id,
    sl.location_id,
    ps.total_quantity,
    0,
    NOW(),
    1
FROM product_sales ps
CROSS JOIN stock_location sl;
