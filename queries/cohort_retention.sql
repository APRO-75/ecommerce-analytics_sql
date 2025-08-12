-- Cohort retention analysis
-- Tracks customer retention by their first order month
WITH customer_cohorts AS (
    -- Determine each customer's cohort (first order month)
    SELECT 
        customer_id,
        date_trunc('month', MIN(order_date)) AS cohort_month
    FROM orders
    WHERE payment_status = 'paid'
    GROUP BY customer_id
),
customer_activities AS (
    -- Get all activity months for each customer
    SELECT 
        o.customer_id,
        cc.cohort_month,
        date_trunc('month', o.order_date) AS activity_month
    FROM orders o
    JOIN customer_cohorts cc ON cc.customer_id = o.customer_id
    WHERE 
        o.payment_status = 'paid'
        AND cc.cohort_month >= :start_date
        AND cc.cohort_month <= :end_date
),
cohort_sizes AS (
    -- Count of customers in each cohort
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohorts
    WHERE 
        cohort_month >= :start_date
        AND cohort_month <= :end_date
    GROUP BY cohort_month
),
cohort_activities AS (
    -- Calculate months since cohort for each activity
    SELECT 
        cohort_month,
        EXTRACT(year FROM activity_month) * 12 + EXTRACT(month FROM activity_month) - 
        (EXTRACT(year FROM cohort_month) * 12 + EXTRACT(month FROM cohort_month)) AS months_since,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM customer_activities
    GROUP BY cohort_month, months_since
)
SELECT 
    ca.cohort_month,
    ca.months_since,
    ca.active_customers,
    cs.cohort_size,
    ROUND(ca.active_customers * 100.0 / cs.cohort_size, 2) AS retention_rate
FROM cohort_activities ca
JOIN cohort_sizes cs ON cs.cohort_month = ca.cohort_month
WHERE ca.months_since <= :horizon
ORDER BY ca.cohort_month, ca.months_since;
