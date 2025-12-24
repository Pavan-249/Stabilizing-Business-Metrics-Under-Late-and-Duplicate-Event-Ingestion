WITH tickets AS (
    SELECT * FROM {{ ref('stg_ticket_purchases') }}
),

matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

teams_home AS (
    SELECT * FROM {{ ref('stg_teams') }}
),

teams_away AS (
    SELECT * FROM {{ ref('stg_teams') }}
),

stadiums AS (
    SELECT * FROM {{ ref('stg_stadiums') }}
),



enriched_tickets AS (
    SELECT 
        t.ticket_id,
        t.purchase_timestamp,
        t.price,
        t.quantity,
        t.ticket_type,
        t.ingestion_lag_seconds,
        m.match_date,
        home.team_name AS home_team,
        away.team_name AS away_team,
        s.stadium_name
    FROM tickets t
    LEFT JOIN matches m ON t.match_id = m.match_id
    LEFT JOIN teams_home home ON m.home_team_id = home.team_id
    LEFT JOIN teams_away away ON m.away_team_id = away.team_id
    LEFT JOIN stadiums s ON m.stadium_id = s.stadium_id
),

daily_aggregates AS (
    SELECT
        DATE(purchase_timestamp) AS sale_date,
        match_date,
        home_team,
        away_team,
        stadium_name,
        
        COUNT(DISTINCT ticket_id) AS tickets_sold,
        SUM(quantity) AS total_quantity,
        SUM(price) AS total_revenue,
        AVG(price) AS avg_transaction_value,
        
        -- By section
        SUM(CASE WHEN ticket_type = 'GA' THEN quantity ELSE 0 END) AS general_tickets,
        SUM(CASE WHEN ticket_type = 'Student' THEN quantity ELSE 0 END) AS student_tickets,
        SUM(CASE WHEN ticket_type = 'VIP' THEN quantity ELSE 0 END) AS vip_tickets,
        
        -- Data quality metrics
        AVG(ingestion_lag_seconds) AS avg_ingestion_lag_seconds,
        MAX(ingestion_lag_seconds) AS max_ingestion_lag_seconds,
        
        CURRENT_TIMESTAMP AS last_updated_at
        
    FROM enriched_tickets
    GROUP BY 1, 2, 3, 4, 5
)

SELECT * FROM daily_aggregates
ORDER BY sale_date DESC, total_revenue DESC