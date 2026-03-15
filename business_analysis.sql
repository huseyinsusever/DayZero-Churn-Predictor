-- ==========================================================
-- PLAYER RETENTION & CHURN ANALYTICS SCRIPT
-- Purpose: Extracting actionable insights from Day-0 behavior
-- ==========================================================

-- 1. DAILY CHURN PREDICTION SUMMARY
-- Goal: Monitor the health of the game by tracking daily predicted churn rates.
SELECT 
    DATE(timestamp) as report_date,
    COUNT(id) as total_predictions,
    ROUND(AVG(churn_prob) * 100, 2) as predicted_churn_percentage,
    SUM(CASE WHEN churn_prob > 0.8 THEN 1 ELSE 0 END) as high_risk_players
FROM churn_logs
GROUP BY 1
ORDER BY 1 DESC;

-- 2. CORRELATION ANALYSIS: SESSIONS VS. CHURN
-- Goal: Determine if higher session counts actually reduce churn risk.
-- This helps the Product Team decide on session-based rewards.
SELECT 
    session_count,
    COUNT(id) as player_count,
    ROUND(AVG(churn_prob), 3) as avg_risk_score
FROM churn_logs
GROUP BY 1
HAVING player_count > 5
ORDER BY session_count ASC;

-- 3. SEGMENTATION FOR MARKETING (The "Whale" Potential)
-- Goal: Identify active players (session_count > 5) who are still at risk.
-- These are the players we should target with a "Special Offer" email.
WITH HighValueAtRisk AS (
    SELECT * FROM churn_logs
    WHERE session_count >= 5 AND churn_prob > 0.7
)
SELECT 
    id, 
    timestamp, 
    session_count, 
    churn_prob 
FROM HighValueAtRisk
ORDER BY churn_prob DESC;

-- 4. PEER BENCHMARKING (Advanced: Window Functions)
-- Goal: Compare a player's session count to the average of that day.
-- Apple loves Window Functions like AVG() OVER()!
SELECT 
    id,
    session_count,
    AVG(session_count) OVER(PARTITION BY DATE(timestamp)) as daily_avg_sessions,
    churn_prob
FROM churn_logs
LIMIT 20;
