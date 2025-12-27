{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ source('raw', 'ticket_events') }}
),


deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
        PARTITION BY ticket_id
        ORDER BY purchase_timestamp, ingest_timestamp
        ) AS row_num
    FROM source
)
SELECT 
    ticket_id,
    match_id,
    user_id,
    user_name,
    user_email,
    ticket_type,
    quantity,
    stadium,
    price,
    purchase_timestamp,
    ingest_timestamp
FROM deduplicated
WHERE row_num = 1