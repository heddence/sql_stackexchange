WITH RECURSIVE thread_posts AS (
    -- Anchor member: start with the post having ID = :postid
    SELECT
        p.id,
        p.parentid,
        p.creationdate,
        p.body,
        1 AS level
    FROM posts p
    WHERE p.id = %(postid)s

    UNION ALL

    -- Recursive member: find posts where ParentId matches ID from the previous level
    SELECT
        p.id,
        p.parentid,
        p.creationdate,
        p.body,
        tp.level + 1 AS level
    FROM posts p
    INNER JOIN thread_posts tp ON p.parentid = tp.id
)
SELECT *
FROM thread_posts
ORDER BY creationdate
LIMIT %(limit)s;
