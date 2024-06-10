SELECT DISTINCT c1.full_name, c2.full_name
    FROM `customer` AS c1
    JOIN `customer` AS c2 ON c1.city=c2.city AND c1.manager_id=c2.manager_id
    WHERE c1.manager_id IS NOT NULL AND c1.customer_id != c2.customer_id
    order by c1.full_name, c2.full_name
