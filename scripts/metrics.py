#!/usr/bin/env python3
"""歷史指標——掃 data/*.json 算出跨版趨勢，供優化時比較與回溯。
用法：python3 scripts/metrics.py [--src] [--groups] [--csv]
  （無參數＝總表；--src 加來源貢獻矩陣；--groups 加各組達標歷史；--csv 輸出 CSV）
資料全部即時重算，不需要維護快照檔。歷次規格變更見 CHANGELOG.md。
"""
import json,glob,collections,sys,os,datetime as dt
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
try:
    from check import QUOTA,WEEKEND_QUOTA   # 下限表以 check.py 為唯一權威，不要在這裡再抄一份
except Exception:
    QUOTA={};WEEKEND_QUOTA={}

def is_weekend(d):
    """與 check.py 同一判定：窗口起點那天是週六日＝週末輪"""
    w=d.get('window') or {}
    try: return dt.datetime.fromisoformat(w['from']).weekday()>=5
    except Exception: return False
# 規格里程碑：讓趨勢表能對照「哪天起換了規則」
MILESTONES={'2026-08-04':'v4 窗口制上線','2026-08-05':'v9 十五組上線',
            '2026-08-06':'v11 台股API/輪詢','2026-08-08':'v13 移除Reuters・v14 精簡',
            '2026-08-09':'v15 列表頁預篩','2026-08-10':'v16 週末模式',
            '2026-08-11':'v17 時序化・thread・搜尋'}

def load():
    out=[]
    for f in sorted(glob.glob(REPO+'/data/2026-*.json')):
        d=json.load(open(f))
        cards=[(g['label'],c) for s in d['sections'] for g in s['groups'] for c in g['cards']]
        out.append((d,cards))
    return out

def main():
    rows=load(); args=set(sys.argv[1:])
    if '--csv' in args:
        print('date,cards,groups,deep,sources,ts_cov,thermo,window_from,window_to')
        for d,cards in rows:
            w=d.get('window') or {}
            lv=str(((d.get('overview') or {}).get('thermo') or {}).get('level',''))
            print('%s,%d,%d,%d,%d,%d,%s,%s,%s'%(d['date'],len(cards),len({l for l,_ in cards}),
                sum(1 for _,c in cards if c.get('deep')),len({c['src'] for _,c in cards}),
                sum(1 for _,c in cards if c.get('ts')),lv if lv.isdigit() else '',
                w.get('from',''),w.get('to','')))
        return
    print('=== 每版總表 ===')
    print(f"{'日期':<11}{'則數':>5}{'組數':>5}{'深度':>5}{'來源':>5}{'ts%':>6}{'溫度':>5}  {'窗口':<24}里程碑")
    for d,cards in rows:
        w=d.get('window') or {}
        n=len(cards); ts=sum(1 for _,c in cards if c.get('ts'))
        win=('%s→%s'%(w['from'][5:16],w['to'][5:16])) if w else '—（窗口制前）'
        lv=str(((d.get('overview') or {}).get('thermo') or {}).get('level',''))
        lv=lv if lv.isdigit() else '—'   # 8/11 前有幾天是散文，時間序列從數值日起算
        print(f"{d['date']:<11}{n:>5}{len({l for l,_ in cards}):>5}"
              f"{sum(1 for _,c in cards if c.get('deep')):>5}{len({c['src'] for _,c in cards}):>5}"
              f"{(ts*100//n if n else 0):>5}%{lv:>5}  {win:<24}{MILESTONES.get(d['date'],'')}")
    if '--groups' in args and QUOTA:
        print('\n=== 各組則數 vs 下限（負值＝不足）===')
        labs=list(QUOTA)
        print(f"{'日期':<11}"+''.join(f'{l[:6]:>7}' for l in labs))
        for d,cards in rows:
            cnt=collections.Counter(l for l,_ in cards)
            q=WEEKEND_QUOTA if is_weekend(d) and WEEKEND_QUOTA else QUOTA
            cells=''.join(f'{(str(cnt[l]-q[l]) if l in cnt else "—"):>7}' for l in labs)
            print(f"{d['date']:<11}{cells}{'  週末' if is_weekend(d) else ''}")
        print('（"—"＝該版沒有這一組；數字＝實際則數減「該日適用下限」的緩衝；週末列已用放寬後的下限）')
    if '--src' in args:
        print('\n=== 來源貢獻矩陣 ===')
        allsrc=sorted({c['src'] for _,cards in rows for _,c in cards})
        print(f"{'日期':<11}"+''.join(f'{s[:7]:>8}' for s in allsrc))
        for d,cards in rows:
            cnt=collections.Counter(c['src'] for _,c in cards)
            print(f"{d['date']:<11}"+''.join(f'{(cnt[s] or "·"):>8}' for s in allsrc))
        print('（"·"＝當日零產出。連續零產出是移除來源的判斷依據，見 CHANGELOG v13 Reuters）')

def tags_block(rows):
    last=rows[-8:]
    tot=collections.Counter(); per=[]
    for d,cards in last:
        c=collections.Counter(c.get('tag','') for _,c in cards)
        per.append((d['date'],c)); tot.update(c)
    tags=[t for t,n_ in tot.most_common() if n_>=3]
    print('\n=== 標籤動能（近 %d 天，總數 ≥3 的標籤）==='%len(last))
    print(f"{'標籤':<12}"+''.join(f'{dd[5:]:>7}' for dd,_ in per)+f"{'合計':>7}")
    for t in tags:
        print(f"{t[:10]:<12}"+''.join(f'{(c[t] or "·"):>7}' for _,c in per)+f"{tot[t]:>7}")
    print('（看哪些題材在升溫／退燒；標籤是自由填寫，同義詞請人工合併判讀）')
    thr=collections.Counter()
    for d,cards in rows:
        for _,c in cards:
            if c.get('thread'): thr[c['thread']]+=1
    if thr:
        print('\n=== 主題連續劇（thread 出現總則數）===')
        for t,n_ in thr.most_common(20): print(f'  {t:<18}{n_}')

if __name__=='__main__':
    main()
    if '--tags' in set(sys.argv[1:]): tags_block(load())
