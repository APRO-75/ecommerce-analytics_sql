-- Daily KPI snapshot
-- Key performance indicators for a specific date
WITH daily_orders AS (
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(payment_amount) AS total_revenue
    FROM orders
    WHERE 
        DATE(order_date) = :target_date
        AND payment_status = 'paid'
),
new_customers AS (
    SELECT 
        COUNT(DISTINCT customer_id) AS new_customers_count
    FROM orders
    WHERE 
        DATE(order_date) = :target_date
        AND payment_status = 'paid'
        AND customer_id NOT IN (
            SELECT DISTINCT customer_id 
            FROM orders 
            WHERE DATE(order_date) < :target_date
            AND payment_status = 'paid'
        )
),
top_category AS (
    SELECT 
        c.category_name AS top_category_name,
        SUM((oi.unit_price * oi.quantity) - oi.discount) AS category_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p ON p.product_id = oi.product_id
    JOIN categories c ON c.category_id = p.category_id
    WHERE 
        DATE(o.order_date) = :target_date
        AND o.payment_status = 'paid'
    GROUP BY c.category_name
    ORDER BY category_revenue DESC
    LIMIT 1
),
top_product AS (
    SELECT 
        p.product_name AS top_product_name,
        SUM(oi.quantity) AS units_sold
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p ON p.product_id = oi.product_id
    WHERE 
        DATE(o.order_date) = :target_date
        AND o.payment_status = 'paid'
    GROUP BY p.product_name
    ORDER BY units_sold DESC
    LIMIT 1
)
SELECT 
    :target_date AS date,
    COALESCE(dorders.total_orders, 0) AS orders,
    COALESCE(ROUND(dorders.total_revenue, 2), 0) AS revenue,
    CASE 
        WHEN dorders.total_orders > 0 
        THEN ROUND(dorders.total_revenue / dorders.total_orders, 2)
        ELSE 0 
    END AS aov,
    COALESCE(dorders.unique_customers, 0) AS unique_customers,
    COALESCE(nc.new_customers_count, 0) AS new_customers,
    CASE 
        WHEN dorders.unique_customers > 0 
        THEN ROUND((dorders.unique_customers - nc.new_customers_count) * 100.0 / dorders.unique_customers, 2)
        ELSE 0 
    END AS repeat_rate,
    COALESCE(tc.top_category_name, 'N/A') AS top_category,
    COALESCE(tp.top_product_name, 'N/A') AS top_product
FROM daily_orders dorders
CROSS JOIN new_customers nc
LEFT JOIN top_category tc ON true
LEFT JOIN top_product tp ON true;
