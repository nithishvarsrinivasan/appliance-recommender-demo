let currentRecommendation=null;
const $=s=>document.querySelector(s);
const recBox=$("#recBox"), fbBox=$("#fbBox"), userInput=$("#userId");
const getBtn=$("#getBtn"), randomBtn=$("#randomBtn"), helpfulBtn=$("#helpfulBtn"), notHelpfulBtn=$("#notHelpfulBtn");
const show=el=>el.classList.remove("hidden"); const hide=el=>el.classList.add("hidden");
const pretty=o=>JSON.stringify(o,null,2);

async function fetchUsers(){ const r=await fetch("/users"); if(!r.ok) return []; return r.json(); }
async function getRandomUser(){ const u=await fetchUsers(); if(u.length===0) return null; return u[Math.floor(Math.random()*u.length)]; }

async function doRecommend(){
  const uid=userInput.value.trim();
  if(!uid){ alert("Enter a user id (e.g., U1)"); return; }
  const res=await fetch(`/recommend?user_id=${encodeURIComponent(uid)}`);
  const data=await res.json();
  if(!res.ok){ recBox.textContent=pretty(data); show(recBox); helpfulBtn.disabled=true; notHelpfulBtn.disabled=true; currentRecommendation=null; return; }
  currentRecommendation=data.recommendation; const stats=data.feedback_stats;
  recBox.innerHTML=`
    <div class="kv">
      <div><strong>User</strong></div><div>${currentRecommendation.user_id}</div>
      <div><strong>Appliance</strong></div><div>${currentRecommendation.appliance}</div>
      <div><strong>Recommended Model</strong></div><div>${currentRecommendation.recommended_model}</div>
      <div><strong>Current Power (kWh/use)</strong></div><div>${currentRecommendation.current_power_kwh}</div>
      <div><strong>Usage Count</strong></div><div>${currentRecommendation.usage_count}</div>
      <div><strong>Estimated kWh Saved / use</strong></div><div>${currentRecommendation.estimated_kwh_saved_per_use}</div>
      <div><strong>Feedback Tally</strong></div><div>👍 ${stats.helpful} | 👎 ${stats.not_helpful}</div>
    </div>
    <p style="margin-top:8px;">${currentRecommendation.rationale}</p>`;
  show(recBox); helpfulBtn.disabled=false; notHelpfulBtn.disabled=false;
}

async function sendFeedback(helpful){
  if(!currentRecommendation){ alert("Get a recommendation first"); return; }
  const payload={user_id: currentRecommendation.user_id, appliance: currentRecommendation.appliance, recommended_model: currentRecommendation.recommended_model, helpful: helpful};
  const res=await fetch("/feedback",{method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload)});
  const data=await res.json(); fbBox.textContent=pretty(data); show(fbBox); await doRecommend();
}

getBtn.addEventListener("click", doRecommend);
randomBtn.addEventListener("click", async ()=>{ const uid=await getRandomUser(); if(uid){ userInput.value=uid; doRecommend(); }});
helpfulBtn.addEventListener("click", ()=>sendFeedback(true));
notHelpfulBtn.addEventListener("click", ()=>sendFeedback(false));
userInput.value="U1";
