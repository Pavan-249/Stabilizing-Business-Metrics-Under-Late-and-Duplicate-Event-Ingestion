SELECT
  'as_of_4_40_40' AS snapshot,
  COUNT(*) AS tickets_sold
FROM raw.ticket_events
WHERE DATE(purchase_timestamp) = '2026-07-07'
  AND ingest_timestamp <= '2025-12-25 04:40:40.006'

UNION ALL

SELECT
  'as_of_4_40_35',
  COUNT(*)
FROM raw.ticket_events
WHERE DATE(purchase_timestamp) = '2026-07-07'
  AND ingest_timestamp <= '2025-12-25 04:40:35.004'

UNION ALL

SELECT
  'as_of_4_40_50',
  COUNT(*)
FROM raw.ticket_events
WHERE DATE(purchase_timestamp) = '2026-07-07'
  AND ingest_timestamp <= '2025-12-25 04:40:50.004';