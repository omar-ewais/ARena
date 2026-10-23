from flask import Flask, render_template, jsonify, request
from pathlib import Path

app = Flask(__name__)

# Data is based on the Python code supplied by the project owner.
DATA = {
    "AI": {
        "advisor": {"name": "الأستاذ الدكتور محمود ياسين", "office": "الدور الرابع من كلية الذكاء الاصطناعي"},
        "levels": {
            "1": {
                "schedule": "/static/schedules/schedule-1.png",
                "doctors": [
                    {"name":"د. محمود الصباغ", "courses":"English"},
                    {"name":"د. محمد عبده قاسم", "courses":"Structured Programming"},
                    {"name":"د. تامر مدحت", "courses":"Computer Fundamentals"},
                    {"name":"د. بسمة حسن", "courses":"Introduction to Linear Algebra"},
                    {"name":"د. منال السيد", "courses":"Math 1"},
                    {"name":"د. محمود ياسين", "courses":"Electric Circuits"},
                    {"name":"د. رشدي مرعي", "courses":"Math Zero; Probability and Statistics 1"}
                ],
                "assistants": [
                    {"name":"م. آلاء أيمن", "courses":"Math 1"},
                    {"name":"م. مي سعيد", "courses":"Probability and Statistics 1"},
                    {"name":"م. محمد أمين", "courses":"Introduction to Linear Algebra"},
                    {"name":"م. مروة خليل", "courses":"Computer Fundamentals"},
                    {"name":"م. هاجر علي", "courses":"Electric Circuits"},
                    {"name":"م. عبدالمولى يوسف", "courses":"Structured Programming"}
                ]
            },
            "2": {
                "schedule": "/static/schedules/schedule-2.png",
                "doctors": [
                    {"name":"د. محمود الصباغ", "courses":"Introduction to Machine Learning"},
                    {"name":"د. زينب حسن", "courses":"Computer Networks"},
                    {"name":"د. تامر مدحت", "courses":"Introduction to Computer Vision and Robotics"},
                    {"name":"د. بسمة حسن", "courses":"Computer Architecture"},
                    {"name":"د. فاطمة طلعت", "courses":"Information Retrieval and Web Search; Object Oriented Programming"},
                    {"name":"د. محمود ياسين", "courses":"Scientific Writing"}
                ],
                "assistants": [
                    {"name":"م. بشار جمال", "courses":"Object Oriented Programming"},
                    {"name":"م. حسن سعد", "courses":"Introduction to Machine Learning"},
                    {"name":"م. عبد الرحمن أبو ستيت", "courses":"Computer Architecture"},
                    {"name":"م. عاطف موسى", "courses":"Object Oriented Programming"},
                    {"name":"م. أحمد هشام", "courses":"Computer Networks"},
                    {"name":"م. عبدالرؤوف حواش", "courses":"Introduction to Computer Vision and Robotics"}
                ]
            }
        }
    },
    "VR": {
        "advisor": {"name": "الأستاذ الدكتور محمد عبده قاسم", "office": "الدور الثاني من كلية الذكاء الاصطناعي"},
        "levels": {
            "1": {
                "schedule": "/static/schedules/schedule-3.png",
                "doctors": [
                    {"name":"د. مروة الصديق", "courses":"Computer Fundamentals; English"},
                    {"name":"د. محمد عبده قاسم", "courses":"Fundamentals of Programming"},
                    {"name":"د. منال السيد", "courses":"Math 1"},
                    {"name":"د. محمود ياسين", "courses":"Introduction to Electronics"},
                    {"name":"د. محمود الصباغ", "courses":"Communication Skills"},
                    {"name":"د. رشدي مرعي", "courses":"Math Zero"}
                ],
                "assistants": [
                    {"name":"م. رحمة عزت", "courses":"Introduction to Electronics"},
                    {"name":"م. محمود حمزة", "courses":"Fundamentals of Programming"},
                    {"name":"م. ميرنا هشام", "courses":"Math 1"},
                    {"name":"م. هاجر غازي", "courses":"Computer Fundamentals"}
                ]
            },
            "2": {
                "schedule": "/static/schedules/schedule-4.png",
                "doctors": [
                    {"name":"د. مروة الصديق", "courses":"Web Development"},
                    {"name":"د. محمد عبده قاسم", "courses":"Software Engineering 1"},
                    {"name":"د. تامر مدحت", "courses":"Creative Thinking"},
                    {"name":"د. بسمة حسن", "courses":"Operating Systems 1"},
                    {"name":"د. فاطمة طلعت", "courses":"Structured Programming"},
                    {"name":"د. زينب حسن", "courses":"Computer Networks; Cyber Security"}
                ],
                "assistants": [
                    {"name":"م. علاء حسين", "courses":"Cyber Security"},
                    {"name":"م. شهد المحمدي", "courses":"Web Development"},
                    {"name":"م. آية مطاوع", "courses":"Operating Systems 1"},
                    {"name":"م. عمر معروف", "courses":"Software Engineering 1"},
                    {"name":"م. أحمد هشام", "courses":"Computer Networks"},
                    {"name":"م. عبدالمولى يوسف", "courses":"Structured Programming"}
                ]
            }
        }
    }
}

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/student")
def student_data():
    program = request.args.get("program", "AI").upper()
    level = request.args.get("level", "1")
    if program not in DATA or level not in DATA[program]["levels"]:
        return jsonify({"error": "اختيار غير صحيح"}), 400
    selected = DATA[program]["levels"][level]
    return jsonify({"program": program, "level": level, "advisor": DATA[program]["advisor"], **selected})

@app.post("/api/chat")
def chatbot():
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip().lower()
    program = (body.get("program") or "AI").upper()
    level = str(body.get("level") or "1")
    if program not in DATA or level not in DATA[program]["levels"]:
        program, level = "AI", "1"
    selected = DATA[program]["levels"][level]
    advisor = DATA[program]["advisor"]
    if any(k in question for k in ["مرشد", "advisor", "ارشاد"]):
        answer = f"المرشد الأكاديمي: {advisor['name']} — المكتب في {advisor['office']}."
    elif any(k in question for k in ["مكتب", "فين", "مكان", "office", "where"]):
        answer = f"مكتب {advisor['name']} في {advisor['office']}."
    elif any(k in question for k in ["جدول", "schedule", "timetable"]):
        answer = "افتح خدمة Class Schedule من لوحة الطالب لعرض صورة الجدول الرسمي للمستوى والبرنامج المختارين."
    elif any(k in question for k in ["دكتور", "دكاترة", "هيئة التدريس", "faculty", "doctor"]):
        answer = "تقدر تشوف قائمة الدكاترة المخصصة لفرقتك من Faculty Members داخل لوحة الطالب."
    elif any(k in question for k in ["معيد", "معيدين", "assistant", "ta"]):
        answer = "تقدر تشوف قائمة المعيدين المخصصة لفرقتك من Faculty Members داخل لوحة الطالب."
    elif any(k in question for k in ["سكشن", "sections", "مجموعة", "group"]):
        answer = "افتح Lectures & Sections ثم اختر رقم مجموعتك من 1 إلى 4. تفاصيل المواعيد يجب مراجعتها من صورة الجدول الرسمي المعروضة."
    elif any(k in question for k in ["محاضرة", "محاضرات", "النهارده", "اليوم", "lecture", "today"]):
        answer = "لعرض المواعيد الصحيحة، افتح Class Schedule أو Lectures & Sections وراجع جدول برنامجك ومستواك. لم أضف مواعيد غير مؤكدة."
    elif any(k in question for k in ["أهلا", "مرحبا", "hello", "hi"]):
        answer = "أهلًا بيك في ARENA! اسأل عن المرشد الأكاديمي أو الجدول أو الدكاترة أو المعيدين."
    else:
        answer = "أنا نسخة تجريبية بإجابات محددة مسبقًا. جرّب سؤالًا عن المرشد الأكاديمي أو مكان مكتبه أو الجدول أو الدكاترة أو المعيدين أو السكاشن."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
