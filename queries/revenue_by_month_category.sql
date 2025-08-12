-- Revenue by month and category analysis
-- Groups revenue by month and category for paid orders
WITH order_lines AS (
    SELECT 
        oi.order_id,
        oi.product_id,
        (oi.unit_price * oi.quantity - oi.discount) AS net_line_revenue
    FROM order_items oi
),
monthly_revenue AS (
    SELECT 
        date_trunc('month', o.order_date) AS month,
        c.category_name,
        SUM(ol.net_line_revenue) AS revenue
    FROM orders o
    JOIN order_lines ol ON ol.order_id = o.order_id
    JOIN products p ON p.product_id = ol.product_id
    JOIN categories c ON c.category_id = p.category_id
    WHERE 
        o.order_date >= :start_date
        AND o.order_date <= :end_date
        AND o.payment_status = 'paid'
        AND o.order_status IN ('paid', 'shipped', 'delivered')
    GROUP BY 
        date_trunc('month', o.order_date),
        c.category_name
)
SELECT 
    month,
    category_name,
    ROUND(revenue, 2) AS revenue
FROM monthly_revenue
ORDER BY month, revenue DESC;
