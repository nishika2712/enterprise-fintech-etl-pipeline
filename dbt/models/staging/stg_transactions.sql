SELECT
    transaction_id,
    customer_id,
    amount,
    status,
    timestamp AS transaction_timestamp
FROM {{ source('raw_data', 'raw_transactions') }}
WHERE status = 'COMPLETED' AND amount > 0