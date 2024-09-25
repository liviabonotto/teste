CREATE VIEW IF NOT EXISTS product_view AS
SELECT
    ingestion_date,
    JSONExtractString(line_data, 'categoria') AS categoria,
    JSONExtractString(line_data, 'sub_categoria') AS sub_categoria,
    JSONExtractString(line_data, 'marca') AS marca,
    tag
FROM
    working_data
WHERE
    tag = 'sku_dataset';