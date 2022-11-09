SELECT 
ZCGPARTNR AS PARCEIRO,ZCGINSTAL AS INSTALACAO,ZCGDSCNAE AS CNAE, 
ZCGSITUCC AS SITUACAO,ZCGNMLOGR AS RUA, LOCALIDADE, PC.ZCGBAIRR AS BAIRRO, MUNICIPIO, SETOR40 AS SETOR, UTD40 AS UTD,ZCGNNVLAD,
pc.ZCGACCOUN as CONTA_CONTRATO,ZCGLATITU AS LATITUDE,ZCGLONGIT AS LONGITUDE, ZONA,PECLD  FROM CLP123432.PLANILHAO_CLIENTE AS PC

LEFT JOIN (SELECT max(DATAREF) AS dataref,ZONA, ZCGBAIRRO,ZCGMUNICI
FROM CLB961920.SUSCETIVEIS
GROUP BY ZONA, ZCGBAIRRO,ZCGMUNICI) susc
ON susc.ZCGBAIRRO = PC.ZCGBAIRR AND susc.ZCGMUNICI = PC.MUNICIPIO

LEFT JOIN	
(SELECT DISTINCT
	dun.ZCGACCOUN, dun.ZCGNNVLAD,
	RANK() OVER ( PARTITION BY dun.ZCGACCOUN ORDER BY dun.ZCGDTVENC DESC ) AS prio
FROM CLB_CCS_ICC.ZCT_DS_DUN001 dun
) AS tab_suscetivel
ON 	PC.ZCGACCOUN = tab_suscetivel.ZCGACCOUN AND tab_suscetivel.prio = 1


left join (SELECT 
ZCGVKONT AS CONTA_CONTRATO,
SUM (ZCGBETRW) AS CR,
SUM (zcgpecldaloc) AS PECLD

FROM CLB_CCS_ICC.ZCT_DS_CARGA_AGING_COELBA
group by ZCGVKONT) as base_pecld
ON base_pecld.CONTA_CONTRATO = PC.ZCGACCOUN


WHERE SEQCC = 1 
AND ZCGLATITU IS NOT NULL
AND PC.ZCGACCOUN IN ({lista_consultar})
