{{ config(materialized='table') }}

WITH target_day AS (
    SELECT
        DATE(purchase_timestamp) AS sale_date,
        COUNT(*) AS event_count
    FROM {{ source('raw', 'ticket_events') }}
    GROUP BY 1
    ORDER BY event_count DESC
    LIMIT 1
),

ingest_window AS (
    SELECT
        MIN(ingest_timestamp) AS first_ingest,
        MAX(ingest_timestamp) AS last_ingest
    FROM {{ source('raw', 'ticket_events') }}
    WHERE DATE(purchase_timestamp) = (SELECT sale_date FROM target_day)
),

checkpoints AS (
    SELECT 'T0 + 1h' AS checkpoint, first_ingest + INTERVAL '1 hour' AS observed_at FROM ingest_window
    UNION ALL
    SELECT 'T0 + 6h', first_ingest + INTERVAL '6 hours' FROM ingest_window
    UNION ALL
    SELECT 'T0 + 1d', first_ingest + INTERVAL '1 day' FROM ingest_window
    UNION ALL
    SELECT 'Final', last_ingest FROM ingest_window
)

SELECT
    (SELECT sale_date FROM target_day) AS sale_date,
    c.checkpoint,
    c.observed_at,
    COUNT(DISTINCT e.ticket_id) AS tickets_sold
FROM checkpoints c
JOIN {{ source('raw', 'ticket_events') }} e
  ON DATE(e.purchase_timestamp) = (SELECT sale_date FROM target_day)
 AND e.ingest_timestamp <= c.observed_at
GROUP BY 1, 2, 3
ORDER BY
    CASE c.checkpoint
        WHEN 'T0 + 1h' THEN 1
        WHEN 'T0 + 6h' THEN 2
        WHEN 'T0 + 1d' THEN 3
        WHEN 'Final' THEN 4
    END
