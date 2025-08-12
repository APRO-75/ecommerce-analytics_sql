-- Repeat purchase rate analysis by month
-- Calculates the percentage of customers who made repeat purchases
WITH monthly_customers AS (
    SELECT 
        date_trunc('month', o.order_date) AS month,
        o.customer_id,
        MIN(o.order_date) OVER (PARTITION BY o.customer_id) AS first_order_date
    FROM orders o
    WHERE 
        o.order_date >= :start_date
        AND o.order_date <= :end_date
        AND o.payment_status = 'paid'
),
monthly_stats AS (
    SELECT 
        month,
        COUNT(DISTINCT customer_id) AS total_customers,
        COUNT(DISTINCT CASE 
            WHEN date_trunc('month', first_order_date) < month 
            THEN customer_id 
        END) AS repeat_customers
    FROM monthly_customers
    GROUP BY month
)
SELECT 
    month,
    total_customers,
    repeat_customers,
    CASE 
        WHEN total_customers > 0 
        THEN ROUND(repeat_customers * 100.0 / total_customers, 2)
        ELSE 0 
    END AS repeat_rate
FROM monthly_stats
ORDER BY month;
