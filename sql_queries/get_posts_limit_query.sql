SELECT
    p.id,
    p.title,
    p.creationdate,
    p.body,
    coalesce(json_agg(t.tagname) FILTER (WHERE t.tagname IS NOT NULL), '[]') AS tags
FROM
    posts p
LEFT JOIN
    post_tags pt ON p.id = pt.post_id
LEFT JOIN
    tags t ON pt.tag_id = t.id
WHERE
    (p.title ILIKE %(query)s OR p.body ILIKE %(query)s)
    AND p.title IS NOT NULL
    AND p.body IS NOT NULL
GROUP BY
    p.id, p.title, p.creationdate, p.closeddate, p.body
ORDER BY
    p.creationdate DESC
LIMIT %(limit)s;
