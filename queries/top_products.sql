-- Top products by margin analysis
-- Shows products with highest profit margins
WITH product_performance AS (
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        SUM(oi.quantity) AS units_sold,
        SUM((oi.unit_price * oi.quantity) - oi.discount) AS revenue,
        SUM((oi.unit_price - p.unit_cost) * oi.quantity - oi.discount) AS margin
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    JOIN products p ON p.product_id = oi.product_id
    JOIN categories c ON c.category_id = p.category_id
    WHERE 
        o.order_date >= :start_date
        AND o.order_date <= :end_date
        AND o.payment_status = 'paid'
        AND o.order_status IN ('paid', 'shipped', 'delivered')
    GROUP BY 
        p.product_id, 
        p.product_name, 
        c.category_name
)
SELECT 
    product_id,
    product_name,
    category_name,
    units_sold,
    ROUND(revenue, 2) AS revenue,
    ROUND(margin, 2) AS margin,
    CASE 
        WHEN revenue > 0 
        THEN ROUND(margin * 100.0 / revenue, 2)
        ELSE 0 
    END AS margin_percent
FROM product_performance
WHERE margin > 0
ORDER BY margin DESC
LIMIT :limit_n;
