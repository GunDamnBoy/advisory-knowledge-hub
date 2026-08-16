#!/usr/bin/env python3
# 發布前自我檢查——唯一權威版本（2026/08/08 第 14 次修訂外部化）。
# 用法：python3 /Users/kenny/advisory-knowledge-hub/scripts/check.py [YYYY-MM-DD]（省略＝台北今天）
# 出口碼 0＝全部通過；1＝有硬性失敗。改分組或下限只改本檔的 QUOTA，並同步 AGENT_BRIEF 第 4.1 節散文版。
import json,datetime as dt,collections,re,sys,os
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    from zoneinfo import ZoneInfo; NOW=dt.datetime.now(ZoneInfo('Asia/Taipei'))
except Exception:
    NOW=dt.datetime.utcnow()+dt.timedelta(hours=8)
SRCOK={'bbg','wsj','nyt','ft','nikkei','wapo','barrons','cnbc','ibd','mw','toms',
       'ogj','politico','thehill','wscn','reuters','anue','moneydj','twse','semi',
       'fierce','stat','ked','kh','mint','tf','econ','pub'}   # reuters/ked 已停用，保留供舊檔重跑
QUOTA={'美股與財報':10,'AI 與半導體':10,'央行、利率與匯率':8,'台灣':10,
       '中國':6,'日本':6,'能源與原物料':6,'金融、併購與企業':6,
       '地緣政治（中東與戰事）':6,'美國政治與政策':6,
       '歐洲':3,'亞太（韓國、印度、東南亞）':3,'生技健護':3,'信用債':3,'黃金':3}
# 週末模式（2026/08/10 第 16 次修訂）：窗口涵蓋週六或週日時自動放寬。
# 動機：8/10 那輪窗口涵蓋週日，Fierce/FDA/OGJ/IBD/TrendForce 全部零新文，
# 為了湊平日下限開了四輪補位、佔全輪 22.6% 成本，換來的還是偏軟的素材。
# 週末素材少是事實，不是執行不力——下限跟著現實走，不要讓規則逼出注水內容。
WEEKEND_QUOTA={**QUOTA,
  '中國':4,'日本':4,'能源與原物料':4,'金融、併購與企業':4,
  '地緣政治（中東與戰事）':4,'美國政治與政策':4,
  '歐洲':2,'亞太（韓國、印度、東南亞）':2,'生技健護':2,'信用債':2,'黃金':2}
WEEKEND_RANGE=(80,125)   # 週末全站則數下限跟著放寬
# 卡片字數區間（2026/08/16 第 22 次修訂新增）。只警告不擋——字數是品質指標不是正確性指標，
# 為了湊字數注水比超標更糟。但不量就會安靜漂移：8/15 一般卡 702 字、規格當時寫 450–600。
# 區間 2026/08/16 傍晚由 (650,800) 放寬為 (550,900)：8/16 實測 103 張一般卡為乾淨單峰
# （最短 570、中位 700、最長 1081），40 張逾越純屬自然離散、不是品質問題。
# 但「每天都亮的警告」很快會被當成背景噪音——放寬後涵蓋 102/103 張，逾越才重新有訊號價值。
LEN_REG=(550,900)    # 一般卡：lead ＋ bullets
LEN_DEEP=(900,1300)  # 深度卡：多段 longread（同步放寬上緣，8/15 實測平均 1135）
# 每日更新但網址固定的官方數據頁，豁免去重（內容每天都變，只有 URL 相同）
DEDUP_EXEMPT=('trendforce.com','fred.stlouisfed.org','spdrgoldshares.com',
              'cmegroup.com','gold.org','twse.com.tw','tpex.org.tw','mopsfin.twse.com.tw')
exempt=lambda u:any(h in u for h in DEDUP_EXEMPT)

def main():
    TODAY=sys.argv[1] if len(sys.argv)>1 else NOW.strftime('%Y-%m-%d')
    d=json.load(open('%s/data/%s.json'%(REPO,TODAY)))
    w=d.get('window')
    assert w,'★致命：頂層缺 window 欄'
    frm=dt.datetime.fromisoformat(w['from']); to=dt.datetime.fromisoformat(w['to'])
    fails=[]
    if not(frm.hour==7 and frm.minute==0 and (dt.date.fromisoformat(TODAY)-frm.date()).days==1):
        print('★窗口起點異常：%s（應為前一日 07:00 台北，固定起點見 brief 第 3 節）'%w['from']); fails.append('窗口起點')
    if d.get('date')!=TODAY:
        print('★頂層 date 與檔名不一致：',d.get('date')); fails.append('頂層date')
    # 判定依據是「窗口起點那一天」——窗口是「前一日 07:00 → 當日上午」，主體是前一日。
    # 用 to（當日）判會誤判：8/08 那輪 to 是週六但窗口主體是週五，素材其實很充足（123 則）。
    weekend = frm.weekday()>=5          # 5=週六 6=週日
    quota = WEEKEND_QUOTA if weekend else QUOTA
    lo,hi = WEEKEND_RANGE if weekend else (95,125)
    cards=[(g['label'],c) for s in d['sections'] for g in s['groups'] for c in g['cards']]
    def T(c):
        try:
            x=dt.datetime.fromisoformat(c['ts'])
            return x if x.tzinfo else None   # 沒帶時區＝壞 ts（比較 naive/aware 會 TypeError 崩潰）
        except Exception: return None   # 缺 ts 不中斷——檢查機制自己安靜失效比沒有檢查更危險
    def islist(u):
        if re.search(r'[?&][^=&]{1,20}=[A-Za-z0-9-]{8,}',u): return False   # 文章 ID 在查詢字串（MoneyDJ 等）
        p=re.sub(r'^https?://[^/]+','',u).split('?')[0].strip('/')
        if not p: return True
        last=p.split('/')[-1]
        return '-' not in last and not re.search(r'\d{4,}',last)
    nots=[c['title'] for _,c in cards if T(c) is None]
    bad =[c['title'] for _,c in cards if T(c) and T(c)<frm]
    fut =[c['title'] for _,c in cards if T(c) and T(c)>to]
    mism=[c['title'] for _,c in cards if T(c) and T(c).strftime('%Y/%m/%d')!=c['date']]
    badsrc=[(c.get('src'),c['title'][:30]) for _,c in cards if c.get('src') not in SRCOK]
    listy=sorted({c['url'] for _,c in cards if islist(c['url']) and not exempt(c['url'])})
    days=json.load(open('%s/data/index.json'%REPO))['days']
    prevmeta=max((x for x in days if x['date']<TODAY),key=lambda x:x['date'],default=None)   # 取「小於該日的最大日期」——歷史重跑時不能拿最新版來比
    prev=json.load(open('%s/%s'%(REPO,prevmeta['file']))) if prevmeta else {'sections':[]}
    prevurl={c['url'] for s in prev['sections'] for g in s['groups'] for c in g['cards']}
    dup=[c['title'] for _,c in cards if c['url'] in prevurl and not exempt(c['url'])]
    if TODAY>='2026-08-11':   # v17/v18（時間序列化＋回顧／立場）起生效，歷史檔不回溯套用
        ov=d.get('overview') or {}
        th=ov.get('thermo') or {}
        lv=str(th.get('level',''))
        if not(lv.isdigit() and 0<=int(lv)<=100):
            print('★thermo.level 須為 0–100 整數字串（散文放 note）：',repr(lv)); fails.append('thermo')
        for sn in ov.get('snap',[]):
            if not isinstance(sn.get('num'),(int,float)):
                print('★snap 項缺 num 數值欄：',sn.get('k')); fails.append('snap.num'); break
        # v18：五資產立場列（固定五鍵、固定方向詞）
        PKEYS=['美股','美債','美元','黃金','原油']; DIRS={'偏多','中性','偏空'}
        pu=ov.get('pulse')
        if not(isinstance(pu,list) and [x.get('k') for x in pu]==PKEYS and all(x.get('dir') in DIRS for x in pu)):
            print('★pulse 須為固定五鍵（美股/美債/美元/黃金/原油）且 dir∈偏多/中性/偏空'); fails.append('pulse')
        # v18：昨日盯盤節點回顧（前一版 watch 非空 → 必須逐條回顧）
        VOK={'應驗','落空','未決'}
        pw=(next((x for x in days if prevmeta and x['date']==prevmeta['date']),{}) or {}).get('watch') or []
        wr=ov.get('watchReview') or []
        if pw and not wr:
            print('★前一版有 %d 條盯盤節點，watchReview 不可空——驗證回圈是本站的差異化功能'%len(pw)); fails.append('watchReview')
        for x in wr:
            if x.get('verdict') not in VOK:
                print('★watchReview.verdict 須為 應驗/落空/未決：',x.get('verdict')); fails.append('verdict'); break
        # index.json 當日 entry 的跨日記憶欄位
        ent=next((x for x in days if x['date']==TODAY),None)
        need=lambda e:(isinstance(e.get('thermo'),int) and isinstance(e.get('threads'),list)
                       and isinstance(e.get('watch'),list) and isinstance(e.get('pulse'),list)
                       and isinstance(e.get('snap'),list))
        if not ent or not need(ent):
            print('★index.json 當日 entry 缺跨日記憶欄位（thermo/threads/watch/pulse/snap）'); fails.append('index欄位')
    for _,c in cards:
        tv=c.get('thread')
        if tv is not None and not(isinstance(tv,str) and 2<=len(tv)<=16):
            print('★thread 代號格式錯（2–16 字的字串）：',repr(tv)); fails.append('thread'); break
    u=collections.defaultdict(list)
    for lab,c in cards: u[c['url']].append(lab)
    multi={k:v for k,v in u.items() if len(v)>1 and not exempt(k)}
    viol=[(v,k) for k,v in multi.items() if not(len(v)<=3 and len(set(v))==len(v))]
    # ---- 卡片字數（警告層級，不計入 fails）----
    if TODAY>='2026-08-16':
        L=lambda c:(len(' '.join(c['body']) if isinstance(c['body'],list) else c['body'])
                    +sum(len(b) for b in c.get('bullets',[])))
        reg=[L(c) for _,c in cards if not c.get('deep')]
        dp =[L(c) for _,c in cards if c.get('deep')]
        for name,arr,(lo_,hi_) in [('一般卡',reg,LEN_REG),('深度卡',dp,LEN_DEEP)]:
            if not arr: continue
            avg=sum(arr)//len(arr); out=sum(1 for x in arr if not lo_<=x<=hi_)
            mark='OK' if lo_<=avg<=hi_ else ('★偏短' if avg<lo_ else '★偏長')
            print('%s %d 張 平均 %d 字（規格 %d–%d）%s；逾越區間 %d 張'
                  %(name,len(arr),avg,lo_,hi_,mark,out))

    n=len(cards)
    if d.get('cards')!=n:
        print('★頂層 cards 數字與實際卡數不一致：%s vs %d'%(d.get('cards'),n)); fails.append('頂層cards')
    print('模式：'+('週末（下限已放寬）' if weekend else '平日'))
    print('總數',n,'OK' if lo<=n<=hi else '★不在 %d–%d'%(lo,hi))
    if not lo<=n<=hi: fails.append('總數')
    for name,lst in [('缺/壞 ts',nots),('逾期',bad),('未來 ts',fut),('date/ts 不一致',mism),('與前一版重複',dup)]:
        print(name,len(lst),lst[:3])
        if lst: fails.append(name)
    print('src 不在清單',badsrc[:3] or '無'); fails+=['src'] if badsrc else []
    print('疑似列表頁（警告，人工確認）',listy or '無')
    print('比對的前一版：',prevmeta['file'] if prevmeta else '無')
    for k,v in multi.items():
        ok=len(v)<=3 and len(set(v))==len(v)
        print(('拆卡OK ' if ok else '★違規 '),len(v),v,k[:70])
    if viol: fails.append('拆卡違規')
    seen=set()
    for s in d['sections']:
        for g in s['groups']:
            lab=g['label']; seen.add(lab); q=quota.get(lab)
            if q is None: print('★分組名不在 QUOTA 表：',lab); fails.append('分組名'); continue
            okq=len(g['cards'])>=q
            print('%-22s %2d / 需 %d %s'%(lab,len(g['cards']),q,'OK' if okq else '★不足'))
            if not okq: fails.append(lab)
    missing=set(quota)-seen
    print('★缺少的分組：',missing or '無')
    if missing: fails.append('缺組')
    print('\n'+('✅ 全部通過' if not fails else '❌ 硬性失敗：'+', '.join(fails)))
    sys.exit(0 if not fails else 1)

if __name__=='__main__':
    main()
