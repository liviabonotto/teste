CREATE OR REPLACE VIEW region_view AS
WITH transaction_fact_v6_2024 AS (
    SELECT
        toDateOrNull(JSONExtractString(line_data, 'data')) AS data, 
        JSONExtractString(line_data, 'cod_loja') AS cod_loja,
        JSONExtractString(line_data, 'cod_transacao') AS cod_transacao,
        toFloat32OrNull(JSONExtractString(line_data, 'preco')) AS preco
    FROM working_data
    WHERE tag = 'transaction_fact_v6_2024'
),
store_final AS (
    SELECT
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'nome_loja')) AS nome_loja, 
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'regiao')) AS regiao,
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'diretoria')) AS diretoria
    FROM working_data
    WHERE tag = 'store_final'
),
aggregated_data AS (
    SELECT
        sf.regiao AS regiao,
        sf.diretoria AS diretoria,
        formatDateTime(tf.data, '%Y-%m') AS mes,
        SUM(tf.preco) AS faturamento_total,
        COUNT(DISTINCT tf.cod_transacao) AS total_transacoes,
        SUM(tf.preco) / COUNT(DISTINCT tf.cod_transacao) AS ticket_medio
    FROM 
        transaction_fact_v6_2024 tf
    LEFT JOIN 
        store_final sf
    ON 
        tf.cod_loja = sf.nome_loja
    WHERE tf.preco IS NOT NULL
    GROUP BY 
        sf.regiao, sf.diretoria, formatDateTime(tf.data, '%Y-%m')
)

SELECT
    regiao,
    diretoria,
    mes,
    faturamento_total,
    ticket_medio
FROM 
    aggregated_data
ORDER BY 
    mes, regiao, diretoria;
