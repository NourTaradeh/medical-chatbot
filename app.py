from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

Patterns = {

    "SymptomCheck": re.compile(
        r"(لدي|عندي|اشعر|اعاني).*(صداع|ألم|حلق|سعال|دوخة)"
        r"|"
        r"(دوخة|سعال|ألم|حلق|صداع)",
        re.I
    ),

    "MedicationAdvice": re.compile(
        r"(ما|شو|هل).*(مسكن|باراسيتامول|العلاج|الدواء).*(مناسب|بزبط)"
        r"|"
        r"(كم).*(جرعة)"
        r"|"
        r"(ما).*(جرعة).*(مناسبة)"
        r"|"
        r"(هل).*(أخذ|تناول).*(باراسيتامول|دواء)",
        re.I
    ),

    "FeverConcern": re.compile(
        r"(حرارتي|درجة حرارتي|عندي حرارة|حمى)"
        r"|"
        r"(38|39|40|37\.5|38\.5).*(حرارة|درجة|خطيرة)"
        r"|"
        r"(هل).*(38|39|40).*(خطيرة)"
        r"|"
        r"(كيف).*(أخفض|أنزل).*(الحرارة)",
        re.I
    ),

    "DoctorVisit": re.compile(
        r"(متى|هل).*(أزور|أحتاج).*(طبيب|فحص)"
        r"|"
        r"(حالتي|وضعي).*(خطير|خطيرة)"
        r"|"
        r"(هل).*(أحتاج).*(فحص)",
        re.I
    ),

    "DiseaseInfo": re.compile(
        r"(ما).*(أعراض|أسباب).*(الإنفلونزا|السكري|الربو)"
        r"|"
        r"(اخبرني عن|احكيلي عن|اشرح لي عن).*(الإنفلونزا|السكري|الربو)",
        re.I
    ),

    "Emergency": re.compile(
        r"(لا استطيع التنفس)"
        r"|"
        r"(ألم شديد).*(الصدر)"
        r"|"
        r"(نزيف).*(حاد|شديد)",
        re.I
    ),

    "Greeting": re.compile(
        r"(مرحبا|اهلا|السلام عليكم|هاي)",
        re.I
    ),
    "Goodbye": re.compile(
        r"(سلام|مع السلامة|باي|يلا سلام|اشوفك|الى اللقاء)",
        re.I
    ),
}

responses = {

    "SymptomCheck":
    "يبدو أنك تعاني من بعض الأعراض. يُنصح بالراحة وشرب السوائل. إذا استمرت الأعراض أو ازدادت شدتها، يُفضل استشارة الطبيب.",

    "MedicationAdvice":
    "يمكن استخدام بعض الأدوية لتخفيف الأعراض مثل المسكنات الشائعة، لكن يجب الالتزام بالجرعة الموصى بها ويفضل استشارة الطبيب أو الصيدلي.",

    "FeverConcern":
    "ارتفاع درجة الحرارة قد يكون بسبب عدوى أو التهاب. حاول الراحة وشرب السوائل واستخدام خافض حرارة عند الحاجة.",

    "DoctorVisit":
    "إذا كانت الأعراض شديدة أو استمرت لعدة أيام، فمن الأفضل زيارة الطبيب للحصول على تشخيص دقيق.",

    "DiseaseInfo":
    "تختلف أعراض وأسباب الأمراض حسب الحالة. من الأفضل قراءة معلومات طبية موثوقة أو استشارة الطبيب.",

    "Emergency":
    "قد تكون هذه حالة طبية طارئة. يُنصح بالتوجه فورًا إلى أقرب مستشفى أو الاتصال بالإسعاف.",

    "Greeting":
    "مرحبًا بك! كيف يمكنني مساعدتك اليوم؟",

    "Unknown":
    "لم أفهم سؤالك الطبي. هل يمكنك إعادة صياغته بطريقة أخرى؟",
    
    "Goodbye": "مع السلامة 👋 أتمنى لك الصحة والعافية!",
}

def detect_intent(user_input):
    for intent, pattern in Patterns.items():
        if pattern.search(user_input):
            return intent
    return "Unknown"

def get_bot_reply(user_input):
    intent = detect_intent(user_input)
    return responses[intent]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    reply = get_bot_reply(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

