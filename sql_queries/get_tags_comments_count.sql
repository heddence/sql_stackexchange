WITH filtered_posts AS (
    SELECT p.id
    FROM posts p
    JOIN post_tags pt ON p.id = pt.post_id
    JOIN tags t ON pt.tag_id = t.id
    WHERE t.tagname = %(tagname)s
    GROUP BY p.id, p.commentcount
    HAVING count(*) > 0 AND p.commentcount > 10
),
ordered_comments AS (
    SELECT
        c.postid,
        c.id AS comment_id,
        c.creationdate,
        row_number() OVER (
            PARTITION BY c.postid
            ORDER BY c.creationdate
        ) AS comment_seq,
        round(extract(
            EPOCH FROM (
                c.creationdate - lag(c.creationdate) OVER (
                    PARTITION BY c.postid
                    ORDER BY c.creationdate
                )
            )
        ), 2) AS response_time
    FROM comments c
    WHERE c.postid IN (SELECT id FROM filtered_posts)
),
comments_with_avg_response_time AS (
    SELECT
        oc.postid,
        oc.comment_seq,
        oc.comment_id,
        oc.creationdate,
        oc.response_time,
        round(sum(oc.response_time) OVER (
            PARTITION BY oc.postid
            ORDER BY oc.comment_seq
        ) / nullif(oc.comment_seq - 1, 0), 2) AS avg_response_time
    FROM ordered_comments oc
    WHERE oc.comment_seq > %(comments_count)s
)
SELECT
    postid AS post_id,
    comment_seq,
    comment_id,
    creationdate,
    response_time,
    avg_response_time
FROM comments_with_avg_response_time
ORDER BY postid, comment_seq;
