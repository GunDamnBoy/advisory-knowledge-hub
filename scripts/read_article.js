// 標準文章讀法——唯一權威版本（2026/08/08 外部化）。主 agent 每天讀本檔一次，
// 逐字放進每個 subagent 的提示。輪詢至段落數穩定（Barron's 等站固定秒數不夠）。
const SEL='article p, main p, [class*="ArticleBody"] p, [class*="body-content"] p,'
  +' p[class*="Paragraph"], div[class*="paragraph"], .available-content p, [class*="markup"] p';
const count=()=>[...document.querySelectorAll(SEL)].filter(p=>p.innerText.trim().length>60).length;
let prev=-1, stable=0;
for(let i=0;i<12;i++){
  await new Promise(r=>setTimeout(r,1000));
  const n=count();
  if(n===prev && n>0){ if(++stable>=2) break; } else { stable=0; prev=n; }
}
const t=document.querySelector('meta[property="article:published_time"]')?.content
  || document.querySelector('meta[name="article.published"]')?.content   // Barron's 備援
  || document.querySelector('time[datetime]')?.getAttribute('datetime') || '';
let paras=[...document.querySelectorAll(SEL)].map(p=>p.innerText.trim()).filter(x=>x.length>60);
if(paras.length<8){   // 選擇器沒對上時的保險絲（Mint 需要）——但全頁 p 抓到的更少就不換（避免把短訊換成導覽雜訊）
  const alt=[...document.querySelectorAll('p')].map(p=>p.innerText.trim()).filter(x=>x.length>60);
  if(alt.join(' ').length>paras.join(' ').length) paras=alt;
}
JSON.stringify({published:t, title:document.title, n:paras.length, chars:paras.join(' ').length, text:paras.join('\n')});
