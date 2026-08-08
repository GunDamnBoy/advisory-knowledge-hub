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
TODAY=sys.argv[1] if len(sys.argv)>1 else NOW.strftime('%Y-%m-%d')
SRCOK={'bbg','wsj','nyt','ft','nikkei','wapo','barrons','cnbc','ibd','mw','toms',
       'ogj','politico','thehill','wscn','reuters','anue','moneydj','twse','semi',
       'fierce','stat','ked','kh','mint','tf','econ','pub'}   # reuters/ked 已停用，保留供舊檔重跑
QUOTA={'美股與財報':10,'AI 與半導體':10,'央行、利率與匯率':8,'台灣':10,
       '中國':6,'日本':6,'能源與原物料':6,'金融、併購與企業':6,
       '地緣政治（中東與戰事）':6,'美國政治與政策':6,
       '歐洲':3,'亞太（韓國、印度、東南亞）':3,'生技健護':3,'信用債':3,'黃金':3}
# 每日更新但網址固定的官方數據頁，豁免去重（內容每天都變，只有 URL 相同）
DEDUP_EXEMPT=('trendforce.com','fred.stlouisfed.org','spdrgoldshares.com',
              'cmegroup.com','gold.org','twse.com.tw','tpex.org.tw','mopsfin.twse.com.tw')
exempt=lambda u:any(h in u for h in DEDUP_EXEMPT)
d=json.load(open('%s/data/%s.json'%(REPO,TODAY)))
w=d.get('window')
assert w,'★致命：頂層缺 window 欄'
frm=dt.datetime.fromisoformat(w['from']); to=dt.datetime.fromisoformat(w['to'])
cards=[(g['label'],c) for s in d['sections'] for g in s['groups'] for c in g['cards']]
def T(c):
    try: return dt.datetime.fromisoformat(c['ts'])
    except Exception: return None   # 缺 ts 不中斷——檢查機制自己安靜失效比沒有檢查更危險
def islist(u):
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
prevmeta=next((x for x in days if x['date']!=TODAY),None)   # 不可直接用 days[1]
prev=json.load(open('%s/%s'%(REPO,prevmeta['file']))) if prevmeta else {'sections':[]}
prevurl={c['url'] for s in prev['sections'] for g in s['groups'] for c in g['cards']}
dup=[c['title'] for _,c in cards if c['url'] in prevurl and not exempt(c['url'])]
u=collections.defaultdict(list)
for lab,c in cards: u[c['url']].append(lab)
multi={k:v for k,v in u.items() if len(v)>1 and not exempt(k)}
viol=[(v,k) for k,v in multi.items() if not(len(v)<=3 and len(set(v))==len(v))]
n=len(cards); fails=[]
print('總數',n,'OK' if 95<=n<=125 else '★不在 95–125')
if not 95<=n<=125: fails.append('總數')
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
        lab=g['label']; seen.add(lab); q=QUOTA.get(lab)
        if q is None: print('★分組名不在 QUOTA 表：',lab); fails.append('分組名'); continue
        okq=len(g['cards'])>=q
        print('%-22s %2d / 需 %d %s'%(lab,len(g['cards']),q,'OK' if okq else '★不足'))
        if not okq: fails.append(lab)
missing=set(QUOTA)-seen
print('★缺少的分組：',missing or '無')
if missing: fails.append('缺組')
print('\n'+('✅ 全部通過' if not fails else '❌ 硬性失敗：'+', '.join(fails)))
sys.exit(0 if not fails else 1)
