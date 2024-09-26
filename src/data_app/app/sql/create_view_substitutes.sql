CREATE OR REPLACE VIEW substitute_view AS
WITH substitute_data AS (
    SELECT
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractString(line_data, 'descricao') AS descricao,
        JSONExtractString(line_data, 'categoria') AS categoria,
        JSONExtractString(line_data, 'sub_categoria') AS sub_categoria,
        JSONExtractFloat(line_data, 'conteudo_valor') AS conteudo_valor,
        JSONExtractString(line_data, 'conteudo_medida') AS conteudo_medida,
        JSONExtractString(line_data, 'marca') AS marca
    FROM working_data
    WHERE tag = 'sku_dataset'
),
stock_data AS (
    SELECT
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        JSONExtractString(line_data, 'cod_loja') AS cod_loja,
        JSONExtractFloat(line_data, 'quantidade') AS quantidade
    FROM working_data
    WHERE tag = 'daily_stock_dataset'
)

SELECT
    sd.cod_prod,
    sd.descricao,
    sd.categoria,
    sd.sub_categoria,
    sd.conteudo_valor,
    sd.conteudo_medida,
    sd.marca,
    stk.cod_loja,
    stk.quantidade
FROM 
    substitute_data sd
LEFT JOIN 
    stock_data stk
    ON sd.cod_prod = stk.cod_prod;
