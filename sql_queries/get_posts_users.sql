SELECT
    u.id AS user_id,
    u.displayname AS display_name,
    u.reputation AS reputation,
    max(c.creationdate) AS last_comment_date
FROM
    comments c
JOIN
    users u ON c.userid = u.id
WHERE
    c.postid = %(postid)s
GROUP BY
    u.id, u.displayname, u.reputation
ORDER BY
    last_comment_date DESC;
