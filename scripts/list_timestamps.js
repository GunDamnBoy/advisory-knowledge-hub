// 列表頁預篩——一次取回全部「連結＋時間戳」，取代逐篇 fetch。
// 唯一權威版本（2026/08/09 第 15 次修訂新增）。
// 動機：8/09 那輪 A 組為了預篩時間戳對 Bloomberg 連發約 35 次 fetch，觸發網路層風控，
// 此後所有文章頁一律回傳「Are you a robot?」，當日 Bloomberg 成卡 0 篇——
// 而開場的可用性測試原本是通過的（23 段／5,208 字）。**是採集方式把來源惹毛的，不是來源本來就擋。**
// 用法：navigate 到列表頁後執行本片段，拿到清單後「只點窗口內的那幾篇」進去讀正文。
await new Promise(r=>setTimeout(r,3000));
const abs=h=>{try{return new URL(h,location.href).pathname}catch(e){return h}};
const seen=new Set(), out=[];
for(const a of document.querySelectorAll('a[href]')){
  const href=a.getAttribute('href')||'';
  // 只要看起來像單篇文章的連結（有日期路徑、長 slug 或數字 ID）
  if(!/\/(19|20)\d{2}[\/-]|\/news\/|\/articles?\/|\/story\/|\.html$/.test(href)) continue;
  const p=abs(href); if(seen.has(p)) continue; seen.add(p);
  // 時間戳：先找連結自身或祖先容器內的 <time>，再退回 data 屬性
  let node=a, t='';
  for(let i=0;i<4 && node && !t;i++){
    const el=node.querySelector?.('time[datetime]')||node.parentElement?.querySelector?.('time[datetime]');
    t=el?.getAttribute('datetime')||node.getAttribute?.('data-timestamp')||'';
    node=node.parentElement;
  }
  // 沒有機器可讀時間戳時，抓容器內的相對時間文字（"3 hours ago" / "2小時前"）
  let rel='';
  if(!t){
    const txt=(a.closest('article,li,div')?.innerText||'').slice(0,200);
    const m=txt.match(/(\d+)\s*(minutes?|mins?|hours?|hrs?|days?|分鐘|小時|天)\s*(ago|前)/i);
    if(m) rel=m[0];
  }
  out.push({path:p.slice(0,120), title:(a.innerText||'').trim().slice(0,90), ts:t, rel});
}
JSON.stringify({count:out.length, withTs:out.filter(x=>x.ts).length, items:out.slice(0,60)});
