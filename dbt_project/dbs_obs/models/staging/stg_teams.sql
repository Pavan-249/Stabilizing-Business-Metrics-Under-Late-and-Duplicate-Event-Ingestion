{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM read_csv_auto('data/team_data.csv', header=true)
)

SELECT 
    team_id,
    team_name
FROM source