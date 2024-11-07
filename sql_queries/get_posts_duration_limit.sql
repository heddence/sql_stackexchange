SELECT
    p.id,
    p.title,
    p.creationdate,
    p.closeddate,
    round(extract(EPOCH FROM (p.closeddate - p.creationdate)) / 60, 2) AS duration
FROM
    posts p
WHERE
    p.closeddate IS NOT NULL
    AND round(extract(EPOCH FROM (p.closeddate - p.creationdate)) / 60, 2) <= %(duration_in_minutes)s
ORDER BY
    p.closeddate DESC
LIMIT %(limit)s;
