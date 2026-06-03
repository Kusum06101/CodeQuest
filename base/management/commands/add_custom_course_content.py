from django.core.management.base import BaseCommand
from base.models import LearningPath, Lesson
import json

class Command(BaseCommand):
    help = 'Add custom detailed content for specific courses'
    
    def handle(self, *args, **kwargs):
        
        # Custom content for KannadaScript
        kannada_course = LearningPath.objects.get(slug="kannadascript-programming")
        Lesson.objects.filter(learning_path=kannada_course).delete()
        
        Lesson.objects.create(
            learning_path=kannada_course,
            title="KannadaScript - Programming in Kannada",
            slug="kannadascript-intro",
            order=1,
            xp_reward=50,
            theory_content="""
<h2>Welcome to KannadaScript! 🇮🇳</h2>
<p>KannadaScript is a programming language that allows you to write code using Kannada keywords and syntax.</p>

<h3>Why KannadaScript?</h3>
<ul>
    <li>Learn programming in your native language</li>
    <li>Break language barriers in coding</li>
    <li>Preserve and promote Kannada language in tech</li>
</ul>

<h3>Basic KannadaScript Syntax</h3>
<pre><code>// Hello World in KannadaScript
ಮುದ್ರಿಸು("ನಮಸ್ಕಾರ ವಿಶ್ವ!");

// Variables
ಸಂಖ್ಯೆ x = 10;
ಪದ name = "ಕನ್ನಡ";
</code></pre>
            """,
            example_code="""// Simple program in KannadaScript
ಇನ್ಪುಟ್ name = "ಕನ್ನಡಿಗ";
ಮುದ್ರಿಸು("ನಮಸ್ಕಾರ " + name + "!");

ಸಂಖ್ಯೆ a = 10;
ಸಂಖ್ಯೆ b = 20;
ಸಂಖ್ಯೆ sum = a + b;
ಮುದ್ರಿಸು("ಮೊತ್ತ: " + sum);""",
            learning_objectives="Learn to code using KannadaScript",
            key_concepts="Kannada keywords, Variables, Output, Input",
            practice_exercises="""1. Write a program to print your name in Kannada
2. Create variables for age and city in Kannada
3. Write a calculator using Kannada keywords""",
            quiz_questions_json=json.dumps([
                {"question": "What does 'ಮುದ್ರಿಸು' mean?", "options": ["Input", "Output/Print", "Variable", "Loop"], "correct": 1},
                {"question": "How do you declare a number variable?", "options": ["ಸಂಖ್ಯೆ", "ಪದ", "ಅಕ್ಷರ", "ದಶಮಾಂಶ"], "correct": 0}
            ])
        )
        
        self.stdout.write(self.style.SUCCESS('✅ KannadaScript course updated!'))