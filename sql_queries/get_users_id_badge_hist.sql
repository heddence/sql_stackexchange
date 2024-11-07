WITH badges_with_prev_post AS (
    SELECT
        b.id AS badge_id,
        b.name AS badge_name,
        b.date AS badge_date,
        (
            SELECT p.id
            FROM posts p
            WHERE p.owneruserid = b.userid
              AND p.creationdate < b.date
            ORDER BY p.creationdate DESC
            LIMIT 1
        ) AS prev_post_id
    FROM badges b
    WHERE b.userid = %(userid)s
),
filtered_badges AS (
    SELECT *
    FROM badges_with_prev_post
),
ranked_badges AS (
    SELECT
        *,
        row_number() OVER (PARTITION BY prev_post_id ORDER BY badge_date DESC) AS badge_rank_per_post
    FROM filtered_badges
),
last_badge_per_post AS (
    SELECT *
    FROM ranked_badges
    WHERE badge_rank_per_post = 1
),
unique_badges AS (
    SELECT
        *,
        row_number() OVER (PARTITION BY badge_name ORDER BY badge_date DESC) AS badge_rank
    FROM last_badge_per_post
)
SELECT
    badge_name,
    prev_post_id AS post_id,
    p.creationdate AS post_date,
    p.body AS post_body
FROM unique_badges ub
JOIN posts p ON p.Id = ub.prev_post_id
WHERE ub.badge_rank = 1
ORDER BY badge_date;
