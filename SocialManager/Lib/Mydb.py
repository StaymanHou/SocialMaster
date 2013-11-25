from settings import *

def MydbExec(exetuple):
    import MySQLdb
    con = MySQLdb.connect(Mydb_host,Mydb_username,Mydb_password,Mydb_db, charset="utf8")
    con.autocommit(True)
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute(*exetuple)
    except Exception, e:
        print str(exetuple)
        raise Exception('DBquery execute error', e)
    con.close()
    return cur

def MydbCon():
    import MySQLdb
    con = MySQLdb.connect(Mydb_host,Mydb_username,Mydb_password,Mydb_db, charset="utf8")
    con.autocommit(True)
    return con

def MydbGetConf():
    cur = MydbExec(("SELECT `MAX_MONITOR_THREAD`, `MON_LOAD_ITERATION`, `MON_CHECK_ITERATION`, `MON_TIMEOUT_LIMIT`, `MON_INIT_RETRY_WAITING_TIME`, `MON_INIT_RETRY_COMMON_RATIO` FROM `MAINCONF` WHERE `PK`=1",))
    if cur.rowcount == 0:
        raise Exception('GetConf error', 'No Configure')
    return cur.fetchone()

def MydbGetAccListForMnt():
    cur = MydbExec(("SELECT `FI_ID`, `USERNAME`, DES_DECRYPT(`PSWD`,%s) AS PSWD FROM `Accounts` WHERE `ACTIVE`=1",(Mydb_key)))
    return cur.fetchall()

def MydbGetAccListForCtl():
    cur = MydbExec(("SELECT `FI_ID`, `USERNAME`, `MONITOR_FINISHED_HOUR`, `CONTROLLER_FINISHED_HOUR` FROM `Accounts` WHERE `ACTIVE`=1",))
    return cur.fetchall()

def MydbGetAccConfForGnrt(fi_id):
    cur = MydbExec(("SELECT `USERNAME`, `MAX_CAMPAIGN_NUM`, `INTST_NUM_LOW`, `INTST_NUM_HIGH`, `INTST_PRIVATE_WEIGHT`, `USER_NUM_LOW`, `USER_NUM_HIGH`, `USER_PRIVATE_WEIGHT`, `CNTRY_NUM_LOW`, `CNTRY_NUM_HIGH`, `CNTRY_PRIVATE_WEIGHT`, `BID_LOW`, `BID_HIGH`, `CMP_BUDGET`, `DLY_BUDGET`, `PTS`, `GENDER`, `ACCELERATED_DELIVERY` FROM `Accounts` WHERE `ACTIVE`=1 AND `FI_ID`=%s LIMIT 1",(fi_id)))
    if cur.rowcount == 0:
        raise Exception('MydbGetAccConfForGnrt error', 'No such user')
    return cur.fetchone()

def MydbGetAccConfForAnlz(fi_id):
    cur = MydbExec(("SELECT `POOR_ZSCORE_THRESHOLD`, `EFFECTIVE_DAYS`, `UPDATE_TIME` FROM `Accounts` WHERE `FI_ID`=%s",(fi_id)))
    if cur.rowcount == 0:
        raise Exception('MydbGetAccZscoreThreshold error', 'No such user')
    return cur.fetchone()

def MydbGetAlvAndCrtpdNum(fi_id):
    cur = MydbExec(("SELECT COUNT(*) AS COUNT FROM `Campaigns` WHERE (`LOCAL_STATUS` = 2 OR `LOCAL_STATUS` = 3) AND `FI_ID`=%s",(fi_id)))
    if cur.rowcount == 0:
        raise Exception('MydbGetAlvAndCrtpdNum error', 'No such user')
    return cur.fetchone()['COUNT']

def MydbGetAliveCmpList(fi_id):
    cur = MydbExec(("SELECT ID, START_TIME, DATA, MAX_BID FROM Campaigns WHERE LOCAL_STATUS = 2 AND `FI_ID`=%s",(fi_id)))
    alive_cmp_lst = []
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_id = row['ID']
        temp_start_time = row['START_TIME']
        temp_bid = row['MAX_BID']
        temp_data = row['DATA']
        alive_cmp_lst.append({'id':temp_id,'start_time':temp_start_time,'bid':temp_bid,'data':temp_data})
    return alive_cmp_lst

def MydbGetAccMonitorFinishedHour(fi_id):
    cur = MydbExec(("SELECT `MONITOR_FINISHED_HOUR` FROM `Accounts` WHERE `FI_ID`=%s",(fi_id)))
    if cur.rowcount == 0:
        raise Exception('GetAccMonitorFinishedHour error', 'No such user')
    return cur.fetchone()['MONITOR_FINISHED_HOUR']

def MydbGetAccExceedThreshold(fi_id):
    cur = MydbExec(("SELECT ACC_BUDGET_REMAIN, `BUDGET_LIMIT_THRESHOLD` FROM `Accounts` WHERE `FI_ID`=%s",(fi_id)))
    if cur.rowcount == 0:
        raise Exception('GetAccBudgetLimitThreshold error', 'No such user')
    budget_data = cur.fetchone()
    if budget_data['ACC_BUDGET_REMAIN']<budget_data['BUDGET_LIMIT_THRESHOLD']: return True
    else: return False

def MydbAccPause(fi_id):
    cur = MydbExec(("UPDATE `Accounts` SET `MAX_CAMPAIGN_NUM`=0 WHERE `FI_ID`=%s",(fi_id)))
    cur = MydbExec(("UPDATE `Campaigns` SET `LOCAL_STATUS`=5 WHERE `FI_ID`=%s AND `LOCAL_STATUS`=3",(fi_id)))
    cur = MydbExec(("UPDATE `Campaigns` SET `LOCAL_STATUS`=4 WHERE `FI_ID`=%s AND `LOCAL_STATUS`=2",(fi_id)))
    return

def MydbSetAccMonitorFinishedHour(fi_id, datetime):
    cur = MydbExec(("UPDATE `Accounts` SET `MONITOR_FINISHED_HOUR`=%s WHERE `FI_ID`=%s",(datetime,fi_id)))
    return

def MydbSetAccControllerFinishedHour(fi_id, datetime):
    cur = MydbExec(("UPDATE `Accounts` SET `CONTROLLER_FINISHED_HOUR`=%s WHERE `FI_ID`=%s",(datetime,fi_id)))
    return

def MydbUpdateRemainAndCheck(fi_id, new_spend):
    cur = MydbExec(("UPDATE `Accounts` SET ACC_BUDGET_REMAIN = (ACC_BUDGET_REMAIN-%s) WHERE FI_ID = %s",(new_spend,fi_id)))
    if MydbGetAccExceedThreshold(fi_id):
        MydbAccPause(fi_id)
    return
    



