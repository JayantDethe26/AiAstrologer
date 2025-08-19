import os
import random
import time
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ---------------- Gemini Setup ----------------
API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Optimized generation config for consistent quality
generation_config = genai.types.GenerationConfig(
    temperature=0.9,        # Balanced creativity
    top_p=0.85,            # Good diversity without chaos
    top_k=35,              # Focused token selection
    max_output_tokens=450, # Comprehensive but not overwhelming
    candidate_count=1      
)

# Simplified but effective randomization elements
READING_APPROACHES = [
    "intuitive and insightful", "practical and grounding", "transformational and empowering",
    "nurturing and supportive", "direct and clarifying", "mystical and deep",
    "energizing and motivational", "healing and restorative"
]

COSMIC_INFLUENCES = [
    "current planetary transits", "lunar cycle energies", "seasonal cosmic shifts",
    "mercury communication patterns", "venus love vibrations", "mars action energies",
    "jupiter expansion cycles", "saturn wisdom lessons"
]

# Focused system prompts for better astrology readings
ASTROLOGY_PROMPTS = [
    # Prompt 1 - Personal Growth Focus
    """You are an expert astrologer providing personalized guidance based on birth chart analysis.

    Your task: Create a unique, insightful astrology reading that addresses the user's specific question while incorporating their birth details.

    STRUCTURE YOUR RESPONSE (250-350 words):
    1. PERSONAL GREETING: Address them by name with their zodiac sign significance
    2. BIRTH CHART INSIGHTS: Connect their birth details to relevant astrological patterns
    3. QUESTION ANALYSIS: Directly address their specific question using astrological wisdom
    4. PRACTICAL GUIDANCE: Provide actionable advice based on current cosmic energies
    5. TIMING & MANIFESTATION: Suggest optimal periods for action based on their chart

    REQUIREMENTS:
    - Write in a warm, professional tone
    - Include specific astrological concepts (houses, aspects, transits)
    - Provide both spiritual insights and practical advice
    - Make it personal to their birth information
    - Address their question comprehensively""",

    # Prompt 2 - Relationship & Career Focus  
    """You are a skilled astrologer specializing in life path guidance through cosmic wisdom.

    Create a detailed reading that combines traditional astrology with practical life advice for their specific situation.

    READING FORMAT (280-380 words):
    → COSMIC IDENTITY: How their birth chart shapes their core nature
    → CURRENT INFLUENCES: What planetary energies are affecting them now
    → QUESTION GUIDANCE: Specific astrological insights about their inquiry
    → STRENGTHS TO LEVERAGE: Natural talents shown in their birth chart
    → RECOMMENDED ACTIONS: Steps aligned with favorable cosmic timing

    FOCUS AREAS:
    - Use their zodiac sign characteristics meaningfully
    - Reference their birth time and location when relevant
    - Provide hope and empowerment
    - Include warnings about challenges with solutions
    - Give specific timeframes for important actions""",

    # Prompt 3 - Spiritual & Healing Focus
    """You are a compassionate astrologer focused on healing and spiritual growth through celestial guidance.

    Provide a nurturing yet insightful reading that helps them understand their life path and current challenges.

    HEALING STRUCTURE (260-360 words):
    ★ SOUL PURPOSE: What their birth chart reveals about their life mission
    ★ CURRENT LESSONS: How cosmic energies relate to their question/challenge
    ★ HEALING PATH: Astrological guidance for overcoming obstacles
    ★ HIDDEN GIFTS: Untapped potentials in their birth chart
    ★ DIVINE TIMING: When cosmic support is strongest for their goals

    APPROACH:
    - Acknowledge their courage in seeking guidance
    - Connect emotional patterns to astrological influences  
    - Provide gentle but powerful transformational insights
    - Include specific healing practices aligned with their sign
    - End with an empowering affirmation based on their chart""",

    # Prompt 4 - Success & Manifestation Focus
    """You are a strategic astrologer helping clients align with cosmic success patterns.

    Create an empowering reading that shows them how to work with universal energies for their highest good.

    SUCCESS BLUEPRINT (270-370 words):
    ◆ COSMIC ADVANTAGES: Their birth chart's natural success indicators
    ◆ CURRENT OPPORTUNITIES: How present planetary aspects support their goal
    ◆ STRATEGIC TIMING: Best periods for important decisions/actions
    ◆ CHALLENGE NAVIGATION: How to overcome obstacles using astrological wisdom
    ◆ MANIFESTATION ALLIES: Which cosmic energies to work with

    EMPOWERMENT FOCUS:
    - Frame challenges as growth opportunities
    - Highlight their astrological superpowers
    - Provide specific dates/periods for taking action
    - Connect their question to larger life patterns
    - Inspire confidence in their cosmic support system"""
]

def get_zodiac_sign(day, month):
    """Calculate zodiac sign from birth date"""
    zodiac_dates = [
        (120, "Capricorn ♑"), (219, "Aquarius ♒"), (320, "Pisces ♓"), 
        (420, "Aries ♈"), (521, "Taurus ♉"), (621, "Gemini ♊"), 
        (722, "Cancer ♋"), (822, "Leo ♌"), (922, "Virgo ♍"), 
        (1022, "Libra ♎"), (1121, "Scorpio ♏"), (1221, "Sagittarius ♐"),
        (1231, "Capricorn ♑")
    ]
    date_key = month * 100 + day
    for cutoff_date, sign in zodiac_dates:
        if date_key <= cutoff_date:
            return sign
    return "Capricorn ♑"

def get_life_stage(birth_date):
    """Determine astrological life stage for more relevant readings"""
    current_date = datetime.now()
    age = current_date.year - birth_date.year
    
    if age < 14:
        return "childhood development phase"
    elif age < 29:
        return "first Saturn return approach - foundational years"
    elif age < 43:
        return "Uranus opposition phase - transformation time"
    elif age < 58:
        return "second Saturn return - mastery period"
    else:
        return "wisdom harvest years"

def create_personalized_context(name, dob, question, zodiac_sign):
    """Create meaningful context for personalized readings"""
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    current_time = datetime.now()
    
    # Life stage context
    life_stage = get_life_stage(birth_date)
    
    # Question category analysis
    question_lower = question.lower()
    if any(word in question_lower for word in ['love', 'relationship', 'partner', 'marriage', 'dating']):
        focus_area = "heart and relationship matters"
        cosmic_guidance = "Venus and 7th house influences"
    elif any(word in question_lower for word in ['career', 'job', 'work', 'business', 'money', 'finance']):
        focus_area = "career and material success"
        cosmic_guidance = "10th house and Saturn teachings"
    elif any(word in question_lower for word in ['health', 'healing', 'wellness', 'body', 'energy']):
        focus_area = "health and vitality"
        cosmic_guidance = "6th house and Mars energy"
    elif any(word in question_lower for word in ['family', 'home', 'parents', 'children']):
        focus_area = "family and home foundations"
        cosmic_guidance = "4th house and Moon cycles"
    elif any(word in question_lower for word in ['spiritual', 'purpose', 'meaning', 'growth']):
        focus_area = "spiritual evolution and life purpose"
        cosmic_guidance = "12th house and Jupiter expansion"
    else:
        focus_area = "general life guidance"
        cosmic_guidance = "overall birth chart harmony"
    
    # Seasonal context
    season = ["Winter", "Spring", "Summer", "Autumn"][current_time.month // 3]
    
    # Current cosmic influence
    cosmic_influence = random.choice(COSMIC_INFLUENCES)
    reading_style = random.choice(READING_APPROACHES)
    
    return {
        "life_stage": life_stage,
        "focus_area": focus_area,
        "cosmic_guidance": cosmic_guidance,
        "season": season,
        "cosmic_influence": cosmic_influence,
        "reading_style": reading_style,
        "birth_month": birth_date.strftime("%B"),
        "birth_season": ["Winter", "Spring", "Summer", "Autumn"][birth_date.month // 3]
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Get form data
        name = request.form['name'].strip()
        dob = request.form['dob']
        tob = request.form['tob']
        pob = request.form['pob'].strip()
        question = request.form['question'].strip()

        if not all([name, dob, tob, pob, question]):
            raise ValueError("All fields are required")

        # Calculate zodiac and get context
        dob_obj = datetime.strptime(dob, "%Y-%m-%d")
        zodiac = get_zodiac_sign(dob_obj.day, dob_obj.month)
        context = create_personalized_context(name, dob, question, zodiac)

        # Select random system prompt for variety
        system_prompt = random.choice(ASTROLOGY_PROMPTS)
        
        # Create comprehensive user prompt
        user_prompt = f"""
ASTROLOGY READING REQUEST

CLIENT DETAILS:
- Name: {name}
- Birth Date: {dob_obj.strftime('%B %d, %Y')} ({context['birth_season']} birth)
- Birth Time: {tob}
- Birth Place: {pob}
- Zodiac Sign: {zodiac}
- Life Stage: {context['life_stage']}

SPECIFIC QUESTION: "{question}"

READING CONTEXT:
- Focus Area: {context['focus_area']}
- Astrological Focus: {context['cosmic_guidance']}
- Current Season: {context['season']} energies
- Cosmic Influence: {context['cosmic_influence']}
- Reading Approach: {context['reading_style']}

INSTRUCTIONS:
Create a personalized astrology reading that directly addresses {name}'s question about {context['focus_area']}. Use their {zodiac} nature and {context['life_stage']} to provide meaningful insights. Include practical guidance they can apply in their daily life.

Make this reading feel like it was written specifically for {name} - no generic astrology content. Address their question with depth and provide actionable wisdom."""

        # Generate reading
        response = model.generate_content(
            f"{system_prompt}\n\n{user_prompt}",
            generation_config=generation_config
        )
        
        ai_answer = response.text if response.text else generate_fallback_reading(name, zodiac, question)
        
        # Return JSON response
        return jsonify({
            'success': True,
            'name': name,
            'dob': dob,
            'tob': tob,
            'pob': pob,
            'zodiac': zodiac,
            'question': question,
            'ai_answer': ai_answer,
            'reading_context': context
        })

    except Exception as e:
        print(f"Error generating reading: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback_reading': generate_fallback_reading(
                request.form.get('name', 'Seeker'),
                'Universal ✨',
                request.form.get('question', 'guidance')
            )
        }), 500

@app.route('/api/reading', methods=['POST'])
def api_reading():
    """Clean API endpoint for generating readings"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'name': request.form['name'].strip(),
                'dob': request.form['dob'],
                'tob': request.form['tob'], 
                'pob': request.form['pob'].strip(),
                'question': request.form['question'].strip()
            }
        
        # Validate required fields
        required_fields = ['name', 'dob', 'tob', 'pob', 'question']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Process the reading request
        dob_obj = datetime.strptime(data['dob'], "%Y-%m-%d")
        zodiac = get_zodiac_sign(dob_obj.day, dob_obj.month)
        context = create_personalized_context(data['name'], data['dob'], data['question'], zodiac)
        
        # Generate reading with random prompt selection
        system_prompt = random.choice(ASTROLOGY_PROMPTS)
        
        user_prompt = f"""
PERSONALIZED ASTROLOGY READING

CLIENT: {data['name']}
BIRTH: {dob_obj.strftime('%B %d, %Y')} at {data['tob']} in {data['pob']}
SIGN: {zodiac} 
LIFE PHASE: {context['life_stage']}

QUESTION: "{data['question']}"

FOCUS: {context['focus_area']} using {context['cosmic_guidance']}
APPROACH: {context['reading_style']} with {context['cosmic_influence']}

Create a meaningful astrology reading that:
1. Addresses their specific question directly
2. Uses their birth details meaningfully
3. Provides both spiritual insight and practical advice  
4. Feels personal and unique to their situation
5. Offers hope and empowerment

Write as if you're their personal astrologer who knows their chart intimately."""

        # Generate the reading
        response = model.generate_content(
            f"{system_prompt}\n\n{user_prompt}",
            generation_config=generation_config
        )
        
        ai_answer = response.text if response.text else generate_fallback_reading(
            data['name'], zodiac, data['question']
        )
        
        return jsonify({
            'success': True,
            'reading': {
                'name': data['name'],
                'birth_date': dob_obj.strftime('%B %d, %Y'),
                'birth_time': data['tob'],
                'birth_place': data['pob'],
                'zodiac_sign': zodiac,
                'question': data['question'],
                'cosmic_guidance': ai_answer,
                'reading_timestamp': datetime.now().isoformat(),
                'life_stage': context['life_stage'],
                'focus_area': context['focus_area']
            }
        })
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': f'Invalid date format: {str(ve)}'
        }), 400
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to generate reading at this time',
            'details': str(e) if app.debug else None
        }), 500

def generate_fallback_reading(name, zodiac, question):
    """Generate a quality fallback reading when AI fails"""
    
    zodiac_insights = {
        "Aries ♈": "Your fiery Aries energy brings natural leadership and courage to face any challenge.",
        "Taurus ♉": "Your steady Taurus nature provides the persistence needed to manifest your desires.",
        "Gemini ♊": "Your curious Gemini spirit opens multiple pathways to explore your question.",
        "Cancer ♋": "Your intuitive Cancer nature guides you toward emotionally fulfilling solutions.",
        "Leo ♌": "Your confident Leo energy illuminates creative approaches to your situation.",
        "Virgo ♍": "Your analytical Virgo mind can break down complex situations into manageable steps.",
        "Libra ♎": "Your diplomatic Libra nature seeks harmony and balanced solutions.",
        "Scorpio ♏": "Your transformative Scorpio power helps you dive deep and emerge renewed.",
        "Sagittarius ♐": "Your adventurous Sagittarius spirit sees the bigger picture and future possibilities.",
        "Capricorn ♑": "Your ambitious Capricorn energy builds lasting foundations for success.",
        "Aquarius ♒": "Your innovative Aquarius mind brings fresh perspectives to old problems.",
        "Pisces ♓": "Your compassionate Pisces intuition connects you to deeper universal wisdom."
    }
    
    general_guidance = [
        "The stars suggest this is a time of important growth and learning for you.",
        "Current planetary energies support taking thoughtful action toward your goals.",
        "Your birth chart indicates strong potential for positive transformation in this area.",
        "The cosmic timing favors trust in your inner wisdom and natural abilities."
    ]
    
    sign_insight = zodiac_insights.get(zodiac, "Your unique cosmic signature holds the key to your question.")
    cosmic_guidance = random.choice(general_guidance)
    
    return f"""Dear {name},

{sign_insight} Regarding your question about {question[:50]}{'...' if len(question) > 50 else ''}, the cosmic energies offer this guidance:

{cosmic_guidance} Your {zodiac} nature possesses exactly the qualities needed to navigate this situation successfully. Trust in the timing of your life's unfolding.

The universe is supporting your highest good during this period. Pay attention to synchronicities and trust your intuition as you move forward. Remember that every challenge contains the seeds of opportunity, and your birth chart shows you have the strength to transform any obstacle into growth.

This is a powerful time for manifestation and positive change. Stay open to unexpected solutions and trust that you are being guided toward your highest path.

✨ The stars are aligned in your favor, {name}. Move forward with confidence. ✨"""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)