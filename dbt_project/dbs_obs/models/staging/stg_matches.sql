{{ config(materialized='table') }}
WITH source AS (
    SELECT * FROM read_csv_auto('data/matches_data.csv', header=true)
)

SELECT 
    match_id,
    home_team_id,
    away_team_id,
    stadium_id,
    match_date
    
FROM source