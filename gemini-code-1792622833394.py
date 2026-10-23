from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

SCHEDULE_DB = {
    "ar_vr": {
        "advisor": "الأستاذ الدكتور/ محمد عبده قاسم",
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
        "advisor": "الأستاذ الدكتور/ محمود ياسين",
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARENA | المرشد الأكاديمي الذكي</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-color: #020617; --card-bg: #0f172a; --accent: #0ea5e9; --accent-hover: #38bdf8;
            --text-main: #f8fafc; --text-muted: #94a3b8; --border: rgba(255,255,255,0.08);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: var(--bg-color); color: var(--text-main); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 24px; }
        .app-container {
            width: min(100%, 920px); min-height: 82vh; background: var(--card-bg); border: 1px solid var(--border);
            border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); display: flex; flex-direction: column; overflow: hidden; position: relative;
        }
        .screen { display: none; flex-direction: column; height: 100%; padding: 32px; }
        .screen.active { display: flex; }
        .splash-content { text-align: center; animation: pulse 2s infinite; margin: auto; }
        .splash-content i { font-size: 4rem; color: var(--accent); margin-bottom: 20px; }
        .splash-content h1 { font-size: 2.5rem; letter-spacing: 2px; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .screen-header { text-align: center; margin-bottom: 28px; }
        .screen-header h2 { color: var(--accent); font-size: 1.8rem; margin-bottom: 8px; }
        .screen-header p { color: var(--text-muted); font-size: 1rem; }
        .grid-layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; width: 100%; max-width: 720px; margin: 0 auto; }
        .card { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 16px; padding: 30px 20px; text-align: center; cursor: pointer; transition: 0.3s; }
        .card:hover { transform: translateY(-5px); border-color: var(--accent); background: rgba(14,165,233,0.05); }
        .card i { font-size: 2.5rem; color: var(--accent); margin-bottom: 15px; }
        .card h3 { font-size: 1.2rem; }
        .back-btn { align-self: flex-start; background: none; border: none; color: var(--text-muted); font-size: 1rem; cursor: pointer; margin-bottom: 22px; display: flex; align-items: center; gap: 8px; }
        .back-btn:hover { color: var(--text-main); }
        .year-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 18px; width: 100%; max-width: 520px; margin: 0 auto; }
        .year-btn {
            background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 16px; color: var(--text-main);
            padding: 24px 18px; font-size: 1.1rem; cursor: pointer; transition: 0.2s;
        }
        .year-btn:hover { border-color: var(--accent); }
        .summary-box { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 16px; padding: 18px 20px; margin-bottom: 18px; }
        .summary-box strong { color: var(--accent); }
        .schedule-list { display: flex; flex-direction: column; gap: 14px; }
        .data-item { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-right: 4px solid var(--accent); border-radius: 10px; padding: 16px; }
        .data-item h4 { margin-bottom: 8px; font-size: 1.1rem; }
        .data-item p { color: var(--text-muted); line-height: 1.8; font-size: 0.96rem; }
        .chat-container { display: flex; flex-direction: column; height: 100%; width: 100%; }
        .chat-messages { flex-grow: 1; overflow-y: auto; padding: 18px; display: flex; flex-direction: column; gap: 12px; }
        .msg { display: flex; gap: 12px; max-width: 80%; }
        .msg.bot { align-self: flex-start; }
        .msg.user { align-self: flex-end; flex-direction: row-reverse; }
        .msg-avatar { width: 38px; height: 38px; background: rgba(255,255,255,0.05); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.05rem; }
        .msg-bubble { background: rgba(255,255,255,0.05); padding: 12px 16px; border-radius: 12px; line-height: 1.6; }
        .msg.user .msg-bubble { background: rgba(14,165,233,0.15); border: 1px solid rgba(14,165,233,0.3); color: var(--accent); }
        .chat-input { display: flex; gap: 10px; padding: 16px 18px; border-top: 1px solid var(--border); }
        .chat-input input { flex: 1; background: rgba(255,255,255,0.03); border: 1px solid var(--border); padding: 15px; border-radius: 12px; color: #fff; outline: none; }
        .chat-input button { background: var(--accent); border: none; color: white; width: 56px; border-radius: 12px; cursor: pointer; font-size: 1.1rem; }
        .modal { display: none; position: absolute; inset: 0; background: rgba(2,6,23,0.96); z-index: 100; padding: 20px; }
        .modal.active { display: flex; }
        .modal-content { background: var(--card-bg); border: 1px solid var(--border); width: min(720px, 100%); margin: auto; border-radius: 22px; padding: 24px; max-height: 85vh; overflow-y: auto; position: relative; }
        .close-modal { position: absolute; left: 18px; top: 16px; background: none; border: none; color: #ef4444; font-size: 1.4rem; cursor: pointer; }
        @media (max-width: 640px) {
            .screen { padding: 22px 18px; }
            .app-container { min-height: 90vh; }
            .msg { max-width: 92%; }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div id="screen-splash" class="screen active">
            <div class="splash-content">
                <i class="fa-solid fa-graduation-cap"></i>
                <h1>ARENA</h1>
                <p style="color: var(--accent); font-size: 1.2rem; margin-top: 12px;">نظام الإرشاد الأكاديمي الذكي</p>
            </div>
        </div>

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

        <div id="screen-year" class="screen">
            <button class="back-btn" onclick="nav('screen-year', 'screen-program')"><i class="fa-solid fa-arrow-right"></i> رجوع</button>
            <div class="screen-header">
                <h2>اختر الفرقة الدراسية</h2>
                <p id="selected-prog">البرنامج</p>
            </div>
            <div class="year-grid">
                <button class="year-btn" onclick="selectYear('1')">الفرقة الأولى</button>
                <button class="year-btn" onclick="selectYear('2')">الفرقة الثانية</button>
            </div>
        </div>

        <div id="screen-menu" class="screen">
            <button class="back-btn" onclick="nav('screen-menu', 'screen-year')"><i class="fa-solid fa-arrow-right"></i> رجوع</button>
            <div class="screen-header">
                <h2>القائمة الرئيسية</h2>
                <p id="menu-program-label">البرنامج</p>
            </div>
            <div class="grid-layout">
                <div class="card" onclick="showSchedule()">
                    <i class="fa-solid fa-calendar-days"></i>
                    <h3>الجدول الدراسي</h3>
                </div>
                <div class="card" onclick="showChat()">
                    <i class="fa-solid fa-comments"></i>
                    <h3>المساعدة الذكية</h3>
                </div>
            </div>
        </div>

        <div id="screen-chat" class="screen">
            <button class="back-btn" onclick="nav('screen-chat', 'screen-menu')"><i class="fa-solid fa-arrow-right"></i> رجوع</button>
            <div class="screen-header">
                <h2>المساعد الذكي</h2>
                <p id="chat-header">الاستفسار عن الجدول</p>
            </div>
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages"></div>
                <div class="chat-input">
                    <input id="chatInput" type="text" placeholder="اكتب سؤالك مثل: جدول الاحد، أو وقت مادة البرمجة" aria-label="رسالة المستخدم">
                    <button id="sendChatBtn" type="button" onclick="sendChat()"><i class="fa-solid fa-paper-plane"></i></button>
                </div>
            </div>
        </div>
    </div>

    <div id="scheduleModal" class="modal">
        <div class="modal-content">
            <button class="close-modal" onclick="closeScheduleModal()"><i class="fa-solid fa-xmark"></i></button>
            <div id="scheduleContent"></div>
        </div>
    </div>

    <script>
        const state = { program: 'ar_vr', year: '1', programLabel: 'الواقع المعزز والافتراضي' };
        const dayMap = {
            'السبت': 'السبت',
            'الاحد': 'الأحد',
            'الاثنين': 'الاثنين',
            'الثلاثاء': 'الثلاثاء',
            'الاربعاء': 'الأربعاء',
            'الخميس': 'الخميس'
        };

        function nav(fromId, toId) {
            document.getElementById(fromId).classList.remove('active');
            document.getElementById(toId).classList.add('active');
        }

        function showScreen(id) {
            document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
            document.getElementById(id).classList.add('active');
        }

        function selectProgram(program, label) {
            state.program = program;
            state.programLabel = label;
            document.getElementById('selected-prog').textContent = label;
            document.getElementById('menu-program-label').textContent = label;
            document.getElementById('chat-header').textContent = 'الاستفسار عن الجدول - ' + label;
            showScreen('screen-year');
        }

        function selectYear(year) {
            state.year = year;
            nav('screen-year', 'screen-menu');
        }

        function renderSchedule(days) {
            const content = document.getElementById('scheduleContent');
            const items = Object.entries(days || {}).map(([day, courses]) => {
                const courseHtml = (courses || []).map(item => `
                    <div class="data-item">
                        <h4>${item.course}</h4>
                        <p><strong>الوقت:</strong> ${item.time}</p>
                        <p><strong>المكان:</strong> ${item.place}</p>
                        <p><strong>النوع:</strong> ${item.type} | <strong>المجموعة:</strong> ${item.group}</p>
                        <p><strong>المحاضر:</strong> ${item.instructor}</p>
                    </div>
                `).join('');
                return `
                    <div class="summary-box">
                        <strong>${day}</strong>
                        <div class="schedule-list">${courseHtml || '<p>لا توجد محاضرات في هذا اليوم.</p>'}</div>
                    </div>
                `;
            }).join('');

            content.innerHTML = `
                <h2 style="margin-bottom: 18px; color: var(--accent);">${state.programLabel}</h2>
                <div class="summary-box">
                    <strong>الفرقة:</strong> ${state.year === '1' ? 'الأولى' : 'الثانية'}<br>
                    <strong>الموجه:</strong> ${state.advisor || 'غير محدد'}
                </div>
                ${items || '<p>لا توجد بيانات للفرقة الحالية.</p>'}
            `;
        }

        function fetchSchedule() {
            fetch(`/api/schedule?program=${state.program}&year=${state.year}`)
                .then(res => res.json())
                .then(data => {
                    state.advisor = data.advisor || '';
                    renderSchedule(data.days || {});
                })
                .catch(() => {
                    document.getElementById('scheduleContent').innerHTML = '<p>تعذر تحميل الجدول.</p>';
                });
        }

        function showSchedule() {
            fetchSchedule();
            document.getElementById('scheduleModal').classList.add('active');
        }

        function closeScheduleModal() {
            document.getElementById('scheduleModal').classList.remove('active');
        }

        function showChat() {
            showScreen('screen-chat');
            if (!document.getElementById('chatMessages').children.length) {
                addMessage('bot', 'مرحباً! يمكنك أن تسأل عن يوم معين أو مادة أو وقت محاضرة.');
            }
        }

        function addMessage(role, text) {
            const msg = document.createElement('div');
            msg.className = `msg ${role}`;
            msg.innerHTML = `
                <div class="msg-avatar"><i class="fa-solid ${role === 'bot' ? 'fa-robot' : 'fa-user'}"></i></div>
                <div class="msg-bubble">${text}</div>
            `;
            document.getElementById('chatMessages').appendChild(msg);
            document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
        }

        function sendChat() {
            const input = document.getElementById('chatInput');
            const message = (input.value || '').trim();
            if (!message) return;
            addMessage('user', message);
            input.value = '';

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, program: state.program, year: state.year })
            })
            .then(res => res.json())
            .then(data => {
                addMessage('bot', data.reply || 'لا توجد إجابة مناسبة في الوقت الحالي.');
            })
            .catch(() => addMessage('bot', 'حدثت مشكلة أثناء معالجة سؤالك.'));
        }

        document.getElementById('chatInput').addEventListener('keydown', function (e) {
            if (e.key === 'Enter') sendChat();
        });

        setTimeout(() => {
            showScreen('screen-program');
        }, 1400);
    </script>
</body>
</html>
"""


def get_schedule(program, year):
    return SCHEDULE_DB.get(program, {}).get(year, {})


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/schedule')
def schedule_api():
    program = request.args.get('program', 'ar_vr')
    year = request.args.get('year', '1')
    timetable = get_schedule(program, year)
    return jsonify({
        'program': program,
        'year': year,
        'advisor': SCHEDULE_DB.get(program, {}).get('advisor', ''),
        'days': timetable
    })


@app.route('/api/chat', methods=['POST'])
def chat_api():
    payload = request.get_json(silent=True) or {}
    message = (payload.get('message') or '').strip()
    program = payload.get('program', 'ar_vr')
    year = payload.get('year', '1')

    if not message:
        return jsonify({'reply': 'أعطني سؤالاً عن الجدول الدراسي.'})

    text = message.lower()
    timetable = get_schedule(program, year)
    days = list(timetable.keys())
    found_day = None
    for day in days:
        if day in text or day.replace('ال', '') in text:
            found_day = day
            break

    if 'استاذ' in text or 'أستاذ' in text or 'موجه' in text or 'advisor' in text:
        return jsonify({'reply': f"الموجه الأكاديمي: {SCHEDULE_DB.get(program, {}).get('advisor', 'غير متوفر')}"})

    if found_day:
        items = timetable.get(found_day, [])
        if not items:
            return jsonify({'reply': f'لا توجد محاضرات في يوم {found_day} للفرقة {year}.'})
        lines = [f"في يوم {found_day}:"]
        for item in items:
            lines.append(f"- {item['course']} | {item['time']} | {item['place']} | {item['instructor']}")
        return jsonify({'reply': '\n'.join(lines)})

    if 'جدول' in text or 'موعد' in text or 'مواعيد' in text or 'جدولي' in text:
        if not timetable:
            return jsonify({'reply': 'لا يوجد جدول متاح لهذه الفرقة.'})
        summary = []
        for day, items in timetable.items():
            summary.append(f"{day}: {len(items)} مادة")
        return jsonify({'reply': ' | '.join(summary)})

    if 'مادة' in text or 'course' in text:
        matches = []
        for day, items in timetable.items():
            for item in items:
                if item['course'].lower() in text or text in item['course'].lower():
                    matches.append(f"{day}: {item['course']} — {item['time']} — {item['place']}")
        if matches:
            return jsonify({'reply': '\n'.join(matches)})

    return jsonify({'reply': 'يمكنني مساعدتك في معرفة جدول يوم معين أو اسم مادة أو الموجه الأكاديمي. مثال: "جدول الاحد" أو "مادة البرمجة".'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
