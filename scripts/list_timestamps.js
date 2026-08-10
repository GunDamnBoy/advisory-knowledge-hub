// 列表頁預篩——一次取回全部「連結＋時間戳」，取代逐篇 fetch。
// 唯一權威版本（2026/08/09 第 15 次修訂新增）。
// 動機：8/09 那輪 A 組為了預篩時間戳對 Bloomberg 連發約 35 次 fetch，觸發網路層風控，
// 此後所有文章頁一律回傳「Are you a robot?」，當日 Bloomberg 成卡 0 篇——
// 而開場的可用性測試原本是通過的（23 段／5,208 字）。**是採集方式把來源惹毛的，不是來源本來就擋。**
// 用法：navigate 到列表頁後執行本片段，拿到清單後「只點窗口內的那幾篇」進去讀正文。
await new Promise(r=>setTimeout(r,3000));
// 文章 ID 可能在查詢字串（MoneyDJ NewsViewer.aspx?a=GUID）——只留路徑會把整站文章去重成一條
const abs=h=>{try{const u=new URL(h,location.href);
  const q=/[?&][^=&]{1,20}=[A-Za-z0-9-]{8,}/.test(u.search)?u.search:'';
  return u.pathname+q}catch(e){return h}};
const seen=new Set(), out=[];
for(const a of document.querySelectorAll('a[href]')){
  const href=a.getAttribute('href')||'';
  // 只要看起來像單篇文章的連結（有日期路徑、長 slug 或數字 ID）
  if(!/\/(19|20)\d{2}[\/-]|\/news\/|\/articles?\/|\/story\/|\.html($|\?)/i.test(href)) continue;   // i：MoneyDJ 是 /News/
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
  out.push({path:p.slice(0,160), title:(a.innerText||'').trim().slice(0,90), ts:t, rel});
}
// 第四層備援：DOM 完全沒有時間戳時，掃 Next.js 的 __NEXT_DATA__。
// Bloomberg 就是這種——2026/08/09 實測列表頁 33 條連結全部沒有 <time> 也沒有相對時間，
// 但 __NEXT_DATA__ 裡有 62 篇的「slug＋標題＋發布時間」，一次請求就取代 35 次逐篇 fetch。
// 附帶好處：部分 Bloomberg 文章頁的 article:published_time 是空的，這裡反而拿得到。
const nextItems=[];
if(out.filter(x=>x.ts||x.rel).length===0 && window.__NEXT_DATA__){
  const seen2=new Set();
  const TIME=/^(published(At)?|datePublished|firstPublished(At)?)$/i;
  (function walk(o,d){
    if(!o||typeof o!=='object'||d>12) return;
    if(Array.isArray(o)){for(const x of o) walk(x,d+1); return;}
    let t=null,slug=null,title=null;
    for(const k of Object.keys(o)){
      const v=o[k];
      if(typeof v!=='string') continue;
      if(TIME.test(k)&&/^20\d{2}-\d{2}-\d{2}T/.test(v)) t=v;
      if(/^(slug|id|url|canonical|longURL)$/i.test(k)&&/\/news\/articles\/|^20\d{2}-\d{2}-\d{2}\//.test(v)) slug=v;
      if(/^(headline|title|seoHeadline)$/i.test(k)&&v.length>15&&!title) title=v;
    }
    if(t&&(slug||title)){
      const key=(slug||title).slice(0,60);
      if(!seen2.has(key)){seen2.add(key);nextItems.push({path:slug||'',title:(title||'').slice(0,90),ts:t,rel:''});}
    }
    for(const k of Object.keys(o)) walk(o[k],d+1);
  })(window.__NEXT_DATA__,0);
  nextItems.sort((a,b)=>b.ts.localeCompare(a.ts));
}
const items=(out.filter(x=>x.ts||x.rel).length===0 && nextItems.length) ? nextItems : out;
JSON.stringify({
  count:items.length,
  withTs:items.filter(x=>x.ts).length,
  source:(items===nextItems?'__NEXT_DATA__':'DOM'),
  items:items.slice(0,60)
});
