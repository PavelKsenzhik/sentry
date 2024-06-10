SELECT customer.full_name as customer_full_name, manager.full_name as manager_full_name, purchase_amount, date
    FROM "order"
    JOIN customer on "order".customer_id = customer.customer_id
    JOIN manager on "order".manager_id = manager.manager_id