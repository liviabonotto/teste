CREATE VIEW IF NOT EXISTS cost_view AS
SELECT
    ingestion_date,
    JSONExtractString(line_data, 'cod_prod') AS cod_prod,
    JSONExtractString(line_data, 'data_inicio') AS data_inicio_custo,
    JSONExtractString(line_data, 'data_fim') AS data_fim_custo,
    JSONExtractFloat(line_data, 'custo') AS custo,
    tag
FROM
    working_data
WHERE
    tag = 'sku_cost';