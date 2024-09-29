CREATE OR REPLACE VIEW view_remuneracao_gerente AS
WITH transacoes AS (
    SELECT
        JSONExtractString(line_data, 'cod_loja') AS cod_loja,
        JSONExtractFloat(line_data, 'preco') AS preco,
        toDate(JSONExtractString(line_data, 'data')) AS data,  -- Converte string para Date
        toMonth(toDate(JSONExtractString(line_data, 'data'))) AS mes,  -- Aplica toMonth sobre o campo Date
        toYear(toDate(JSONExtractString(line_data, 'data'))) AS ano  -- Aplica toYear sobre o campo Date
    FROM working_data
    WHERE tag IN ('transaction_fact_v6_2022', 'transaction_fact_v6_2023', 'transaction_fact_v6_2024')
),
target_loja AS (
    SELECT
        JSONExtractString(line_data, 'store_id') AS cod_loja,
        JSONExtractFloat(line_data, 'sales_target') AS sales_target,
        toMonth(toDate(concat(substring(JSONExtractString(line_data, 'month'), 4, 4), '-', substring(JSONExtractString(line_data, 'month'), 1, 2), '-01'))) AS mes,  -- Converte string para Date e aplica toMonth
        toYear(toDate(concat(substring(JSONExtractString(line_data, 'month'), 4, 4), '-', substring(JSONExtractString(line_data, 'month'), 1, 2), '-01'))) AS ano  -- Converte string para Date e aplica toYear
    FROM working_data
    WHERE tag = 'target_store_final_v6'
),
lojas AS (
    SELECT
        JSONExtractString(line_data, 'nome_loja') AS nome_loja,
        JSONExtractString(line_data, 'regiao') AS regiao
    FROM working_data
    WHERE tag = 'store_final'
)
SELECT
    t.cod_loja,
    t.mes,
    t.ano,
    SUM(t.preco) AS total_vendas,
    tg.sales_target AS target,
    l.regiao
FROM
    transacoes t
INNER JOIN
    target_loja tg ON t.cod_loja = tg.cod_loja AND t.mes = tg.mes AND t.ano = tg.ano
LEFT JOIN
    lojas l ON t.cod_loja = l.nome_loja
GROUP BY
    t.cod_loja, t.mes, t.ano, tg.sales_target, l.regiao
ORDER BY
    t.cod_loja, t.mes, t.ano;
