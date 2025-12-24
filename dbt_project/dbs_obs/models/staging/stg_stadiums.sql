{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM read_csv_auto('data/stadium_data.csv', header=true)
)

SELECT 
    stadium_id,stadium_name,stadium_capacity,avg_ticket_price
FROM source