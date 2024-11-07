WITH post_comments AS (
    SELECT
        c.postid,
        c.id AS comment_id,
        c.creationdate,
        c.text,
        row_number() OVER (
            PARTITION BY c.postid
            ORDER BY c.creationdate
        ) AS comments_position
    FROM comments c
    INNER JOIN posts p ON c.postid = p.id
    INNER JOIN post_tags pt ON p.id = pt.post_id
    INNER JOIN tags t ON pt.tag_id = t.id
    WHERE t.tagname = %(tagname)s
)
SELECT
    postid AS post_id,
    comment_id,
    creationdate,
    text
FROM post_comments
WHERE comments_position = %(position)s
ORDER BY creationdate
LIMIT %(limit)s;
