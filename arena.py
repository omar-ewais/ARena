from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
import pytz

app = Flask(__name__)

# ==========================================
# 1. قاعدة بيانات الجداول (مستخرجة من الجداول الرسمية)
# ==========================================
SCHEDULE_DB = {
    "ar_vr": {
        "advisor": "الأستاذ الدكتور/ محمد عبد القاسم",
        "1": {
            "الاحد": [
                {"course": "Fundamentals of Programming", "time": "9:00 - 11:00", "place": "معمل (4) بالدور الرابع", "type": "سكشن", "group": "1", "instructor": "م/ محمود حمزة"},
                {"course": "Fundamentals of Programming", "time": "11:00 - 1:00", "place": "معمل (4) بالدور الرابع", "type": "سكشن", "group": "2", "instructor": "م/ محمود حمزة"},
                {"course": "Introduction to Electronics", "time": "1:00 - 4:00", "place": "مبني 312 الأهليه R", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "أ.د/ محمود يسن"}
            ],
            "الاثنين": [
                {"course": "Communication skills", "time": "9:00 - 11:00", "place": "قاعة 302 الاهليه", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ محمود الصباغ"},
                {"course": "Fundamentals of Programming", "time": "11:00 - 2:00", "place": "قاعة 302 الأهليه", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ محمد عبده"},
                {"course": "Computer Fundamentals", "time": "3:00 - 6:00", "place": "قاعة 302 الأهليه", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ مروة الصديق"}
            ],
            "الثلاثاء": [
                {"course": "Mathematics-1", "time": "9:00 - 11:00", "place": "معمل (1) بالدور الثاني", "type": "سكشن", "group": "1", "instructor": "م/ ميرنا هشام"},
                {"course": "Mathematics 1", "time": "11:00 - 1:00", "place": "قاعة 302 - الأهليه", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "أ.م.د/ مثال السيد"},
                {"course": "Introduction to Electronics", "time": "1:00 - 3:00", "place": "معمل (5) بالدور الرابع", "type": "سكشن", "group": "1", "instructor": "م/ رحمه عزت"}
            ],
            "الاربعاء": [
                {"course": "Computer Fundamentals", "time": "9:00 - 11:00", "place": "معمل (5) بالدور الرابع", "type": "سكشن", "group": "1", "instructor": "م/ هاجر غازی"},
                {"course": "Mathematics-0", "time": "11:00 - 2:00", "place": "مبني 303 الأهليه R", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "أ.د/ رشدي مرعي"}
            ],
            "الخميس": [
                {"course": "Computer Fundamentals", "time": "9:00 - 11:00", "place": "معمل (5) بالدور الرابع", "type": "سكشن", "group": "1", "instructor": "م/ هاجر غازی"},
                {"course": "English Language", "time": "3:00 - 6:00", "place": "مدرج 5 المدرجات المركزية", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ مروة الصديق"}
            ]
        },
        "2": {
            "السبت": [
                {"course": "Operating Systems 1", "time": "9:00 - 11:00", "place": "R 605", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "م/ ايه مطاوع"},
                {"course": "Software Engineering 1", "time": "11:00 - 2:00", "place": "معمل (1) بالدور الثاني", "type": "سكشن", "group": "1", "instructor": "م/ عمر معروف"},
                {"course": "Cybersecurity", "time": "2:00 - 5:00", "place": "معمل (6) بالدور السادس", "type": "سكشن", "group": "1", "instructor": "م/ الاء حسين"}
            ],
            "الاحد": [
                {"course": "Web development", "time": "9:00 - 11:00", "place": "معمل (3) بالدور الثاني", "type": "سكشن", "group": "2", "instructor": "م/ شهد المحمدي"},
                {"course": "Computer Networks", "time": "11:00 - 2:00", "place": "معمل (7) بالدور السابع", "type": "سكشن", "group": "1", "instructor": "م/ احمد هشام"},
                {"course": "Structured Programming", "time": "2:00 - 5:00", "place": "معمل (6) بالدور السادس", "type": "سكشن", "group": "1", "instructor": "م/ عبدالمولى يوسف"}
            ],
            "الاثنين": [
                {"course": "Software Engineering 1", "time": "9:00 - 12:00", "place": "قاعة الدور 1 الأول", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ محمد عبده"},
                {"course": "Web Development", "time": "12:00 - 3:00", "place": "مدرج 605 كلية الذكاء الاصطناعي", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ مروة الصديق"}
            ],
            "الثلاثاء": [
                {"course": "Computer Networks", "time": "11:00 - 2:00", "place": "معمل (3) بالدور الثاني", "type": "سكشن", "group": "2", "instructor": "م/ احمد هشام"},
                {"course": "Structured Programming", "time": "2:00 - 5:00", "place": "معمل (2) بالدور الثاني", "type": "سكشن", "group": "2", "instructor": "م/ عبد المولى يوسف"}
            ],
            "الاربعاء": [
                {"course": "Creative thinking", "time": "9:00 - 12:00", "place": "مبني الأهلية R312", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "ا.د/ تامر مدحت"},
                {"course": "Operating Systems 1", "time": "2:00 - 5:00", "place": "مبني الأهلية R312", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ بسمة حسن"},
                {"course": "Structured Programming", "time": "5:00 - 7:00", "place": "مبني الأهلية R312", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ فاطمة طلعت"}
            ],
            "الخميس": [
                {"course": "Computer Networks", "time": "11:00 - 2:00", "place": "مبنى الأهلية R312", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ زينب حسن"},
                {"course": "Cybersecurity", "time": "2:00 - 5:00", "place": "مبنى الأهلية R312", "type": "محاضرة", "group": "كامل الفرقة", "instructor": "د/ زينب حسن"}
            ]
        }
    },
    "ai": {
        "advisor": "مرشد أكاديمي - سيتم تحديده",
        "1": {
            "السبت": [
                {"course": "Probability & Statistics 1", "time": "9:00 - 11:00", "place": "R2", "type": "سكشن", "group": "1", "instructor": "م/ مي سعيد"},
                {"course": "Introduction to Linear Algebra", "time": "11:00 - 1:00", "place": "R 305", "type": "سكشن", "group": "2", "instructor": "م/ محمد امين"}
            ]
        },
        "2": {
            "السبت": [
                {"course": "Object Oriented Programming", "time": "9:00 - 11:00", "place": "معمل (3) بالدور الثاني", "type": "سكشن", "group": "1", "instructor": "م/ بشار جمال"},
                {"course": "Information Retrieval", "time": "11:00 - 2:00", "place": "معمل (1) بالدور الثاني", "type": "سكشن", "group": "1", "instructor": "م/ عاطف موسى"}
            ]
        }
    }
}

# ==========================================
# 2. واجهة الويب (HTML & JS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arena | المرشد الأكاديمي الذكي</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-color: #020617; --card-bg: #0f172a; --accent: #0ea5e9; --accent-hover: #38bdf8;
            --text-main: #f8fafc; --text-muted: #94a3b8; --border: rgba(255, 255, 255, 0.08);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); height: 100vh; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        
        .app-container {
            width: 100%; max-width: 900px; height: 90vh; background: var(--card-bg); border: 1px solid var(--border);
            border-radius: 24px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6); display: flex; flex-direction: column; overflow: hidden; position: relative;
        }

        .screen { display: none; flex-direction: column; height: 100%; padding: 40px; justify-content: center; align-items: center; }
        .screen.active { display: flex; }

        /* Splash Screen */
        .splash-content { text-align: center; animation: pulse 2s infinite; }
        .splash-content i { font-size: 4rem; color: var(--accent); margin-bottom: 20px; }
        .splash-content h1 { font-size: 2.5rem; letter-spacing: 2px; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }

        /* Headers */
        .screen-header { text-align: center; margin-bottom: 40px; width: 100%; }
        .screen-header h2 { color: var(--accent); font-size: 1.8rem; margin-bottom: 8px; }
        .screen-header p { color: var(--text-muted); font-size: 1rem; }

        /* Grid Cards */
        .grid-layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; width: 100%; max-width: 700px; }
        .card { 
            background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border); border-radius: 16px; 
            padding: 30px 20px; text-align: center; cursor: pointer; transition: 0.3s; 
        }
        .card:hover { transform: translateY(-5px); border-color: var(--accent); background: rgba(14, 165, 233, 0.05); }
        .card i { font-size: 2.5rem; color: var(--accent); margin-bottom: 15px; }
        .card h3 { font-size: 1.2rem; }

        /* Main Menu */
        .menu-list { display: flex; flex-direction: column; gap: 15px; width: 100%; max-width: 600px; }
        .menu-item { 
            display: flex; align-items: center; gap: 20px; background: rgba(255, 255, 255, 0.03); 
            padding: 20px; border-radius: 16px; cursor: pointer; border: 1px solid var(--border); transition: 0.3s; 
        }
        .menu-item:hover { border-color: var(--accent); background: rgba(255, 255, 255, 0.06); }
        .menu-item i { font-size: 2rem; color: var(--accent); width: 40px; text-align: center; }
        .menu-item div h4 { font-size: 1.1rem; margin-bottom: 4px; }
        .menu-item div p { font-size: 0.85rem; color: var(--text-muted); }

        .back-btn { align-self: flex-start; background: none; border: none; color: var(--text-muted); font-size: 1rem; cursor: pointer; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }
        .back-btn:hover { color: var(--text-main); }

        /* Chat Section */
        .chat-container { display: flex; flex-direction: column; height: 100%; width: 100%; }
        .chat-messages { flex-grow: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .msg { display: flex; gap: 12px; max-width: 80%; }
        .msg.bot { align-self: flex-start; }
        .msg.user { align-self: flex-end; flex-direction: row-reverse; }
        .msg-avatar { width: 38px; height: 38px; background: rgba(255,255,255,0.05); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
        .msg-bubble { background: rgba(255, 255, 255, 0.05); padding: 12px 16px; border-radius: 12px; font-size: 0.95rem; line-height: 1.6; }
        .msg.user .msg-bubble { background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.3); color: var(--accent); }
        
        .chat-input { display: flex; gap: 10px; padding: 20px; border-top: 1px solid var(--border); }
        .chat-input input { flex-grow: 1; background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 15px; border-radius: 12px; color: #fff; outline: none; }
        .chat-input button { background: var(--accent); border: none; color: #fff; width: 55px; border-radius: 12px; font-size: 1.2rem; cursor: pointer; }

        /* Modal / Results */
        .modal { display: none; position: absolute; inset: 0; background: rgba(2, 6, 23, 0.95); z-index: 100; flex-direction: column; padding: 20px; align-items: center; }
        .modal-content { background: var(--card-bg); border: 1px solid var(--border); width: 100%; max-width: 700px; border-radius: 20px; padding: 30px; max-height: 85vh; overflow-y: auto; position: relative; margin-top: 40px; }
        .close-modal { position: absolute; top: 20px; left: 20px; background: none; border: none; color: #ef4444; font-size: 1.5rem; cursor: pointer; }
        
        .data-item { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-right: 4px solid var(--accent); border-radius: 10px; padding: 15px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="app-container">
        
        <!-- 0. Splash Screen -->
        <div id="screen-splash" class="screen active">
            <div class="splash-content">
                <i class="fa-solid fa-graduation-cap"></i>
                <h1>ARENA</h1>
                <p style="color: var(--accent); font-size: 1.2rem; margin-top: 10px;">نظام الإرشاد الأكاديمي الذكي</p>
            </div>
        </div>

        <!-- 1. Program Selection -->
        <div id="screen-program" class="screen">
            <div class="screen-header">
                <h2>اختر برنامجك الدراسي</h2>
                <p>جامعة كفر الشيخ الأهلية - 2026/2027</p>
            </div>
            <div class="grid-layout">
                <div class="card" onclick="selectProgram('ar_vr', 'الواقع المعزز والافتراضي')">
                    <i class="fa-solid fa-vr-cardboard"></i>
                    <h3>الواقع الافتراضي والمعزز</h3>
                </div>
                <div class="card" onclick="selectProgram('ai', 'الذكاء الاصطناعي')">
                    <i class="fa-solid fa-brain"></i>
                    <h3>الذكاء الاصطناعي</h3>
                </div>
            </div>
        </div>

        <!-- 2. Year Selection -->
        <div id="screen-year" class="screen">
            <button class="back-btn" onclick="nav('screen-year', 'screen-program')"><i class="fa-solid fa-arrow-right"></i> رجوع</button>
            <div class="screen-header">
                <h2>اختر الفرقة الدراسية</h2>
                <p id="selected-prog-label"></p>
            </div>
            <div class="grid-layout">
                <div class="card" onclick="selectYear('1')">
                    <i class="fa-solid fa-1"></i>
                    <h3>الفرقة الأولى</h3>
                </div>
                <div class="card" onclick="selectYear('2')">
                    <i class="fa-solid fa-2"></i>
                    <h3>الفرقة الثانية</h3>
                </div>
            </div>
        </div>

        <!-- 3. Main Menu -->
        <div id="screen-menu" class="screen" style="padding: 30px;">
            <button class="back-btn" onclick="nav('screen-menu', 'screen-year')"><i class="fa-solid fa-arrow-right"></i> تغيير الفرقة</button>
            <div class="screen-header" style="margin-bottom: 25px;">
                <h2 id="menu-title">القائمة الرئيسية</h2>
            </div>
            <div class="menu-list">
                <div class="menu-item" onclick="fetchData('schedule')">
                    <i class="fa-solid fa-calendar-days"></i>
                    <div><h4>الجدول الدراسي</h4><p>جدول المحاضرات والسكاشن الأسبوعي كامل</p></div>
                </div>
                <div class="menu-item" onclick="nav('screen-menu', 'screen-group')">
                    <i class="fa-solid fa-calendar-check"></i>
                    <div><h4>محاضرات وسكاشن اليوم</h4><p>تصفية الجدول لليوم الحالي حسب مجموعتك</p></div>
                </div>
                <div class="menu-item" onclick="fetchData('staff')">
                    <i class="fa-solid fa-users"></i>
                    <div><h4>أعضاء هيئة التدريس</h4><p>أسماء الدكاترة والمدرسين لبرنامجك</p></div>
                </div>
                <div class="menu-item" onclick="fetchData('advisor')">
                    <i class="fa-solid fa-user-tie"></i>
                    <div><h4>المرشد الأكاديمي</h4><p>معلومات المرشد الأكاديمي لبرنامجك</p></div>
                </div>
                <div class="menu-item" onclick="nav('screen-menu', 'screen-chat')">
                    <i class="fa-solid fa-robot"></i>
                    <div><h4>المساعد الذكي (Chat)</h4><p>اسألني عن متطلبات المواد واللائحة</p></div>
                </div>
            </div>
        </div>

        <!-- 4. Group Selection for Today's Schedule -->
        <div id="screen-group" class="screen">
            <button class="back-btn" onclick="nav('screen-group', 'screen-menu')"><i class="fa-solid fa-arrow-right"></i> رجوع</button>
            <div class="screen-header">
                <h2>اختر رقم مجموعتك</h2>
                <p>لعرض سكاشن ومحاضرات اليوم الخاص بك</p>
            </div>
            <div class="grid-layout" style="grid-template-columns: repeat(4, 1fr);">
                <div class="card" style="padding: 20px;" onclick="fetchTodaySections('1')"><h3>1</h3></div>
                <div class="card" style="padding: 20px;" onclick="fetchTodaySections('2')"><h3>2</h3></div>
                <div class="card" style="padding: 20px;" onclick="fetchTodaySections('3')"><h3>3</h3></div>
                <div class="card" style="padding: 20px;" onclick="fetchTodaySections('4')"><h3>4</h3></div>
            </div>
        </div>

        <!-- 5. Chat Interface -->
        <div id="screen-chat" class="screen" style="padding: 0;">
            <div class="chat-container">
                <div style="padding: 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; background: rgba(0,0,0,0.2);">
                    <button class="back-btn" style="margin:0;" onclick="nav('screen-chat', 'screen-menu')"><i class="fa-solid fa-arrow-right"></i></button>
                    <h3 style="margin-right: 15px; color: var(--accent);">المساعد الأكاديمي</h3>
                </div>
                <div class="chat-messages" id="chat-messages">
                    <div class="msg bot"><div class="msg-avatar">🤖</div><div class="msg-bubble">أهلاً بك! يمكنك سؤالي هنا عن أي مادة وتفاصيلها.</div></div>
                </div>
                <div class="chat-input">
                    <input type="text" id="chat-input-field" placeholder="اكتب سؤالك (مثال: متطلبات مادة structured)..." onkeypress="if(event.key === 'Enter') sendChat()">
                    <button onclick="sendChat()"><i class="fa-solid fa-paper-plane"></i></button>
                </div>
            </div>
        </div>

        <!-- 6. Results Modal -->
        <div id="result-modal" class="modal">
            <div class="modal-content">
                <button class="close-modal" onclick="closeModal()"><i class="fa-solid fa-xmark"></i></button>
                <div id="modal-body"></div>
            </div>
        </div>

    </div>

    <script>
        let userData = { progId: '', progName: '', year: '' };

        // Splash screen timeout
        setTimeout(() => { nav('screen-splash', 'screen-program'); }, 2000);

        function nav(hide, show) {
            document.getElementById(hide).classList.remove('active');
            document.getElementById(show).classList.add('active');
        }

        function selectProgram(id, name) {
            userData.progId = id; userData.progName = name;
            document.getElementById('selected-prog-label').innerText = name;
            nav('screen-program', 'screen-year');
        }

        function selectYear(yr) {
            userData.year = yr;
            document.getElementById('menu-title').innerText = `${userData.progName} - الفرقة ${yr === '1' ? 'الأولى' : 'الثانية'}`;
            nav('screen-year', 'screen-menu');
        }

        function closeModal() { document.getElementById('result-modal').style.display = 'none'; }

        async function fetchData(action) {
            const res = await fetch('/api/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action, program: userData.progId, level: userData.year })
            });
            const data = await res.json();
            document.getElementById('modal-body').innerHTML = data.html;
            document.getElementById('result-modal').style.display = 'flex';
        }

        async function fetchTodaySections(group) {
            const res = await fetch('/api/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'today', program: userData.progId, level: userData.year, group: group })
            });
            const data = await res.json();
            document.getElementById('modal-body').innerHTML = data.html;
            nav('screen-group', 'screen-menu'); 
            document.getElementById('result-modal').style.display = 'flex';
        }

        async function sendChat() {
            const input = document.getElementById('chat-input-field');
            const text = input.value.trim();
            if(!text) return;
            
            appendMsg(text, 'user', '👤');
            input.value = '';

            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, program: userData.progId, level: userData.year })
            });
            const data = await res.json();
            appendMsg(data.response, 'bot', '🤖');
        }

        function appendMsg(text, type, icon) {
            const container = document.getElementById('chat-messages');
            container.innerHTML += `<div class="msg ${type}"><div class="msg-avatar">${icon}</div><div class="msg-bubble">${text}</div></div>`;
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""

# ==========================================
# 3. توجيهات ومعالجة البيانات (Backend API)
# ==========================================
@app.route("/")
def index():
    return send_file(os.path.join(app.root_path, "arena_frontend.html"))

@app.route("/api/data", methods=["POST"])
def api_data():
    req = request.json
    action = req.get("action")
    prog = req.get("program")
    lvl = req.get("level")
    
    schedule = SCHEDULE_DB.get(prog, {}).get(lvl, {})
    html = ""

    # 1. الجدول الدراسي الكامل
    if action == "schedule":
        html = "<h2 style='color:var(--accent); margin-bottom:20px;'><i class='fa-solid fa-table'></i> الجدول الدراسي الكامل</h2>"
        if not schedule:
            return jsonify({"html": "<p>لا توجد بيانات متاحة لهذا الجدول حالياً.</p>"})
        for day, sessions in schedule.items():
            html += f"<h3 style='margin-top:15px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:5px;'>يوم {day}</h3>"
            for s in sessions:
                group_text = f"مجموعة {s['group']}" if s['group'] != "كامل الفرقة" else "الفرقة كاملة"
                html += f"<div class='data-item'>" \
                        f"<strong style='font-size:1.1rem;'>{s['course']}</strong> <span style='color:var(--accent);'>({s['type']} - {group_text})</span><br>" \
                        f"<div style='margin-top:8px; color:var(--text-muted);'>" \
                        f"<i class='fa-solid fa-clock'></i> {s['time']} &nbsp;|&nbsp; " \
                        f"<i class='fa-solid fa-location-dot'></i> {s['place']}<br>" \
                        f"<i class='fa-solid fa-user'></i> {s['instructor']}</div></div>"

    # 2. سكاشن ومحاضرات اليوم (مصفاة برقم المجموعة)
    elif action == "today":
        group = req.get("group")
        # حساب اليوم الحالي بتوقيت القاهرة
        cairo_tz = pytz.timezone('Africa/Cairo')
        today_en = datetime.now(cairo_tz).strftime("%A")
        days_map = {"Saturday":"السبت", "Sunday":"الاحد", "Monday":"الاثنين", "Tuesday":"الثلاثاء", "Wednesday":"الاربعاء", "Thursday":"الخميس", "Friday":"الجمعة"}
        today_ar = days_map.get(today_en, "السبت")

        greeting = "صباح الخير" if datetime.now(cairo_tz).hour < 12 else "مساء الخير"
        html = f"<h2 style='color:var(--accent); margin-bottom:20px;'>{greeting}! دي محاضراتك النهارده ({today_ar}):</h2>"
        
        today_sessions = schedule.get(today_ar, [])
        has_classes = False
        
        for s in today_sessions:
            # تظهر المادة إذا كانت "محاضرة" (للكل) أو "سكشن" ومجموعتها تطابق المجموعة المختارة
            if s['type'] == 'محاضرة' or s['group'] == str(group):
                has_classes = True
                time_start = s['time'].split('-')[0].strip() if '-' in s['time'] else s['time']
                html += f"<div class='data-item' style='border-right-color: #10b981;'>" \
                        f"<strong style='font-size:1.1rem;'>{time_start}</strong> &nbsp;—&nbsp; {s['course']} <span style='color:#10b981'>({s['type']})</span><br>" \
                        f"<div style='margin-top:8px; color:var(--text-muted);'>" \
                        f"<i class='fa-solid fa-location-dot'></i> {s['place']} &nbsp;|&nbsp; <i class='fa-solid fa-user'></i> {s['instructor']}</div></div>"
        
        if not has_classes:
            html += "<p style='color:var(--text-muted); text-align:center; padding: 20px;'>معندكش محاضرات أو سكاشن النهارده لمجموعتك، استمتع بيومك! 🎉</p>"

    # 3. أعضاء هيئة التدريس
    elif action == "staff":
        html = "<h2 style='color:var(--accent); margin-bottom:20px;'><i class='fa-solid fa-users'></i> أعضاء هيئة التدريس</h2>"
        staff = set()
        for sessions in schedule.values():
            for s in sessions:
                staff.add(s['instructor'])
        if not staff:
            return jsonify({"html": "<p>لا توجد بيانات متاحة.</p>"})
        for st in staff:
            html += f"<div class='data-item' style='padding: 15px;'><i class='fa-solid fa-user-check' style='color:var(--accent); margin-left:10px;'></i> {st}</div>"

    # 4. المرشد الأكاديمي
    elif action == "advisor":
        advisor = SCHEDULE_DB.get(prog, {}).get("advisor", "غير محدد")
        html = f"<div style='text-align:center; padding: 40px 20px;'>" \
               f"<i class='fa-solid fa-user-tie' style='font-size:4rem; color:var(--accent); margin-bottom:20px;'></i>" \
               f"<h2 style='margin-bottom:10px;'>المرشد الأكاديمي الخاص بك</h2>" \
               f"<h3 style='color:var(--accent); font-size:1.5rem;'>{advisor}</h3>" \
               f"<p style='color:var(--text-muted); margin-top:15px; line-height:1.6;'>" \
               f"يمكنك التوجه لسيادته في الساعات المكتبية لأي استشارات أكاديمية، أو حل مشكلات تسجيل المواد والحذف والإضافة.</p></div>"

    return jsonify({"html": html})

# ==========================================
# 4. محرك الشات بوت المبسط
# ==========================================
@app.route("/api/chat", methods=["POST"])
def api_chat():
    req = request.json
    text = req.get("message").lower()
    prog = req.get("program")
    lvl = req.get("level")
    
    schedule = SCHEDULE_DB.get(prog, {}).get(lvl, {})
    
    # البحث عن معلومات مادة معينة
    for day, sessions in schedule.items():
        for s in sessions:
            if s['course'].lower() in text or any(word in text for word in s['course'].lower().split() if len(word)>3):
                reply = f"📖 مادة {s['course']}:\nهذه المادة تُدرس يوم {day} ({s['time']}) في {s['place']}.\nالمحاضر: {s['instructor']}."
                
                # حفظ المحادثة
                with open("chat_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"Student: {req.get('message')}\\nArena: {reply}\\n---\\n")
                
                return jsonify({"response": reply})

    # رد افتراضي
    default_reply = "عفواً، يمكنك سؤالي عن اسم مادة معينة (مثال: متطلبات mathematics) وسأجلب لك تفاصيلها من الجدول الخاص بك."
    return jsonify({"response": default_reply})

if __name__ == "__main__":
    app.run(debug=True)
