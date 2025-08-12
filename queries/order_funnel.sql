-- Order funnel status analysis
-- Shows conversion rates through order statuses
WITH order_counts AS (
    SELECT 
        order_status,
        COUNT(*) AS order_count
    FROM orders
    WHERE 
        order_date >= :start_date
        AND order_date <= :end_date
    GROUP BY order_status
),
total_orders AS (
    SELECT SUM(order_count) AS total
    FROM order_counts
)
SELECT 
    oc.order_status AS status,
    oc.order_count AS orders,
    ROUND(oc.order_count * 100.0 / t.total, 2) AS percentage
FROM order_counts oc
CROSS JOIN total_orders t
ORDER BY 
    CASE oc.order_status
        WHEN 'created' THEN 1
        WHEN 'paid' THEN 2
        WHEN 'shipped' THEN 3
        WHEN 'delivered' THEN 4
        WHEN 'canceled' THEN 5
        WHEN 'refunded' THEN 6
        ELSE 7
    END;
