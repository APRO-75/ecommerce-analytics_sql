-- Low stock alerts
-- Products that need reordering based on inventory levels
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    i.on_hand_qty,
    i.reorder_point,
    i.reorder_qty AS recommended_order_qty,
    CASE 
        WHEN i.on_hand_qty = 0 THEN 'Out of Stock'
        WHEN i.on_hand_qty <= i.reorder_point * 0.5 THEN 'Critical'
        ELSE 'Low'
    END AS urgency
FROM inventory i
JOIN products p ON p.product_id = i.product_id
JOIN categories c ON c.category_id = p.category_id
WHERE 
    i.on_hand_qty <= i.reorder_point
    AND p.is_active = true
ORDER BY 
    CASE 
        WHEN i.on_hand_qty = 0 THEN 1
        WHEN i.on_hand_qty <= i.reorder_point * 0.5 THEN 2
        ELSE 3
    END,
    i.on_hand_qty ASC
LIMIT :limit_n;
