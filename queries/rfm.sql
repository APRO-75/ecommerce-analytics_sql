-- RFM Analysis (Recency, Frequency, Monetary)
-- Scores customers on a 5-5-5 scale for segmentation
WITH customer_metrics AS (
    SELECT 
        o.customer_id,
        -- Recency: days since last order
        EXTRACT(epoch FROM (:as_of_date::date - MAX(o.order_date::date))) / 86400 AS recency_days,
        -- Frequency: number of orders
        COUNT(DISTINCT o.order_id) AS frequency,
        -- Monetary: total revenue
        SUM((oi.unit_price * oi.quantity) - oi.discount) AS monetary
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE 
        o.payment_status = 'paid'
        AND o.order_date <= :as_of_date
    GROUP BY o.customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        -- RFM Scoring (1-5 scale)
        -- Recency: lower days = higher score (more recent is better)
        6 - NTILE(5) OVER (ORDER BY recency_days ASC) AS r_score,
        -- Frequency: higher count = higher score
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        -- Monetary: higher value = higher score
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_metrics
    WHERE monetary > 0
)
SELECT 
    customer_id,
    ROUND(recency_days, 0) AS recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 3 THEN 'Cannot Lose Them'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
        ELSE 'Others'
    END AS segment
FROM rfm_scores
ORDER BY rfm_total DESC, monetary DESC;
