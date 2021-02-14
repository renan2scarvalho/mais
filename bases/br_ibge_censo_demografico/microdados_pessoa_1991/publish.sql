/*

Query para publicar a tabela.

Esse é o lugar para:
    - modificar nomes, ordem e tipos de colunas
    - dar join com outras tabelas
    - criar colunas extras (e.g. logs, proporções, etc.)

Qualquer coluna definida aqui deve também existir em `table_config.yaml`.

# Além disso, sinta-se à vontade para alterar alguns nomes obscuros
# para algo um pouco mais explícito.

TIPOS:
    - Para modificar tipos de colunas, basta substituir STRING por outro tipo válido.
    - Exemplo: `SAFE_CAST(column_name AS NUMERIC) column_name`
    - Mais detalhes: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types

*/

CREATE VIEW basedosdados-dev.br_ibge_censo_demografico.microdados_pessoa_1991 AS
SELECT 
SAFE_CAST(id_municipio AS STRING) id_municipio,
SAFE_CAST(id_questionario AS STRING) id_questionario,
SAFE_CAST(numero_ordem AS STRING) numero_ordem,
SAFE_CAST(v0301 AS STRING) v0301,
SAFE_CAST(v0302 AS STRING) v0302,
SAFE_CAST(v0303 AS STRING) v0303,
SAFE_CAST(v0304 AS STRING) v0304,
SAFE_CAST(v2011 AS STRING) v2011,
SAFE_CAST(v3041 AS STRING) v3041,
SAFE_CAST(v3042 AS STRING) v3042,
SAFE_CAST(v3043 AS STRING) v3043,
SAFE_CAST(v3044 AS STRING) v3044,
SAFE_CAST(v3045 AS STRING) v3045,
SAFE_CAST(v3046 AS STRING) v3046,
SAFE_CAST(v3047 AS STRING) v3047,
SAFE_CAST(v3049 AS STRING) v3049,
SAFE_CAST(v3005 AS STRING) v3005,
SAFE_CAST(v3071 AS STRING) v3071,
SAFE_CAST(v3072 AS STRING) v3072,
SAFE_CAST(v3073 AS STRING) v3073,
SAFE_CAST(v0309 AS STRING) v0309,
SAFE_CAST(v0311 AS STRING) v0311,
SAFE_CAST(v0312 AS STRING) v0312,
SAFE_CAST(v0313 AS STRING) v0313,
SAFE_CAST(v0314 AS STRING) v0314,
SAFE_CAST(v3151 AS STRING) v3151,
SAFE_CAST(v3152 AS STRING) v3152,
SAFE_CAST(v0316 AS STRING) v0316,
SAFE_CAST(v0317 AS STRING) v0317,
SAFE_CAST(v0318 AS STRING) v0318,
SAFE_CAST(v0319 AS STRING) v0319,
SAFE_CAST(v3191 AS STRING) v3191,
SAFE_CAST(v0320 AS STRING) v0320,
SAFE_CAST(v0321 AS STRING) v0321,
SAFE_CAST(v3211 AS STRING) v3211,
SAFE_CAST(v0322 AS STRING) v0322,
SAFE_CAST(v0323 AS STRING) v0323,
SAFE_CAST(v0324 AS STRING) v0324,
SAFE_CAST(v0325 AS STRING) v0325,
SAFE_CAST(v0326 AS STRING) v0326,
SAFE_CAST(v0327 AS STRING) v0327,
SAFE_CAST(v0328 AS STRING) v0328,
SAFE_CAST(v3241 AS STRING) v3241,
SAFE_CAST(v0329 AS STRING) v0329,
SAFE_CAST(v0330 AS STRING) v0330,
SAFE_CAST(v3311 AS STRING) v3311,
SAFE_CAST(v3312 AS STRING) v3312,
SAFE_CAST(v0332 AS STRING) v0332,
SAFE_CAST(v0333 AS STRING) v0333,
SAFE_CAST(v3341 AS STRING) v3341,
SAFE_CAST(v3342 AS STRING) v3342,
SAFE_CAST(v0345 AS STRING) v0345,
SAFE_CAST(v0346 AS STRING) v0346,
SAFE_CAST(v3461 AS STRING) v3461,
SAFE_CAST(v0347 AS STRING) v0347,
SAFE_CAST(v3471 AS STRING) v3471,
SAFE_CAST(v0349 AS STRING) v0349,
SAFE_CAST(v0350 AS STRING) v0350,
SAFE_CAST(v0351 AS STRING) v0351,
SAFE_CAST(v0352 AS STRING) v0352,
SAFE_CAST(v0353 AS STRING) v0353,
SAFE_CAST(v0354 AS STRING) v0354,
SAFE_CAST(v0355 AS STRING) v0355,
SAFE_CAST(v0356 AS STRING) v0356,
SAFE_CAST(v3561 AS STRING) v3561,
SAFE_CAST(v3562 AS STRING) v3562,
SAFE_CAST(v3563 AS STRING) v3563,
SAFE_CAST(v3564 AS STRING) v3564,
SAFE_CAST(v0357 AS STRING) v0357,
SAFE_CAST(v3574 AS STRING) v3574,
SAFE_CAST(v0358 AS STRING) v0358,
SAFE_CAST(v0359 AS STRING) v0359,
SAFE_CAST(v0360 AS STRING) v0360,
SAFE_CAST(v3604 AS STRING) v3604,
SAFE_CAST(v0361 AS STRING) v0361,
SAFE_CAST(v3614 AS STRING) v3614,
SAFE_CAST(v3351 AS STRING) v3351,
SAFE_CAST(v3352 AS STRING) v3352,
SAFE_CAST(v3353 AS STRING) v3353,
SAFE_CAST(v3354 AS STRING) v3354,
SAFE_CAST(v3355 AS STRING) v3355,
SAFE_CAST(v3356 AS STRING) v3356,
SAFE_CAST(v3360 AS STRING) v3360,
SAFE_CAST(v3361 AS STRING) v3361,
SAFE_CAST(v3362 AS STRING) v3362,
SAFE_CAST(v0335 AS STRING) v0335,
SAFE_CAST(v0336 AS STRING) v0336,
SAFE_CAST(v0337 AS STRING) v0337,
SAFE_CAST(v0338 AS STRING) v0338,
SAFE_CAST(v0339 AS STRING) v0339,
SAFE_CAST(v0340 AS STRING) v0340,
SAFE_CAST(v3357 AS STRING) v3357,
SAFE_CAST(v0341 AS STRING) v0341,
SAFE_CAST(v0342 AS STRING) v0342,
SAFE_CAST(v0343 AS STRING) v0343,
SAFE_CAST(v3443 AS STRING) v3443,
SAFE_CAST(v3444 AS STRING) v3444,
SAFE_CAST(v0310 AS STRING) v0310,
SAFE_CAST(v7301 AS STRING) v7301,
SAFE_CAST(sigla_uf AS STRING) sigla_uf
from basedosdados-dev.br_ibge_censo_demografico_staging.microdados_pessoa_1991 as t