SELECT UTD, TURMA, CARTEIRA, SUM(QTD_PENDENTES) AS QTD_PENDENTES FROM (
--ABAIXO ORIGINAL POR ZONA

SELECT 
--ADD_MONTHS(NEXT_DAY(LAST_DAY(CURRENT_DATE)),-1) ,
UTD40 AS UTD,TURMA, 
--ZCGTPNOTA AS TIPO_NOTA, 
ZONA,

SUM(QTDE) AS QTD_PENDENTES, 
SUM(PECLD) AS PECLD_PENDENTES,  
SUM(PECLD)/SUM(QTDE) AS TICKET_PECLD_PENDENTES,
CASE 
	WHEN ZCGTPNOTA = 'CS' THEN 'CORTE' 
	WHEN ZCGTPNOTA = 'CA' THEN 'RECORTE'
	WHEN ZCGTPNOTA = 'CB' THEN 'BAIXA' END AS CARTEIRA
FROM (
SELECT 
 CL.REGIONAL40,
 CL.SETOR40,
 CL.UTD40,	 
 ZONA,
 BASE.ZCGTPNOTA,
 BASE.ZCGDTNOTA,
 
 BASE.ZCGDTENCE,

 COUNT(DISTINCT BASE.ZCGQMNUM) AS QTDE,
 SUM(MP.ZCGMTVCOB) AS MONT_VENC,
SUM(MP.PECLD_CONS) AS PECLD,
 CASE WHEN UPPER(BASE.ZCGTXTCOD) LIKE '%TELE%' OR BASE.ZCGCTTRAB = 'RPT161' OR LEFT(RIGHT(CL.ZCGUNLEIT,3),1)='R' THEN 'REMOTO'
 	  WHEN UPPER(BASE.ZCGTXTCOD) LIKE '% PRONTIDAO' AND BASE.ZCGTPNOTA IN ('CS','CA') THEN 'PRONTIDAO'
	  WHEN LEFT(BASE.ZCGCTTRAB,1) IN ('1','2') THEN 'STC'
		WHEN BASE.ZCGTPNOTA IN ('CS','CA') AND BASE.ZCGCTTRAB = CT.CT THEN 'PRONTIDAO'
	  
	  ELSE 'EPS'
 END AS TURMA
 
FROM CLB_CCS_ICC.ZCT_DS_TAB004 AS BASE
 	
LEFT JOIN (SELECT DISTINCT ZCGACCOUN, ZCGMTVCOB, PECLD_CONS, DATA_CRIACAO 
		 FROM CLB142840.MPRED_HIST
		 WHERE DATA_CRIACAO BETWEEN ADD_DAYS((ADD_MONTHS(NEXT_DAY(LAST_DAY(CURRENT_DATE)),-1)),-6) AND (CURRENT_DATE)
		 ORDER BY DATA_CRIACAO DESC
		 ) AS MP
	ON  BASE.ZCGACCOUN = MP.ZCGACCOUN
	AND MP.DATA_CRIACAO BETWEEN ADD_DAYS(BASE.ZCGDTNOTA,-6) AND BASE.ZCGDTNOTA

LEFT JOIN CLP123432.PLANILHAO_CLIENTE CL ON BASE.ZCGACCOUN = CL.ZCGACCOUN  

LEFT JOIN CLB142840.CT_PRONT AS CT --TABELA DE TURMAS DA PRONTIDAO
	ON BASE.ZCGCTTRAB = CT.CT AND ((BASE.ZCGDTFINA BETWEEN CT.DE AND CT.ATE) OR (BASE.ZCGDTFINA='19000101' AND BASE.ZCGDTNOTA BETWEEN CT.DE AND CT.ATE))

LEFT JOIN (SELECT ZCGACCOUN, ZONA, RANK() OVER ( PARTITION BY ZCGACCOUN ORDER BY DATAREF DESC ) AS rank_sus FROM CLB961920.SUSCETIVEIS
WHERE DATAREF < ADD_DAYS(CURRENT_DATE,40) ) SUSCETIVEIS_ZONAS
ON SUSCETIVEIS_ZONAS.ZCGACCOUN = BASE.ZCGACCOUN AND rank_sus = 1

WHERE   (BASE.ZCGTPNOTA IN ('CS','CA') OR (BASE.ZCGTPNOTA = 'CB' AND UPPER(BASE.ZCGTXTCOD) NOT LIKE '%PED%'))
	AND BASE.ZCGDTNOTA BETWEEN (ADD_MONTHS(NEXT_DAY(LAST_DAY(CURRENT_DATE)),-1)) AND (CURRENT_DATE)
	AND BASE.ZCGQMNUM NOT IN (SELECT DISTINCT ZCGQMNUM FROM CLB142840.B100) 
	AND (BASE.ZCGDTFINA = '1900-01-01')
	AND BASE.ZCGCTTRAB NOT IN ('JF1521','1LA000') 
	AND BASE.ZCGUSRSTS IN ('CRIA','REDI','VLIB','RLIB','DESP','CRRE','RETI')
	
	
	
	
GROUP BY CL.REGIONAL40,	CL.SETOR40, CL.UTD40,ZONA,
	BASE.ZCGDTNOTA,
	BASE.ZCGTPNOTA,
	  BASE.ZCGDTENCE,
	 CASE WHEN UPPER(BASE.ZCGTXTCOD) LIKE '%TELE%' OR BASE.ZCGCTTRAB = 'RPT161' OR LEFT(RIGHT(CL.ZCGUNLEIT,3),1)='R' THEN 'REMOTO'
		  WHEN UPPER(BASE.ZCGTXTCOD) LIKE '% PRONTIDAO' AND BASE.ZCGTPNOTA IN ('CS','CA') THEN 'PRONTIDAO'
		  WHEN LEFT(BASE.ZCGCTTRAB,1) IN ('1','2') THEN 'STC'
		  WHEN BASE.ZCGTPNOTA IN ('CS','CA') AND BASE.ZCGCTTRAB = CT.CT THEN 'PRONTIDAO'
		  
		  ELSE 'EPS'
	 END
	
ORDER BY 
	BASE.ZCGDTENCE
	)
	GROUP BY 
	UTD40 ,TURMA, ZCGTPNOTA,ZONA



-- ACIMA ORIGINAL POR ZONA
)
GROUP BY UTD, TURMA, CARTEIRA
