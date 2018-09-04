INSERT INTO tracks_segment (
  track_id,
  user_uuid,
  vehicle_type,
  geom,
  start_date,
  end_date
)
SELECT
  pts.track_id AS track_id,
  ST_MakeLine(pts.the_geom) AS geom,
  MIN(pts.timestamp) AS start,
  MAX(pts.timestamp) AS end
FROM (
  SELECT track_id, the_geom, timestamp
  FROM tracks_collectedpoint
  WHERE track_id = %(track_id)s
  AND vehicle_type = %(vehicle_type)s
) AS pts
GROUP BY pts.track_id
