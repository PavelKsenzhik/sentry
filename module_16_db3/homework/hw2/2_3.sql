SELECT o.order_no, c.full_name, m.full_name
    FROM `order` AS o
    JOIN `manager` AS m on o.manager_id = m.manager_id
    JOIN `customer` AS c on o.customer_id = c.customer_id
    WHERE c.city != m.city
