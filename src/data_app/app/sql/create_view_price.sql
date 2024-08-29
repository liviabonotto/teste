CREATE VIEW IF NOT EXISTS price_view AS
SELECT
    ingestion_date,
    JSONExtractString(line_data, 'cod_prod') AS cod_prod,
    JSONExtractString(line_data, 'data_inicio') AS data_inicio_preco,
    JSONExtractString(line_data, 'data_fim') AS data_fim_preco,
    JSONExtractFloat(line_data, 'preco') AS preco,
    tag
FROM
    working_data
WHERE
    tag = 'sku_price';