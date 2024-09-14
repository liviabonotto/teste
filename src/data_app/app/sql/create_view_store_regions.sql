CREATE OR REPLACE VIEW region_view AS
WITH transaction_fact_v6_2024 AS (
    SELECT
        toDateOrNull(JSONExtractString(line_data, 'data')) AS data, 
        JSONExtractString(line_data, 'cod_vendedor') AS cod_vendedor,
        JSONExtractString(line_data, 'cod_loja') AS cod_loja,
        JSONExtractString(line_data, 'cod_transacao') AS cod_transacao,
        JSONExtractString(line_data, 'cod_prod') AS cod_prod,
        toInt32OrNull(JSONExtractString(line_data, 'quantidade')) AS quantidade, 
        toFloat32OrNull(JSONExtractString(line_data, 'preco')) AS preco, 
        toFloat32OrNull(JSONExtractString(line_data, 'total')) AS total 
    FROM working_data
    WHERE tag = 'transaction_fact_v6_2024'
),
store_final AS (
    SELECT
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'nome_loja')) AS nome_loja, -- Remover espaços
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'regiao')) AS regiao,
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'diretoria')) AS diretoria
    FROM working_data
    WHERE tag = 'store_final'
),
employee_final AS (
    SELECT
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'name')) AS name, -- Remover espaços
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'surname')) AS surname,
        JSONExtractString(line_data, 'id_employee') AS cod_vendedor,
        trim(BOTH ' ' FROM JSONExtractString(line_data, 'role')) AS role_vendedor
    FROM working_data
    WHERE tag = 'employee_final'
)

SELECT
    CONCAT(ef.name, ' ', ef.surname) AS nome_vendedor, 
    ef.role_vendedor AS role,
    sf.nome_loja AS loja,
    sf.regiao AS regiao,
    sf.diretoria AS diretoria,
    tf.data AS data,
    tf.cod_vendedor AS cod_vendedor,
    tf.cod_loja AS cod_loja,
    tf.cod_transacao AS cod_transacao,
    tf.cod_prod AS cod_prod,
    tf.quantidade AS quantidade,
    tf.preco AS preco,
    tf.total AS total
FROM 
    transaction_fact_v6_2024 tf
LEFT JOIN 
    store_final sf
ON 
    tf.cod_loja = sf.nome_loja
LEFT JOIN 
    employee_final ef
ON 
    tf.cod_vendedor = ef.cod_vendedor;
