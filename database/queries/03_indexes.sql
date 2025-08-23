SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    schemaname,
    tablename,
    indexname;