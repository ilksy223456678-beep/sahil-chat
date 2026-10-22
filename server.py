import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
messages = []

PAGE = """
<h2>Sahil Chat 💬</h2>
<input id="name" placeholder="Tumhara naam">
<input id="msg" placeholder="Message likho">
<button onclick="send()">Send</button>
<div id="chat"></div>
<script>
async function send() {
  const name = document.getElementById('name').value.trim();
  const msg = document.getElementById('msg').value.trim();
  if (!name || !msg) return;
  await fetch('/send', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({name, msg})
  });
  document.getElementById('msg').value = '';
  load();
}
async function load() {
  const r = await fetch('/messages');
  const data = await r.json();
  const chat = document.getElementById('chat');
  chat.replaceChildren();
  data.forEach(m => {
    const p = document.createElement('p');
    p.textContent = m.name + ': ' + m.msg;
    chat.appendChild(p);
  });
}
setInterval(load, 2000);
load();
</script>
"""

@app.route('/')
def home():
    return render_template_string(PAGE)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()[:30]
    msg = str(data.get('msg', '')).strip()[:1000]
    if not name or not msg:
        return jsonify({'error': 'Name aur message zaroori hai'}), 400
    messages.append({'name': name, 'msg': msg})
    return jsonify({'status': 'sent'})

@app.route('/messages')
def get_messages():
    return jsonify(messages[-100:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
