DO BEGIN 

    DECLARE minPECLD REAL;
    DECLARE maxPECLD REAL;
    DECLARE maxSCORE REAL;
    DECLARE minSCORE REAL;
    DECLARE maxMTVCOB REAL;
    DECLARE minMTVCOB REAL;

    DECLARE CARTEIRA VARCHAR(255) = ('{carteira}');
    DECLARE DATA_PEDIDO_A DATE  = ('{data_pedido}');
    DECLARE TURMA VARCHAR(255) = ('{turma}');
    
    
    IF CARTEIRA = 'CONVENCIONAL' AND TURMA = 'STC' THEN
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 40 AND --40
           SC.ZCGMTVCOB > 80 AND  --90           
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            
        -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
             and SC.UTD not in (
                'AMARGOSA','IPIAU','RIBEIRA DO POMBAL','SANTO ANTONIO DE JESUS','TEIXEIRA DE FREITAS','VALENCA', -- 100
                'ALAGOINHAS','CAMACARI','FEIRA DE SANTANA SUL','GUANAMBI','LAURO DE FREITAS','VITORIA DA CONQUISTA', --70
                'ESPLANADA','ITAPETINGA','SERRINHA','PORTO SEGURO','JEQUIE',-- 60
                'BOM JESUS DA LAPA','IBOTIRAMA','ILHEUS','JACOBINA','JUAZEIRO','LUIS EDUARDO MAGALHAES','PIRAJA','PAULO AFONSO','EUNAPOLIS', -- 50
                'LIVRAMENTO DE NOSSA SENHORA','POSTO DA MATA' )--25 

        -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
          ------ ADICIONADO COMO MEDIDA PARA AUMENTAR TICKET PECLD 18.10.2022
        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 50 AND --50 
           SC.ZCGMTVCOB > 80 AND          
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('BOM JESUS DA LAPA','IBOTIRAMA','ILHEUS','JACOBINA','JUAZEIRO','LUIS EDUARDO MAGALHAES','PIRAJA','PAULO AFONSO','EUNAPOLIS')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis

        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 60 AND  --60
           SC.ZCGMTVCOB > 80 AND          
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('ESPLANADA','ITAPETINGA','SERRINHA','PORTO SEGURO','JEQUIE')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
        
        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 70 AND  --70
           SC.ZCGMTVCOB > 80 AND  --100        
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('ALAGOINHAS','CAMACARI','FEIRA DE SANTANA SUL','GUANAMBI','LAURO DE FREITAS','VITORIA DA CONQUISTA')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis

        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 90 AND --100
           SC.ZCGMTVCOB > 100 AND         
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('AMARGOSA','IPIAU','RIBEIRA DO POMBAL','SANTO ANTONIO DE JESUS','TEIXEIRA DE FREITAS','VALENCA')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
        ------ ADICIONADO COMO MEDIDA PARA AUMENTAR TICKET PECLD 18.10.2022
    union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 20 AND --25
           SC.ZCGMTVCOB > 45 AND     --45      
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('LIVRAMENTO DE NOSSA SENHORA','POSTO DA MATA')
    );
        
    ELSEIF CARTEIRA = 'CONVENCIONAL' AND TURMA = 'EPS' THEN
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.ZCGMTVCOB > 80 AND

            
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
 --PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
             and SC.UTD not in (
                'AMARGOSA','IPIAU','RIBEIRA DO POMBAL','SANTO ANTONIO DE JESUS','TEIXEIRA DE FREITAS','VALENCA', -- 100
                'ALAGOINHAS','CAMACARI','FEIRA DE SANTANA SUL','GUANAMBI','LAURO DE FREITAS','VITORIA DA CONQUISTA', --70
                'ESPLANADA','ITAPETINGA','SERRINHA','PORTO SEGURO','JEQUIE', -- 60
                'BOM JESUS DA LAPA','IBOTIRAMA','ILHEUS','JACOBINA','JUAZEIRO','LUIS EDUARDO MAGALHAES','PIRAJA','PAULO AFONSO','EUNAPOLIS', -- 50
                'LIVRAMENTO DE NOSSA SENHORA','POSTO DA MATA') --25 

        -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
        
        
         ------ ADICIONADO COMO MEDIDA PARA AUMENTAR TICKET PECLD 18.10.2022
        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 25 AND --25
            SC.ZCGMTVCOB > 80 AND
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('BOM JESUS DA LAPA','IBOTIRAMA','ILHEUS','JACOBINA','JUAZEIRO','LUIS EDUARDO MAGALHAES','PIRAJA','PAULO AFONSO','EUNAPOLIS')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis

        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 30 AND 
       SC.ZCGMTVCOB > 80 AND
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('ESPLANADA','ITAPETINGA','SERRINHA','PORTO SEGURO','JEQUIE')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
        
        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 35 AND --35
            SC.ZCGMTVCOB > 80 AND
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('ALAGOINHAS','CAMACARI','FEIRA DE SANTANA SUL','GUANAMBI','LAURO DE FREITAS','VITORIA DA CONQUISTA')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis

        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           SC.PECLD_CONS > 40 AND 
            SC.ZCGMTVCOB > 80 AND
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('AMARGOSA','IPIAU','RIBEIRA DO POMBAL','SANTO ANTONIO DE JESUS','TEIXEIRA DE FREITAS','VALENCA')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis
        ------ ADICIONADO COMO MEDIDA PARA AUMENTAR TICKET PECLD 18.10.2022
        
        
        
        
        union 

        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
           ACAO IN ('DISJ','CORTE') AND
           
           SC.ZCGMTVCOB > 35 AND           
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            -- acao para reduzir o valor minimo para utd com poucos suscetiveis
         and SC.UTD in ('LIVRAMENTO DE NOSSA SENHORA','POSTO DA MATA')
    -- PROVISORIO acao para reduzir o valor minimo para utd com poucos suscetiveis

    );
            
    ELSEIF CARTEIRA = 'DISJUNTOR' AND TURMA = 'EPS' THEN
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLP123432.PLANILHAO_CLIENTE PC ON PC.ZCGACCOUN = SC.ZCGACCOUN    
             JOIN CLB142840.DAG40 AS DAG1 ON PC.ZCGCDMUNI||PC.ZCGCODLOC||PC.ZCGCDBAIR = DAG1.ZCGCDMUNI||DAG1.ZCGCODLOC||DAG1.ZCGCDBAIR    
       AND DAG1.FLAG_GAV = 'S' -- desabilita aqui para liberar seleção fora do mapa    
       WHERE
           --ACAO IN ('DISJ','CORTE') AND SC.PECLD_CONS < 700 AND SC.ZCGMTVCOB < 700 AND 
           ACAO IN ('DISJ') and
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
    );
    ELSEIF CARTEIRA = 'DISJUNTOR' AND TURMA = 'STC' THEN
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST   AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLP123432.PLANILHAO_CLIENTE PC ON PC.ZCGACCOUN = SC.ZCGACCOUN    
             JOIN CLB142840.DAG40 AS DAG1 ON PC.ZCGCDMUNI||PC.ZCGCODLOC||PC.ZCGCDBAIR = DAG1.ZCGCDMUNI||DAG1.ZCGCODLOC||DAG1.ZCGCDBAIR    
       --AND DAG1.FLAG_GAV = 'S' -- não existe mapa Disjuntor STC    
       WHERE
           ACAO = 'DISJ' AND
           DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
           FLAG_SEL = FALSE AND -- ainda não selecionados
           CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
           AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
    );
        
    ELSEIF CARTEIRA = 'RECORTE' THEN
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = ADD_DAYS(CURRENT_DATE,-3)
        LEFT JOIN CLB961920.ATENA_HIST AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE
        WHERE
            ACAO = 'RECORTE' AND
            DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
            FLAG_SEL = FALSE AND -- ainda não selecionados
            CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
            AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
    );
    
    ELSEIF CARTEIRA = 'BAIXA MIX' THEN 
    
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  SC.*
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE

        WHERE
            ACAO = 'BAIXA' AND
            DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
            SC.PECLD_CONS >0 AND
            SC.ZCGMTVCOB>0 AND
            FLAG_SEL = FALSE AND -- ainda não selecionados
            CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
            AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
    );
    
    
    ELSEIF CARTEIRA = 'MISTA' AND TURMA = 'STC' THEN
    
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  CASE WHEN ACAO IN ('CORTE','DISJ') THEN 'CONVENCIONAL'
                            ELSE ACAO END AS SERVICO,
        SC.*
        
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE

        WHERE
            (ACAO IN ('RECORTE') OR
                 (ACAO IN ('CORTE','DISJ') AND SC.PECLD_CONS >20 AND SC.ZCGMTVCOB > 30)
             ) AND
            DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
            FLAG_SEL = FALSE AND -- ainda não selecionados
            CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
            AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
    );
    
    ELSEIF CARTEIRA = 'MISTA' AND TURMA = 'EPS' THEN
    
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  CASE WHEN ACAO IN ('CORTE','DISJ') THEN 'CONVENCIONAL'
                            ELSE ACAO END AS SERVICO,
        SC.*
        
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE

        WHERE
            (ACAO IN ('RECORTE') OR 
                 (ACAO IN ('CORTE','DISJ') AND SC.PECLD_CONS > 20 AND SC.ZCGMTVCOB > 80)
             ) AND
            SC.PECLD_CONS >0 AND
            SC.ZCGMTVCOB > 0  AND 
            DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
            FLAG_SEL = FALSE AND -- ainda não selecionados
            CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
            AH.ZCGACCOUN IS NULL  -- não selecionado no Atena (ainda não gravado)
            );-- não selecionado no Atena (ainda não gravado)
            

        
    ELSEIF CARTEIRA = 'RECORTE_BAIXA' AND TURMA = 'EPS' THEN
    
    CREATE LOCAL TEMPORARY TABLE CLB961920."#TAB" AS (
        SELECT  CASE WHEN ACAO IN ('CORTE','DISJ') THEN 'CONVENCIONAL'
                            WHEN ACAO IN ('BAIXA') THEN 'BAIXA MIX'
                            ELSE ACAO END AS SERVICO,
        SC.*
        
        FROM CLB961920.SUSCETIVEIS AS SC
        LEFT JOIN CLB142840.CLUSTER_HIST AS CH ON CH.ZCGACCOUN = SC.ZCGACCOUN AND CH.DATA_PEDIDO = CURRENT_DATE
        LEFT JOIN CLB961920.ATENA_HIST AS AH ON AH.ZCGACCOUN = SC.ZCGACCOUN AND AH.DATA_PEDIDO = CURRENT_DATE

        WHERE
            ACAO IN ('RECORTE','BAIXA') AND
             --ACAO IN ('BAIXA') 
             --) AND
            DATAREF = CURRENT_DATE AND -- suscetíveis de hoje
            FLAG_SEL = FALSE AND -- ainda não selecionados
            CH.ZCGACCOUN IS NULL AND -- não selecionado (para prevenir update Flag_sel desatualizado)
            AH.ZCGACCOUN IS NULL AND -- não selecionado no Atena (ainda não gravado)
            SC.PECLD_CONS > 0 AND SC.ZCGMTVCOB > 0
            );-- não selecionado no Atena (ainda não gravado)                    
      
                      
    END IF;
    
    
   --- Verificação de FERIADOS ---
        DELETE FROM CLB961920."#TAB"
        WHERE ACAO IN ('CORTE','DISJ') AND ZCGMUNICI IN 
        (SELECT DISTINCT B.MUNICIPIO FROM CLB142840.DAG40 A 
         JOIN CLB142840.DAG_CRIT C ON A.UTD40 = C.UTD
         JOIN CLB142840.ZCT_FERIADOS B ON A.ZCGCDMUNI = B.ZCGCDMUNI
         WHERE  ((C.CORTE_DIA = 'SIM' AND TURMA <> 'STC') AND
             ((WEEKDAY(DATA_PEDIDO_A) <= 3 AND B.Z_DTA_FER BETWEEN ADD_DAYS(DATA_PEDIDO_A,1) AND ADD_DAYS(DATA_PEDIDO_A,2)) 
                OR (WEEKDAY(DATA_PEDIDO_A) = 4 AND B.Z_DTA_FER BETWEEN ADD_DAYS(DATA_PEDIDO_A,3) AND ADD_DAYS(DATA_PEDIDO_A,4))))
         OR 
            ((C.CORTE_DIA = 'NÃO' OR TURMA='STC') AND 
             ((WEEKDAY(DATA_PEDIDO_A) <= 2 AND B.Z_DTA_FER BETWEEN ADD_DAYS(DATA_PEDIDO_A,2) AND ADD_DAYS(DATA_PEDIDO_A,3))
                OR (WEEKDAY(DATA_PEDIDO_A) IN (3,4) AND B.Z_DTA_FER BETWEEN ADD_DAYS(DATA_PEDIDO_A,4) AND ADD_DAYS(DATA_PEDIDO_A,5))))
        );    

    
   --- ZONAS PERICULOSAS / INACESSIVEIS ---
       
       /*CALL CLB961920.BLOQUEIO_SUSCETIVEIS();
        DELETE FROM CLB961920."#TAB"
        WHERE ZCGACCOUN IN (SELECT DISTINCT ZCGACCOUN FROM CLB961920.SUSCETIVEIS_BLOCK WHERE FLAG_BLOCK=TRUE);*/
   
         
     
-- RETIRA DOS SUSCETIVEIS CLIENTES DCC QUE TENHAM APENAS 1 FATURA PENDENTE
        IF  TURMA = 'EPS' OR TURMA = 'STC' THEN
        DELETE FROM CLB961920."#TAB"
        WHERE ZCGACCOUN IN (SELECT ZCGACCOUN FROM CLB_CCS_ICC.ZCT_DS_FCC001 
WHERE ZCGQTFTVE < 2
AND ZCGMODPAG = 'D') 
         ;      
    END IF;





-- EXCLUSAO DE RUAS PERICULOSAS (RUAS CADASTRADAS NA BASE CLB344173.RUAS_BLOQUEADAS)
IF  (TURMA = 'EPS' OR TURMA = 'STC') and 1 = 1 THEN
DELETE FROM CLB961920."#TAB"
WHERE ZCGACCOUN  IN (SELECT DISTINCT ZCGACCOUN FROM 
        (
            SELECT 
SUSCETIVEIS.ZCGACCOUN
FROM CLB961920.SUSCETIVEIS
LEFT JOIN (SELECT ZCGNMLOGR AS RUA, ZCGACCOUN
FROM CLB_CCS_ICC.ZCT_DS_CLI001 CLI001 
) AS CLI001
ON CLI001.ZCGACCOUN =  SUSCETIVEIS.ZCGACCOUN
WHERE DATAREF = ADD_DAYS(CURRENT_DATE,0)
AND (UTD IN (SELECT UTD FROM CLB344173.RUAS_BLOQUEADAS WHERE DATA_REMOCAO < CURRENT_DATE)
AND ZCGBAIRRO IN (SELECT BAIRRO FROM CLB344173.RUAS_BLOQUEADAS WHERE DATA_REMOCAO < CURRENT_DATE)
AND RUA IN (SELECT RUA FROM CLB344173.RUAS_BLOQUEADAS WHERE DATA_REMOCAO < CURRENT_DATE))
        )
         );      
    END IF;
-- EXCLUSAO DE RUAS PERICULOSAS (RUAS CADASTRADAS NA BASE CLB344173.RUAS_BLOQUEADAS)

-- EXCLUSAO DE zonas rurais, utilizar apenas em caso de exceção
IF  (TURMA = 'EPS' OR TURMA = 'STC') AND 1 = 0  THEN
DELETE FROM CLB961920."#TAB"
WHERE ZCGACCOUN  IN (SELECT DISTINCT ZCGACCOUN FROM 
        (
            SELECT 
SUSCETIVEIS.ZCGACCOUN
FROM CLB961920.SUSCETIVEIS
LEFT JOIN (SELECT ZCGNMLOGR AS RUA, ZCGACCOUN
FROM CLB_CCS_ICC.ZCT_DS_CLI001 CLI001 
) AS CLI001
ON CLI001.ZCGACCOUN =  SUSCETIVEIS.ZCGACCOUN
WHERE DATAREF = ADD_DAYS(CURRENT_DATE,0)
AND (
ZCGBAIRRO like ('%RURAL%')
or RUA LIKE ('%RURAL%'))
        )
         );      
    END IF;


  



        
     DELETE FROM CLB961920."#TAB"
        WHERE SCORE < 4; --IMPLANTADO DIA 15/07/2022                   
        
    ------------------------------------------------------------------------------
    -- Temporário para cruzar com sqls externas (municipios em emergência) --
    IF CLB961920.TABLE_EXISTS('TEMP_ATENA','CLB961920') = 1 THEN
           DROP TABLE CLB961920.TEMP_ATENA;
    END IF;
    CREATE COLUMN TABLE CLB961920.TEMP_ATENA AS (SELECT * FROM CLB961920."#TAB");
    ------------------------------------------------------------------------------    
   
    SELECT Min(LOG(10, PECLD_CONS)) INTO minPECLD FROM CLB961920."#TAB";
    SELECT Max(LOG(10, PECLD_CONS)) INTO maxPECLD FROM CLB961920."#TAB";
    
    SELECT Min(SCORE) INTO minSCORE FROM CLB961920."#TAB";
    SELECT Max(SCORE) INTO maxSCORE FROM CLB961920."#TAB";

    SELECT Min(LOG(10, ZCGMTVCOB)) INTO minMTVCOB FROM CLB961920."#TAB";
    SELECT Max(LOG(10, ZCGMTVCOB)) INTO maxMTVCOB FROM CLB961920."#TAB";    

    SELECT tb.*,
        40 * (LOG(10,tb.PECLD_CONS)-minPECLD)/(maxPECLD-minPECLD)  +
        50 * (tb.SCORE-minSCORE)     /(maxSCORE-minSCORE)  +
        10 * (LOG(10,tb.ZCGMTVCOB)-minMTVCOB)/(maxMTVCOB-minMTVCOB)
        /*
        +
        -- OPERAÇÃO VERÃO
        CASE WHEN ZCGDSCNAE IN ('Hotéis','Outros alojam não especific anterior (usados como hotéis)','Apart-hotéis','Restaurantes e similares','Bares e outros estabelecimentos especializ servir bebidas','Pensões (alojamento)','Fabricação de gelo comum','Comércio atacadista de sorvetes','Fabricação de sorvetes e outros gelados comestíveis') THEN 14 ELSE 0 END
        */ AS IRR
        FROM CLB961920."#TAB" AS tb
        LEFT JOIN CLP123432.PLANILHAO_CLIENTE PC ON PC.ZCGACCOUN = tb.ZCGACCOUN;

   
END;