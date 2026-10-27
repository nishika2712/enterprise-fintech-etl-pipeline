SELECT
    customer_id,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount) AS lifetime_spend,
    MAX(transaction_timestamp) AS last_transaction_date
FROM {{ ref('stg_transactions') }}
GROUP BY customer_id