SELECT UTD,TURMA, CARTEIRA,DATA_PEDIDO, COUNT(ZCGACCOUN) AS NOTAS_DEFASAGEM_ATENA FROM (
SELECT 
	AH.ZCGACCOUN,
	ZCGUTD AS UTD,
	ZCGMTVCOB,
	CASE WHEN CARTEIRA = 'DISJUNTOR' OR CARTEIRA = 'DISJUNTOR MIX' THEN 'DISJUNTOR' 
	WHEN CARTEIRA = 'RECORTE MIX' OR CARTEIRA = 'RECORTE' THEN 'RECORTE'
	WHEN CARTEIRA = 'CONVENCIONAL' THEN 'CORTE'
	WHEN CARTEIRA = 'BAIXA MIX' OR CARTEIRA = 'BAIXA' THEN 'BAIXA' END AS CARTEIRA,
	TURMA,
	DATA_PEDIDO,
	DAYOFWEEK(DATA_PEDIDO) AS DIA_SEMANA,
	ZCGIDZONA AS ZONA,
	FLAG_DEF

FROM CLB961920.ATENA_HIST AH
WHERE DATA_PEDIDO = '{data_consulta}'
AND FLAG_DEF = 'S')
GROUP BY UTD,TURMA, CARTEIRA,DATA_PEDIDO