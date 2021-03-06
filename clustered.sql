SELECT
  CONCAT(SUBSTR(CAST (timestamp AS STRING),0,4), SUBSTR(CAST (timestamp AS STRING),6,2), SUBSTR(CAST (timestamp AS STRING),9,2)) AS date,
  keyword,
  market,
  location,
  device,
  rank,
  base_rank,
  url,
  advertiser_competition,
  gms,
  rms,
  cpc,
  tags,
  CASE
    WHEN rank = 1 THEN "1. (1)"
    WHEN rank = 2 THEN "2. (2)"
    WHEN rank = 3 THEN "3. (3)"
    WHEN rank <= 10 THEN "4. (4-10)"
    WHEN rank <= 20 THEN "5. (11-20)"
    WHEN rank < 120 THEN "6. (21-119)"
    ELSE "NR"
  END AS grouping_strategy_a,
  CASE
    WHEN rank <= 3 THEN "1. (1-3)"
    WHEN rank <= 10 THEN "2. (4-10)"
    WHEN rank <= 20 THEN "3. (11-20)"
    WHEN rank < 120 THEN "4. (21-119)"
    ELSE "NR"
  END AS grouping_strategy_b,
  CASE
    WHEN rank <= 10 THEN "1"
    WHEN rank <= 20 THEN "2"
    WHEN rank <= 120 THEN "3+"
    ELSE "NR"
  END AS serp_page,
  ctr,
  CAST(ctr * gms AS INT64) AS estimated_global_sessions,
  CAST(ctr * rms AS INT64) AS estimated_regional_sessions,
  CAST(0.3 * gms AS INT64) AS maximum_global_sessions,
  CAST(0.3 * rms AS INT64) AS maximum_regional_sessions
FROM (
  SELECT
    stat.timestamp AS timestamp,
    stat.keyword AS keyword,
    stat.market AS market,
    stat.location AS location,
    stat.device AS device,
    stat.rank AS rank,
    stat.base_rank AS base_rank,
    stat.url AS url,
    stat.advertiser_competition AS advertiser_competition,
    stat.gms AS gms,
    stat.rms AS rms,
    stat.cpc AS cpc,
    stat.tags AS tags,
    ctrs.calculated AS ctr
  FROM
    `bq-stat.%CLIENT%.stat` AS stat
  LEFT JOIN
    `bq-stat.stat_config.ctrs` AS ctrs
  ON
    stat.rank = ctrs.rank)
