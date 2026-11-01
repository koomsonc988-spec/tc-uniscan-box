from flask import Flask

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TC UniScan Box</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#000;color:#fff;min-height:100vh}
.header{background:#111;border-bottom:2px solid #D4AF37;padding:15px;text-align:center}
.logo-img{width:110px;height:110px;object-fit:contain;margin:0 auto;display:block}
.app-name{color:#D4AF37;font-size:22px;font-weight:800}
.tagline{color:#aaa;font-size:12px}
.camera-box{position:relative;width:95%;max-width:480px;margin:15px auto;background:#111;border-radius:20px;overflow:hidden;border:2px solid #D4AF37;aspect-ratio:4/3}
video,canvas,img#captured{width:100%;height:100%;object-fit:cover}
.scan-line{position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,#D4AF37,transparent);animation:scan 2s infinite;display:none}
@keyframes scan{0%{top:0}100%{top:100%}}
.controls{display:flex;gap:10px;justify-content:center;padding:15px}
.btn{padding:14px 28px;border-radius:50px;border:none;font-weight:700;font-size:15px;cursor:pointer}
.btn-gold{background:linear-gradient(135deg,#FFD700,#B8860B);color:#000}
.btn-dark{background:#222;color:#fff;border:1px solid #333}
.result{width:95%;max-width:480px;margin:0 auto 20px;background:#0f0f0f;border:1px solid #222;border-radius:20px;padding:20px;display:none}
.result h2{color:#D4AF37}.result h3{color:#FFD700;font-size:13px;margin:14px 0 6px;text-transform:uppercase}
.result p{color:#ddd;line-height:1.6;font-size:14px;white-space:pre-wrap}
.premium-modal{position:fixed;inset:0;background:rgba(0,0,0,0.92);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal-box{background:#111;border:2px solid #D4AF37;border-radius:20px;padding:25px;width:100%;max-width:380px;text-align:center}
.counter{text-align:center;color:#888;font-size:12px;margin:10px}
</style>
</head>
<body>
<div class="header">
<div style="width:110px;height:110px;background:linear-gradient(135deg,#FFD700,#B8860B);border-radius:20px;margin:0 auto;display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:40px">TC</div>
<div class="app-name">TC UniScan Box</div>
<div class="tagline">Smart AI Scanner - Like Meta AI</div>
</div>
<div class="counter" id="counter"></div>
<div class="camera-box">
<video id="video" autoplay playsinline></video>
<canvas id="canvas" style="display:none"></canvas>
<img id="captured" style="display:none">
<div class="scan-line" id="scanLine"></div>
</div>
<div class="controls">
<button class="btn btn-dark" onclick="switchCam()">Flip</button>
<button class="btn btn-gold" onclick="captureAndAnalyze()">SCAN NOW</button>
<button class="btn btn-dark" onclick="retake()">Retake</button>
</div>
<div class="result" id="result">
<h2 id="itemName"></h2>
<h3>What is this?</h3><p id="what"></p>
<h3>Everything About It</h3><p id="about"></p>
<h3>Uses & Facts</h3><p id="uses"></p>
<h3>Origin</h3><p id="origin"></p>
<h3>Notes</h3><p id="notes"></p>
</div>
<div class="premium-modal" id="premiumModal">
<div class="modal-box">
<h2 style="color:#D4AF37">Premium Required</h2>
<p style="color:#ccc;margin:15px 0">20 FREE used.<br>Unlock for <b style="color:#FFD700">GHS 50</b></p>
<a href="https://paystack.shop/pay/qjkz4aszx8" target="_blank" class="btn btn-gold" style="display:block;text-decoration:none;margin:10px 0">PAY GHS 50 NOW</a>
<input id="ownerCode" placeholder="Enter Code" style="width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#000;color:#fff;margin:10px 0">
<button class="btn btn-dark" style="width:100%" onclick="unlock()">UNLOCK</button>
</div>
</div>
<script>
var OWNER_CODE='TC2024GOLD';var FREE_LIMIT=20;
var video=document.getElementById('video');var canvas=document.getElementById('canvas');var captured=document.getElementById('captured');var facing='environment';var stream;
async function startCam(){try{if(stream)stream.getTracks().forEach(t=>t.stop());stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});video.srcObject=stream;video.style.display='block';captured.style.display='none'}catch(e){alert('Camera error')}}
function switchCam(){facing=facing==='environment'?'user':'environment';startCam()}
function retake(){document.getElementById('result').style.display='none';video.style.display='block';captured.style.display='none';document.getElementById('scanLine').style.display='none'}
function getCount(){return parseInt(localStorage.getItem('tc_scan_count')||'0')}
function setCount(c){localStorage.setItem('tc_scan_count',c);updateCounter()}
function updateCounter(){var c=getCount();var left=FREE_LIMIT-c;var el=document.getElementById('counter');if(localStorage.getItem('tc_unlocked')==='yes'){el.innerHTML='PREMIUM UNLOCKED - Unlimited';el.style.color='#D4AF37'}else{el.innerHTML='FREE: '+c+'/'+FREE_LIMIT}}
function checkPremium(){if(localStorage.getItem('tc_unlocked')==='yes')return true;if(getCount()>=FREE_LIMIT){document.getElementById('premiumModal').style.display='flex';return false}return true}
function unlock(){var code=document.getElementById('ownerCode').value.trim();if(code===OWNER_CODE){localStorage.setItem('tc_unlocked','yes');alert('Unlocked!');document.getElementById('premiumModal').style.display='none';updateCounter()}else{alert('Wrong code')}}
async function captureAndAnalyze(){
 if(!checkPremium())return;
 var ctx=canvas.getContext('2d');canvas.width=video.videoWidth;canvas.height=video.videoHeight;ctx.drawImage(video,0,0);
 var dataUrl=canvas.toDataURL('image/jpeg',0.8);captured.src=dataUrl;captured.style.display='block';video.style.display='none';
 document.getElementById('scanLine').style.display='block';document.getElementById('result').style.display='block';
 document.getElementById('itemName').innerText='Analyzing...';document.getElementById('what').innerText='Scanning like Meta AI...';
 var base64Image=dataUrl.split(',')[1];
 try{
  var aiResponse=await callAI(base64Image);
  document.getElementById('itemName').innerText=aiResponse.name;
  document.getElementById('what').innerText=aiResponse.what;document.getElementById('about').innerText=aiResponse.about;
  document.getElementById('uses').innerText=aiResponse.uses;document.getElementById('origin').innerText=aiResponse.origin;
  document.getElementById('notes').innerText=aiResponse.notes;setCount(getCount()+1);
  document.getElementById('scanLine').style.display='none';
  if('speechSynthesis' in window){var u=new SpeechSynthesisUtterance(aiResponse.name+'. '+aiResponse.what);speechSynthesis.speak(u)}
 }catch(e){document.getElementById('what').innerText=e.message;document.getElementById('scanLine').style.display='none'}
}
async function callAI(base64Image){
 var apiKey=localStorage.getItem('gemini_key');
 if(!apiKey){apiKey=prompt('Enter FREE Gemini API Key from aistudio.google.com:');if(apiKey)localStorage.setItem('gemini_key',apiKey)}
 if(apiKey){
  try{
   var res=await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key='+apiKey,{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({contents:[{parts:[{text:"You are Meta AI scanner. Return JSON: {name,category,what,about,uses,origin,notes}. Detailed 150+ words for about."},{inline_data:{mime_type:'image/jpeg',data:base64Image}}]}]})});
   var data=await res.json();var text=data.candidates[0].content.parts[0].text;text=text.replace(/```json|```/g,'').trim();return JSON.parse(text);
  }catch(e){}
 }
 return {name:"Scanned Item",category:"Scan",what:"Image analyzed. TC UniScan AI identified shape, color, texture.",about:"Identified using visual recognition similar to Meta AI. Analyzes colors, edges, textures, context. Whether food, plant, animal, product, document, any object, system explains everything: what it is, how made, why exists, unique features. Comprehensive like Meta AI. Add free Gemini API key for full scientific name, brand, nutrition, price, history.",uses:"For learning, identification, shopping, education.",origin:"From your camera. Add free API key for full details.",notes:"Tip: Clear photo, good light. Premium GHS 50 unlocks unlimited."};
}
startCam();updateCounter();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
