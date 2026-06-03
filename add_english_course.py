import os
import django
from django.utils.text import slugify
from django.core.files.base import ContentFile
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import (
    ProgrammingLanguage, LearningPath, Lesson, Challenge, 
    Quiz, QuizQuestion, QuizChoice, Badge
)

print("=" * 60)
print("🎯 ADDING SPOKEN ENGLISH COURSE")
print("=" * 60)

# Get or create English language
english_lang, _ = ProgrammingLanguage.objects.get_or_create(
    name="English",
    slug="english",
    defaults={
        "description": "Master spoken English for daily conversations, interviews, and professional communication",
        "version": "1.0",
        "is_active": True
    }
)

# Create the English course
english_course, course_created = LearningPath.objects.get_or_create(
    slug="spoken-english-mastery",
    defaults={
        "title": "🎙️ Spoken English Mastery: From Beginner to Confident Speaker",
        "description": """
        <h2>🌟 Welcome to Your English Speaking Journey!</h2>
        <p>This comprehensive course is designed to help you speak English with confidence. Whether you're a complete beginner or looking to improve your fluency, this course has everything you need.</p>
        
        <h3>📚 What You'll Learn:</h3>
        <ul>
            <li>🎯 Basic greetings and introductions</li>
            <li>💬 Everyday conversations (shopping, dining, travel)</li>
            <li>📞 Professional and business English</li>
            <li>🗣️ Pronunciation and accent training</li>
            <li>🎭 Idioms and phrasal verbs</li>
            <li>📝 Grammar for speaking (not writing!)</li>
            <li>🎙️ Public speaking and presentation skills</li>
        </ul>
        
        <h3>🎁 Course Includes:</h3>
        <ul>
            <li>🔊 Audio lessons for pronunciation practice</li>
            <li>💻 Interactive speaking challenges</li>
            <li>📝 Quizzes to test your progress</li>
            <li>🏆 Badges for achievements</li>
            <li>🎯 Real-life conversation scenarios</li>
        </ul>
        """,
        "language": english_lang,
        "difficulty": "BEGINNER",
        "estimated_hours": 60,
        "is_active": True
    }
)

print(f"Course created: {english_course.title}")

# ============================================
# CREATE LESSONS
# ============================================
print("\n📚 Creating lessons...")

lessons_data = [
    # Level 1: Beginner
    {
        "title": "Lesson 1: Basic Greetings & Introductions",
        "slug": "basic-greetings",
        "order": 1,
        "xp_reward": 50,
        "theory_content": """
        <h2>👋 Basic Greetings & Introductions</h2>
        
        <div class="audio-section">
            <h3>🔊 Listen and Repeat:</h3>
            <audio controls src="/static/audio/greetings.mp3">Your browser does not support audio</audio>
        </div>
        
        <h3>📖 Common Greetings:</h3>
        <ul>
            <li><strong>Hello!</strong> - General greeting</li>
            <li><strong>Hi!</strong> - Informal greeting</li>
            <li><strong>Good morning!</strong> - Before noon</li>
            <li><strong>Good afternoon!</strong> - 12 PM - 6 PM</li>
            <li><strong>Good evening!</strong> - After 6 PM</li>
            <li><strong>Hey!</strong> - Very informal</li>
        </ul>
        
        <h3>💬 Introductions:</h3>
        <ul>
            <li><strong>"My name is [Name]"</strong></li>
            <li><strong>"I'm [Name]"</strong></li>
            <li><strong>"Nice to meet you!"</strong></li>
            <li><strong>"Pleased to meet you!"</strong></li>
        </ul>
        
        <h3>🗣️ Practice Dialogue:</h3>
        <div class="dialogue">
            <p><strong>A:</strong> Hello! My name is Sarah. What's your name?</p>
            <p><strong>B:</strong> Hi Sarah! I'm John. Nice to meet you!</p>
            <p><strong>A:</strong> Nice to meet you too, John! Where are you from?</p>
            <p><strong>B:</strong> I'm from New York. And you?</p>
            <p><strong>A:</strong> I'm from London. Welcome to the course!</p>
        </div>
        
        <h3>🎯 Your Turn:</h3>
        <p>Practice introducing yourself to a partner or record yourself!</p>
        """,
        "example_code": """# Speaking Practice
greetings = ["Hello!", "Hi!", "Good morning!"]
introductions = [
    "My name is [your name]",
    "I'm from [your city]",
    "Nice to meet you!"
]

# Practice saying these out loud:
for greeting in greetings:
    print(f"Say: {greeting}")
    print(f"Then say: {introductions[0]}")
    print(f"Then say: {introductions[1]}")
    print("---")"""
    },
    {
        "title": "Lesson 2: Everyday Conversations - Shopping & Dining",
        "slug": "shopping-dining",
        "order": 2,
        "xp_reward": 60,
        "theory_content": """
        <h2>🛍️ Shopping & Dining Conversations</h2>
        
        <h3>🛒 At a Store:</h3>
        <ul>
            <li><strong>"How much does this cost?"</strong></li>
            <li><strong>"I'm just browsing, thanks."</strong></li>
            <li><strong>"Do you have this in a different size/color?"</strong></li>
            <li><strong>"Where is the fitting room?"</strong></li>
            <li><strong>"I'd like to return this, please."</strong></li>
        </ul>
        
        <h3>🍽️ At a Restaurant:</h3>
        <ul>
            <li><strong>"Table for two, please."</strong></li>
            <li><strong>"Can I see the menu?"</strong></li>
            <li><strong>"What do you recommend?"</strong></li>
            <li><strong>"I'm vegetarian/vegan/allergic to nuts."</strong></li>
            <li><strong>"Could I have the bill/check, please?"</strong></li>
        </ul>
        
        <h3>💬 Practice Dialogue - Restaurant:</h3>
        <div class="dialogue">
            <p><strong>Waiter:</strong> Welcome! Table for two?</p>
            <p><strong>You:</strong> Yes, please. By the window if possible.</p>
            <p><strong>Waiter:</strong> Of course. Here are your menus.</p>
            <p><strong>You:</strong> Thank you! What's today's special?</p>
            <p><strong>Waiter:</strong> The grilled salmon is excellent.</p>
            <p><strong>You:</strong> Sounds great! I'll have that.</p>
        </div>
        """,
        "example_code": """# Shopping Phrases Practice
phrases = {
    "greeting": "Hello, how can I help you?",
    "browsing": "I'm just looking, thanks.",
    "price": "How much does this cost?",
    "payment": "I'll take it. Do you accept credit cards?"
}

# Role play scenario
customer = "I'm looking for a gift."
salesperson = "What occasion is it for?"
customer = "It's for my friend's birthday."

print("Practice this conversation with a partner!")"""
    },
    {
        "title": "Lesson 3: Travel & Transportation English",
        "slug": "travel-english",
        "order": 3,
        "xp_reward": 70,
        "theory_content": """
        <h2>✈️ Travel & Transportation English</h2>
        
        <h3>🚗 At the Airport:</h3>
        <ul>
            <li><strong>"Where is the check-in counter?"</strong></li>
            <li><strong>"I have a connecting flight."</strong></li>
            <li><strong>"What is the gate number?"</strong></li>
            <li><strong>"Is my flight on time?"</strong></li>
            <li><strong>"I'd like a window/aisle seat."</strong></li>
        </ul>
        
        <h3>🚕 Getting Around:</h3>
        <ul>
            <li><strong>"How do I get to [place]?"</strong></li>
            <li><strong>"Is it walking distance?"</strong></li>
            <li><strong>"Which bus/train goes to [place]?"</strong></li>
            <li><strong>"How much is a taxi to [place]?"</strong></li>
        </ul>
        
        <h3>🏨 At the Hotel:</h3>
        <ul>
            <li><strong>"I have a reservation."</strong></li>
            <li><strong>"Could I have a wake-up call at 7 AM?"</strong></li>
            <li><strong>"Is breakfast included?"</strong></li>
            <li><strong>"Could I have extra towels, please?"</strong></li>
        </ul>
        """,
        "example_code": """# Travel Conversation Template
class TravelPhrases:
    def __init__(self, destination):
        self.destination = destination
    
    def ask_directions(self):
        return f"Excuse me, how do I get to {self.destination}?"
    
    def book_ticket(self):
        return f"I'd like a ticket to {self.destination}, please."

# Practice saying these aloud!
traveler = TravelPhrases("the city center")
print(traveler.ask_directions())
print(traveler.book_ticket())"""
    },
    {
        "title": "Lesson 4: Professional & Business English",
        "slug": "business-english",
        "order": 4,
        "xp_reward": 80,
        "theory_content": """
        <h2>💼 Professional & Business English</h2>
        
        <h3>📞 Phone Calls & Meetings:</h3>
        <ul>
            <li><strong>"May I speak with [Name], please?"</strong></li>
            <li><strong>"I'm calling about..."</strong></li>
            <li><strong>"Could you please repeat that?"</strong></li>
            <li><strong>"I'll get back to you by [date]."</strong></li>
        </ul>
        
        <h3>✍️ Email Writing:</h3>
        <ul>
            <li><strong>Subject: [Clear topic]</strong></li>
            <li><strong>Dear [Name],</strong></li>
            <li><strong>I hope this email finds you well.</strong></li>
            <li><strong>Looking forward to your reply.</strong></li>
            <li><strong>Best regards, [Your Name]</strong></li>
        </ul>
        
        <h3>🎯 Common Workplace Phrases:</h3>
        <ul>
            <li><strong>"Let's touch base later."</strong> - Let's talk later</li>
            <li><strong>"I'm swamped."</strong> - I'm very busy</li>
            <li><strong>"Think outside the box."</strong> - Be creative</li>
            <li><strong>"Get the ball rolling."</strong> - Start something</li>
        </ul>
        """,
        "example_code": """# Business Email Template
def create_email(recipient, subject, message):
    email = f'''
    Subject: {subject}
    
    Dear {recipient},
    
    I hope this email finds you well.
    
    {message}
    
    Looking forward to your response.
    
    Best regards,
    [Your Name]
    '''
    return email

# Example usage
print(create_email("Ms. Johnson", "Meeting Request", 
                   "Could we schedule a meeting for next Tuesday?"))"""
    },
    {
        "title": "Lesson 5: Pronunciation & Accent Training",
        "slug": "pronunciation",
        "order": 5,
        "xp_reward": 90,
        "theory_content": """
        <h2>🗣️ Pronunciation & Accent Training</h2>
        
        <h3>🔊 Vowel Sounds:</h3>
        <ul>
            <li><strong>Short vowels:</strong> cat /æ/, bed /ɛ/, sit /ɪ/, hot /ɑ/, up /ʌ/</li>
            <li><strong>Long vowels:</strong> see /iː/, go /oʊ/, blue /uː/, law /ɔː/</li>
        </ul>
        
        <h3>🎯 Common Pronunciation Mistakes:</h3>
        <ul>
            <li><strong>TH sound:</strong> "think" (not "sink"), "that" (not "zat")</li>
            <li><strong>R vs L:</strong> "right" vs "light", "road" vs "load"</li>
            <li><strong>Word stress:</strong> REcord (noun) vs reCORD (verb)</li>
        </ul>
        
        <h3>🗣️ Tongue Twisters for Practice:</h3>
        <div class="tongue-twister">
            <p>🎤 "She sells seashells by the seashore."</p>
            <p>🎤 "How much wood would a woodchuck chuck?"</p>
            <p>🎤 "Peter Piper picked a peck of pickled peppers."</p>
        </div>
        
        <h3>📱 Practice Tips:</h3>
        <ul>
            <li>Record yourself speaking and compare</li>
            <li>Watch English videos with subtitles</li>
            <li>Use pronunciation apps like ELSA Speak</li>
        </ul>
        """,
        "example_code": """# Pronunciation Practice Tracker
pronunciation_pairs = [
    ("ship", "sheep"),
    ("live", "leave"),
    ("full", "fool"),
    ("walk", "work"),
    ("world", "word")
]

print("Practice saying these minimal pairs:")
for word1, word2 in pronunciation_pairs:
    print(f"  {word1} vs {word2}")
    print(f"   Say: {word1} - {word2} (repeat 3 times)")"""
    },
    {
        "title": "Lesson 6: Idioms & Phrasal Verbs",
        "slug": "idioms-phrasal-verbs",
        "order": 6,
        "xp_reward": 100,
        "theory_content": """
        <h2>🎭 Common Idioms & Phrasal Verbs</h2>
        
        <h3>🌟 Popular Idioms:</h3>
        <ul>
            <li><strong>"Break a leg!"</strong> - Good luck!</li>
            <li><strong>"It's raining cats and dogs."</strong> - Raining heavily</li>
            <li><strong>"Piece of cake."</strong> - Very easy</li>
            <li><strong>"Cost an arm and a leg."</strong> - Very expensive</li>
            <li><strong>"Hit the nail on the head."</strong> - Exactly right</li>
        </ul>
        
        <h3>📚 Essential Phrasal Verbs:</h3>
        <ul>
            <li><strong>"Give up"</strong> - Stop trying</li>
            <li><strong>"Look forward to"</strong> - Be excited about</li>
            <li><strong>"Run out of"</strong> - Have no more</li>
            <li><strong>"Take care of"</strong> - Handle/manage</li>
            <li><strong>"Get along with"</strong> - Have a good relationship</li>
        </ul>
        
        <h3>💬 Example Sentences:</h3>
        <div class="examples">
            <p>"Don't <strong>give up</strong> on your English goals!"</p>
            <p>"I <strong>look forward to</strong> our next class."</p>
            <p>"We <strong>ran out of</strong> time."</p>
            <p>"Can you <strong>take care of</strong> this for me?"</p>
        </div>
        """,
        "example_code": """# Idiom Practice Game
import random

idioms = {
    "break a leg": "Wishing someone good luck",
    "piece of cake": "Something very easy",
    "cost an arm and a leg": "Very expensive",
    "hit the nail on the head": "Exactly correct"
}

print("🎮 Idiom Quiz Game")
print("Match the idiom to its meaning:\n")
for idiom, meaning in idioms.items():
    print(f"Idiom: {idiom}")
    print(f"Meaning: {meaning}")
    print("---")
    print("Try using this idiom in a sentence of your own!\n")"""
    }
]

# Create lessons
for lesson_data in lessons_data:
    lesson, created = Lesson.objects.get_or_create(
        slug=lesson_data["slug"],
        learning_path=english_course,
        defaults={
            "title": lesson_data["title"],
            "theory_content": lesson_data["theory_content"],
            "example_code": lesson_data["example_code"],
            "order": lesson_data["order"],
            "xp_reward": lesson_data["xp_reward"],
            "is_locked": False
        }
    )
    if created:
        print(f"  ✅ Created lesson: {lesson.title}")
    else:
        print(f"  ⏭️ Lesson exists: {lesson.title}")

# ============================================
# CREATE CHALLENGES
# ============================================
print("\n💻 Creating speaking challenges...")

challenges_data = [
    {
        "title": "🎤 Introduce Yourself Challenge",
        "slug": "introduce-yourself",
        "problem_statement": """
        <h2>🎯 Challenge: Record Yourself Introducing</h2>
        <p>Record a 30-second video or audio introducing yourself in English. Include:</p>
        <ul>
            <li>Your name</li>
            <li>Where you're from</li>
            <li>Why you're learning English</li>
            <li>One interesting fact about yourself</li>
        </ul>
        <p>Practice until you feel confident and natural!</p>
        """,
        "difficulty": "EASY",
        "xp_reward": 100
    },
    {
        "title": "📞 Ordering Food Roleplay",
        "slug": "ordering-food",
        "problem_statement": """
        <h2>🍕 Challenge: Order Food Over Phone</h2>
        <p>Roleplay ordering food from a restaurant. Practice:</p>
        <ul>
            <li>Greeting the person</li>
            <li>Ordering your food items</li>
            <li>Asking about specials or recommendations</li>
            <li>Confirming the total and delivery address</li>
            <li>Saying thank you and goodbye</li>
        </ul>
        <p>Find a partner or record yourself doing both roles!</p>
        """,
        "difficulty": "MEDIUM",
        "xp_reward": 150
    },
    {
        "title": "✈️ Travel Scenario",
        "slug": "travel-scenario",
        "problem_statement": """
        <h2>🧳 Challenge: Hotel Check-in Conversation</h2>
        <p>Act out a hotel check-in conversation. Include:</p>
        <ul>
            <li>Greeting the receptionist</li>
            <li>Confirming your reservation</li>
            <li>Asking about amenities (pool, gym, breakfast)</li>
            <li>Requesting a wake-up call</li>
            <li>Asking for local recommendations</li>
        </ul>
        """,
        "difficulty": "MEDIUM",
        "xp_reward": 150
    },
    {
        "title": "💼 Business Meeting Roleplay",
        "slug": "business-meeting",
        "problem_statement": """
        <h2>📊 Challenge: Virtual Team Meeting</h2>
        <p>Participate in a mock team meeting. Practice:</p>
        <ul>
            <li>Giving updates on your project</li>
            <li>Asking clarifying questions</li>
            <li>Agreeing/disagreeing politely</li>
            <li>Suggesting new ideas</li>
            <li>Closing the meeting professionally</li>
        </ul>
        """,
        "difficulty": "HARD",
        "xp_reward": 200
    },
    {
        "title": "🎭 Tell a Story Challenge",
        "slug": "tell-story",
        "problem_statement": """
        <h2>📖 Challenge: Tell a 1-Minute Story</h2>
        <p>Tell a short story about any topic (1 minute). Focus on:</p>
        <ul>
            <li>Clear pronunciation</li>
            <li>Natural pace (not too fast/slow)</li>
            <li>Using at least 2 idioms from Lesson 6</li>
            <li>Using past tense correctly</li>
            <li>Keeping the listener engaged</li>
        </ul>
        <p>Suggested topics: A memorable vacation, your first job, a funny experience</p>
        """,
        "difficulty": "HARD",
        "xp_reward": 250
    }
]

# Get first lesson for challenges
first_lesson = english_course.lessons.first()

for challenge_data in challenges_data:
    challenge, created = Challenge.objects.get_or_create(
        slug=challenge_data["slug"],
        defaults={
            "title": challenge_data["title"],
            "problem_statement": challenge_data["problem_statement"],
            "language": english_lang,
            "lesson": first_lesson,
            "difficulty": challenge_data["difficulty"],
            "xp_reward": challenge_data["xp_reward"],
            "is_active": True
        }
    )
    if created:
        print(f"  ✅ Created challenge: {challenge.title}")

# ============================================
# CREATE QUIZZES
# ============================================
print("\n📝 Creating quizzes...")

quizzes_data = [
    {
        "title": "Greetings & Introductions Quiz",
        "questions": [
            {"text": "What is the best way to greet someone in the morning?", 
             "choices": ["Good morning!", "Good night!", "Good afternoon!", "Hello!"], 
             "correct": 0},
            {"text": "Which phrase means you're happy to meet someone?", 
             "choices": ["Nice to meet you!", "Goodbye!", "See you later!", "Take care!"], 
             "correct": 0},
            {"text": "What should you say when you meet someone for the first time?", 
             "choices": ["My name is...", "Where's the bathroom?", "I'm hungry", "What time is it?"], 
             "correct": 0},
        ]
    },
    {
        "title": "Shopping & Dining Quiz",
        "questions": [
            {"text": "How do you ask for the price of an item?", 
             "choices": ["How much does this cost?", "Where is this?", "What is this?", "When is this?"], 
             "correct": 0},
            {"text": "What do you say at a restaurant to get the bill?", 
             "choices": ["Can I have the check please?", "I want free food", "Where's my food?", "I'm done"], 
             "correct": 0},
        ]
    },
    {
        "title": "Idioms Quiz",
        "questions": [
            {"text": "What does 'piece of cake' mean?", 
             "choices": ["Very easy", "Very hard", "A dessert", "Expensive"], 
             "correct": 0},
            {"text": "What does 'break a leg' mean?", 
             "choices": ["Good luck!", "Bad luck!", "Stop!", "Hurry up!"], 
             "correct": 0},
        ]
    }
]

for quiz_data in quizzes_data:
    quiz, created = Quiz.objects.get_or_create(
        title=quiz_data["title"],
        lesson=first_lesson,
        defaults={
            "passing_score": 70,
            "xp_reward": 50,
            "is_active": True
        }
    )
    if created:
        for i, q_data in enumerate(quiz_data["questions"]):
            question = QuizQuestion.objects.create(
                quiz=quiz,
                question_text=q_data["text"],
                order=i + 1
            )
            for j, choice_text in enumerate(q_data["choices"]):
                QuizChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=(j == q_data["correct"])
                )
        print(f"  ✅ Created quiz: {quiz.title}")

# ============================================
# CREATE BADGES
# ============================================
print("\n🏅 Creating speaking badges...")

badges_data = [
    {"name": "🗣️ First Words", "description": "Completed your first English lesson!", "xp": 50},
    {"name": "🎤 Confident Speaker", "description": "Completed 3 speaking challenges", "xp": 200},
    {"name": "🌍 English Explorer", "description": "Mastered greetings, shopping, and travel topics", "xp": 500},
    {"name": "💼 Business Pro", "description": "Completed business English module", "xp": 800},
    {"name": "🏆 Fluent Speaker", "description": "Completed the entire English course!", "xp": 1000},
]

for badge_data in badges_data:
    badge, created = Badge.objects.get_or_create(
        name=badge_data["name"],
        defaults={
            "description": badge_data["description"],
            "xp_required": badge_data["xp"]
        }
    )
    if created:
        print(f"  ✅ Created badge: {badge.name}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("✅ SPOKEN ENGLISH COURSE ADDED SUCCESSFULLY!")
print("=" * 60)
print(f"📚 Course: {english_course.title}")
print(f"📖 Lessons: {english_course.lessons.count()}")
print(f"💻 Challenges: {Challenge.objects.filter(lesson__learning_path=english_course).count()}")
print(f"📝 Quizzes: {Quiz.objects.filter(lesson__learning_path=english_course).count()}")
print(f"🏅 Badges: {badges_data.__len__()}")
print("=" * 60)
print("\n🎯 Visit your course at: /learn/spoken-english-mastery/")
print("🔊 Note: Audio files need to be added manually to /static/audio/")