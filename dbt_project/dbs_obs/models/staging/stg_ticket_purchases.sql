
WITH source AS (
    SELECT * FROM read_csv_auto('../../ticket_purchases_raw.csv', header=true)
),

with_lag AS (
    SELECT 
        *,
        EXTRACT(EPOCH FROM (ingest_timestamp - purchase_timestamp)) AS ingestion_lag_seconds
    FROM source
),

deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY ticket_id 
            ORDER BY purchase_timestamp ASC, ingest_timestamp ASC
        ) AS row_num
    FROM with_lag
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
    ingest_timestamp,
    ingestion_lag_seconds
FROM deduplicated
WHERE row_num = 1