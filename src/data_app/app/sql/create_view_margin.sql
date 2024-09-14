CREATE OR REPLACE VIEW margin_view AS
WITH margin_data AS (
    SELECT
        ingestion_date,
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractFloat(line_data, 'custo') AS custo,
        line_data
    FROM working_data
    WHERE tag = 'sku_cost'
),
price_data AS (
    SELECT
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractFloat(line_data, 'preco') AS preco
    FROM working_data
    WHERE tag = 'sku_price'
),
year_data AS (
    SELECT
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractString(line_data, 'data') AS data_referencia
    FROM working_data
    WHERE tag = 'transaction_fact_v6_2024'
),
sku_data AS (
    SELECT
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractString(line_data, 'categoria') AS categoria,
        JSONExtractString(line_data, 'sub_categoria') AS sub_categoria,
        JSONExtractString(line_data, 'descricao') AS descricao,
        JSONExtractString(line_data, 'nome_completo') AS nome_completo,
        JSONExtractString(line_data, 'marca') AS marca
    FROM working_data
    WHERE tag = 'sku_dataset'
),
store_data AS (
    SELECT
        JSONExtractString(line_data, 'nome_loja') AS nome_loja,
        JSONExtractString(line_data, 'regiao') AS regiao
    FROM working_data
    WHERE tag = 'store_final'
)

SELECT
    md.ingestion_date,
    md.cod_prod,
    pd.preco,
    md.custo,
    sd.regiao,
    skd.categoria,
    skd.sub_categoria,
    skd.descricao,
    skd.nome_completo,
    skd.marca,
    yd.data_referencia,
    ((pd.preco - md.custo) / pd.preco) * 100 AS margem_lucro_bruto,
    (pd.preco - md.custo) / pd.preco AS lucro_bruto_financeiro,
    avg(((pd.preco - md.custo) / pd.preco) * 100) OVER (PARTITION BY sd.regiao) AS margem_lucro_bruto_regiao
FROM 
    margin_data md
INNER JOIN 
    price_data pd 
    ON md.cod_prod = pd.cod_prod
INNER JOIN 
    year_data yd 
    ON md.cod_prod = yd.cod_prod
INNER JOIN 
    sku_data skd 
    ON md.cod_prod = skd.cod_prod
LEFT JOIN 
    store_data sd 
    ON JSONExtractString(md.line_data, 'cod_loja') = sd.nome_loja;
