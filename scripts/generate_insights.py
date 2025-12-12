#!/usr/bin/env python3
"""
Generate AI insights using OpenRouter free models
Supports Arabic language with multiple free model fallbacks
"""

import json
import os
import sys
from datetime import datetime
import urllib.request
import urllib.error

# Free models from OpenRouter (no cost)
FREE_MODELS = [
    "qwen/qwen-2-7b-instruct:free",  # Best for Arabic
    "google/gemma-2-9b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

def call_openrouter(prompt, api_key, model=None):
    """Call OpenRouter API with free model"""
    if not api_key:
        print("⚠️ No OpenRouter API key provided")
        return None
    
    model = model or FREE_MODELS[0]
    print(f"🤖 Calling {model}...")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/kaledh4/calc',
        'X-Title': 'Smart Finance Calculator'
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            content = result['choices'][0]['message']['content']
            print(f"✅ AI response received ({len(content)} chars)")
            return content
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_insights():
    """Generate SMART & CONCISE AI insights"""
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    
    # Load data
    try:
        with open('data/inflation.json', 'r', encoding='utf-8') as f: inflation = json.load(f)
    except: inflation = {'current': 2.5, 'change': 0.0}
    
    try:
        with open('data/news.json', 'r', encoding='utf-8') as f: 
            news = json.load(f)
            news_headlines = ' | '.join([n['title'] for n in news[:3]]) # Only top 3, concise
    except: news_headlines = "لا توجد أخبار هامة"
    
    # SMART PROMPT - DIRECT & AGGRESSIVE
    prompt = f"""
    أنت محلل مالي خبير ومختصر جداً. لا تستخدم عبارات ترحيبية.
    
    البيانات:
    - التضخم: {inflation['current']}%
    - الأخبار: {news_headlines}
    
    المطلوب (إجابة مباشرة فوراً):
    
    1. 📉 **حقيقة أموالك:**
    احسب بدقة: كم يخسر راتب 10,000 ريال من قوته الشرائية سنوياً بهذا المعدل؟ (أعطني الرقم فقط).
    
    2. 💡 **الإجراء الفوري:**
    بناءً على الأخبار والتضخم، أعطني نصيحة واحدة محددة جداً (شراء/بيع/سداد) اليوم. لا تقل "راقب" أو "وفر"، كن محدداً.
    
    3. 🔮 **نظرة المستقبل:**
    في جملة واحدة: هل نتجه لركود أم انتعاش؟ ولماذا (بكلمتين)؟
    
    4. 🏦 **حكمة القروض:**
    هل الوقت مناسب لأخذ قرض اليوم؟ (نعم/لا) ولماذا حسابياً؟
    """

    # Try to get AI insights
    insights_text = None
    
    if api_key:
        # Use Gemini 2.0 Flash (Fast & Smart) or Llama 3.2 as fallback
        models = ["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.2-3b-instruct:free"]
        for model in models:
            insights_text = call_openrouter(prompt, api_key, model)
            if insights_text: break
    
    # Fallback if no API key or failure
    if not insights_text:
        loss = 10000 * (inflation['current'] / 100)
        insights_text = f"""
        1. 📉 **حقيقة أموالك:** راتب 10,000 يخسر {loss:.0f} ريال سنوياً من قيمته الحقيقية.
        2. 💡 **الإجراء الفوري:** فعّل مفتاح AI للحصول على نصيحة ذكية مخصصة.
        3. 🔮 **نظرة المستقبل:** التضخم {inflation['current']}% يتطلب حماية مدخراتك بأصول حقيقية.
        4. 🏦 **حكمة القروض:** الفائدة الحقيقية = الفائدة الاسمية - {inflation['current']}%. احسبها جيداً.
        """

    # Create insights object
    insights = {
        'summary': insights_text,
        'timestamp': datetime.utcnow().isoformat(),
        'model': 'Smart-AI',
        'language': 'ar'
    }
    
    # Save insights
    os.makedirs('data', exist_ok=True)
    with open('data/insights.json', 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Smart Insights Generated")
    return insights

if __name__ == '__main__':
    generate_insights()
