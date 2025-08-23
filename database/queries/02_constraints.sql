-- Primary Key Constraints
SELECT
    tc.table_schema,
    tc.table_name,
    kcu.column_name AS primary_key_column
FROM
    information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE
    tc.constraint_type = 'PRIMARY KEY'
ORDER BY
    tc.table_schema,
    tc.table_name;

-- Foreign Key Constraints
SELECT
    tc.table_schema,
    tc.table_name,
    kcu.column_name AS foreign_key_column,
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM
    information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
WHERE
    tc.constraint_type = 'FOREIGN KEY'
ORDER BY
    tc.table_schema,
    tc.table_name;