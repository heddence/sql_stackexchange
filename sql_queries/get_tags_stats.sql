WITH total_posts AS (
    -- Calculate total number of posts per day of the week
    SELECT
        to_char(p.creationdate, 'FMDay') AS day_of_week,
        count(*) AS total_posts
    FROM
        posts p
    GROUP BY
        to_char(p.creationdate, 'FMDay')
),
tagged_posts AS (
    -- Calculate number of posts with the specified tag per day of the week
    SELECT
        to_char(p.creationdate, 'FMDay') AS day_of_week,
        count(*) AS tagged_posts
    FROM
        posts p
    JOIN
        post_tags pt ON p.id = pt.post_id
    JOIN
        tags t ON pt.tag_id = t.id
    WHERE
        t.tagname ILIKE %(tagname)s
    GROUP BY
        to_char(p.creationdate, 'FMDay')
)
SELECT
    tp.day_of_week AS day,
    round(
        ((coalesce(tp_tag.tagged_posts, 0)::FLOAT / coalesce(tp.total_posts, 1)) * 100)::NUMERIC,
        2
    ) AS percentage
FROM
    total_posts tp
LEFT JOIN
    tagged_posts tp_tag ON tp.day_of_week = tp_tag.day_of_week
ORDER BY
    CASE
        WHEN tp.day_of_week = 'Monday' THEN 1
        WHEN tp.day_of_week = 'Tuesday' THEN 2
        WHEN tp.day_of_week = 'Wednesday' THEN 3
        WHEN tp.day_of_week = 'Thursday' THEN 4
        WHEN tp.day_of_week = 'Friday' THEN 5
        WHEN tp.day_of_week = 'Saturday' THEN 6
        WHEN tp.day_of_week = 'Sunday' THEN 7
    END;
