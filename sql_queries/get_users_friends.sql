WITH relevant_posts AS (
    -- Posts created by the user
    SELECT DISTINCT p.id
    FROM posts p
    WHERE p.owneruserid = %(userid)s

    UNION

    -- Posts the user has commented on
    SELECT DISTINCT c.postid
    FROM comments c
    WHERE c.userid = %(userid)s
)
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
    c.postid IN (SELECT id FROM relevant_posts)
    AND c.userid != %(userid)s  -- Exclude the original user
GROUP BY
    u.id, u.displayname, u.reputation
ORDER BY
    last_comment_date DESC;
