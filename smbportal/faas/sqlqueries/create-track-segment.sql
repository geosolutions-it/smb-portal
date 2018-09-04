-- this next query over-simplifies the problem
--
-- INSERT INTO tracks_segment (
--   track_id,
--   user_uuid,
--   vehicle_type,
--   geom,
--   start_date,
--   end_date
-- )
-- SELECT
--   pts.track_id AS track_id,
--   %(user_uuid)s,
--   %(vehicle_type)s,
--   ST_MakeLine(pts.the_geom) AS geom,
--   MIN(pts.timestamp) AS start,
--   MAX(pts.timestamp) AS end
-- FROM (
--   SELECT track_id, the_geom, timestamp
--   FROM tracks_collectedpoint
--   WHERE track_id = %(track_id)s
--   AND vehicle_type = %(vehicle_type)s
-- ) AS pts
-- GROUP BY pts.track_id

-- we need something like this
-- SELECT
--   id,
--   timestamp,
--   vehicle_type,
--   vehicle_type = lag(vehicle_type, 1) OVER (ORDER BY timestamp ASC)
-- FROM tracks_collectedpoint
-- WHERE track_id = %(track_id)s


-- canon
SELECT
  track_id AS track_id,
  clustr AS segment,
  vehicle_type AS vehicle_type,
  st_makeline(the_geom) AS the_geom,
  min(timestamp) AS start,
  max(timestamp) AS end
FROM (
  SELECT
    track_id,
    the_geom,
    timestamp,
    vehicle_type,
    SUM(CASE WHEN changed THEN 0 ELSE 1 END) OVER (ORDER BY timestamp ASC) AS clustr
    FROM (
      SELECT
        track_id,
        timestamp,
        the_geom,
        vehicle_type,
        vehicle_type = lag(vehicle_type, 1) OVER (ORDER BY timestamp ASC) AS changed
      FROM tracks_collectedpoint
      WHERE track_id = %(track_id)s
    ) AS sq
  ) as sq2
GROUP BY
  track_id,
  vehicle_type,
  clustr;