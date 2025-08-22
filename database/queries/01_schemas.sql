WITH table_columns AS (
    SELECT
        table_schema,
        table_name,
        column_name,
        data_type,
        is_nullable,
        column_default
    FROM
        information_schema.columns
    WHERE
        table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY
        table_schema,
        table_name,
        ordinal_position
)
SELECT
    table_schema,
    table_name,
    json_agg(
        json_build_object(
            'column_name',
            column_name,
            'data_type',
            data_type,
            'is_nullable',
            is_nullable,
            'column_default',
            column_default
        )
    ) AS columns
FROM
    table_columns
GROUP BY
    table_schema,
    table_name
ORDER BY
    table_schema,
    table_name;