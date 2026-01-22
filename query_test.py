import oracledb
from datetime import datetime
fromdate = '2026-01-19'
to_date = '2026-01-20'



def get_data():
    date = datetime.now()
    print(f"start ..... {date}")
    conn = oracledb.connect(user="COLVIR", password="ColvirTuron", dsn="192.168.7.152/CBSPROD", port=1521)
    cursor = conn.cursor()
    cursor.execute("call colvir.c_pkgconnect.popen()")
    cursor.execute(f"""WITH base_trn AS (
            SELECT n.*
            FROM colvir.n_crdintrn n
            WHERE n.trn_date >= DATE '{fromdate}'
              AND n.trn_date <  DATE '{to_date}'
              AND lower(n.merch_name) LIKE '%p2p%'
        ),
        big_cards AS (
            SELECT SUBSTR(card_acc,10,8) AS card_acc_8
            FROM base_trn
            GROUP BY SUBSTR(card_acc,10,8)
            HAVING SUM(trn_sum) >= 10000000
        )
        SELECT /*+ 
                INDEX(n IE_N_CRDINT#_CARD_ACC_TRN_DATE)
                INDEX(idn IE_G_CLIIDN_IDN)
                INDEX(hst FK_G_ACCBLNHST_G_CLI)
                INDEX(ch PK_G_CLIHST)
                INDEX(hv AK_A_RESPRS_CLI)
               */
               n.trn_date AS data,
               CASE 
                 WHEN LENGTH(colvir.gl_anl.fAccAnlValue(hst.dep_id, hst.id, 'DEPARTMENT')) > 6
                 THEN colvir.c_pkgdep.fGetCodeDep(
                        colvir.c_pkgdep.fGetIdHiDep(
                          colvir.gl_anl.fAccAnlValue(hst.dep_id, hst.id, 'DEPARTMENT')
                        )
                      )
                 ELSE colvir.gl_anl.fAccAnlValue(hst.dep_id, hst.id, 'DEPARTMENT')
               END AS dep_code,
               hst.codehst AS acc,
               n.card_no,
               n.trn_val,
               n.debfl,
               n.trn_sum,
               n.merch_name,
               n.merch_country,
               n.merch_num,
               n.mcc_code,
               ch.longname,
               idn.idn_num,
               hv.tab_number,
               hv.id as per_id
        FROM big_cards bc
        JOIN base_trn n
          ON SUBSTR(n.card_acc,10,8) = bc.card_acc_8
        JOIN colvir.g_accblnhst hst
          ON hst.codehst = n.card_acc
        JOIN colvir.g_cliidn idn
          ON hst.clidep_id = idn.dep_id
         AND hst.cli_id    = idn.id
        JOIN colvir.g_clihst ch
          ON hst.clidep_id = ch.dep_id
         AND hst.cli_id    = ch.id
        JOIN colvir.a_resprs hv
          ON ch.dep_id = hv.cli_dep_id
         AND ch.id     = hv.cli_id
        JOIN COLVIR.T_PROCMEM M
          ON hv.ord_dep_id = M.DEP_ID 
         AND hv.ord_id     = M.ORD_ID
         AND M.MAINFL      = '1'
        JOIN COLVIR.T_PROCESS P
          ON P.ID = M.ID
        JOIN COLVIR.T_BOP_STAT S
          ON S.ID   = P.BOP_ID
         AND S.NORD = P.NSTAT
        WHERE idn.idn_id = '905'
          AND idn.todate > SYSDATE
          AND hst.todate > SYSDATE
          AND ch.todate  > SYSDATE
          AND s.CODE     != 'H_DISMISSED'
          """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

print(get_data())


