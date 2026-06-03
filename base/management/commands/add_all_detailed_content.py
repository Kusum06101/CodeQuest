# base/management/commands/add_all_detailed_content.py
from django.core.management.base import BaseCommand
from django.db import transaction
from base.models import LearningPath, Lesson, ProgrammingLanguage
import json

class Command(BaseCommand):
    help = 'Add detailed content, quizzes, and practice code for all courses'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        
        # ============================================
        # CONTENT TEMPLATES
        # ============================================
        
        def get_basic_lesson(lang_name, lesson_num, title, content_type):
            """Generate basic lesson content"""
            templates = {
                'intro': f'''
<h2>Welcome to {lang_name} Programming!</h2>
<p>{lang_name} is a powerful programming language used for various applications.</p>

<h3>Why Learn {lang_name}?</h3>
<ul>
    <li>High demand in the job market</li>
    <li>Versatile and powerful</li>
    <li>Large community support</li>
    <li>Great for beginners and experts</li>
</ul>

<h3>What You'll Learn</h3>
<p>In this lesson, you'll understand the basics of {lang_name} programming, including syntax, variables, and basic operations.</p>
''',
                'syntax': f'''
<h2>{lang_name} Basic Syntax</h2>

<h3>Hello World Program</h3>
<pre><code>// Your first {lang_name} program
print("Hello, World!");</code></pre>

<h3>Key Concepts</h3>
<ul>
    <li>Comments - Document your code</li>
    <li>Indentation - Code blocks</li>
    <li>Variables - Store data</li>
    <li>Data Types - Types of information</li>
</ul>
''',
                'variables': f'''
<h2>Variables and Data Types in {lang_name}</h2>

<h3>What are Variables?</h3>
<p>Variables are containers for storing data values.</p>

<h3>Common Data Types</h3>
<ul>
    <li><strong>Numbers</strong> - Integers and decimals</li>
    <li><strong>Strings</strong> - Text data</li>
    <li><strong>Booleans</strong> - True/False values</li>
    <li><strong>Lists/Arrays</strong> - Collections of items</li>
    <li><strong>Dictionaries/Objects</strong> - Key-value pairs</li>
</ul>

<h3>Naming Conventions</h3>
<p>Use descriptive names, start with lowercase, use underscores for multiple words.</p>
''',
                'control': f'''
<h2>Control Flow in {lang_name}</h2>

<h3>Conditional Statements</h3>
<pre><code>if condition:
    # code executes if true
elif other_condition:
    # code executes if previous false and this true
else:
    # code executes if all false</code></pre>

<h3>Loops</h3>
<pre><code># For loop - iterate over a sequence
for item in collection:
    process(item)

# While loop - repeat while condition is true
while condition:
    do_something()</code></pre>
''',
                'functions': f'''
<h2>Functions in {lang_name}</h2>

<h3>Defining Functions</h3>
<pre><code>def function_name(parameters):
    """Docstring explaining the function"""
    # function body
    return result</code></pre>

<h3>Function Benefits</h3>
<ul>
    <li>Code reuse</li>
    <li>Modularity</li>
    <li>Easier debugging</li>
    <li>Better organization</li>
</ul>
''',
                'collections': f'''
<h2>Working with Collections in {lang_name}</h2>

<h3>Lists/Arrays</h3>
<pre><code># Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]

# Common operations
fruits.append("orange")     # Add element
fruits.remove("banana")     # Remove element
fruits.sort()               # Sort the list</code></pre>

<h3>Dictionaries/Objects</h3>
<pre><code># Key-value pairs
person = {{
    "name": "John",
    "age": 30,
    "city": "New York"
}}

# Access values
print(person["name"])</code></pre>
'''
            }
            return templates.get(content_type, templates['intro'])
        
        def get_code_example(lang_name, difficulty):
            examples = {
                'easy': f'''# Simple {lang_name} Program
def main():
    # Get user input
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    
    # Display output
    print(f"Hello {{name}}!")
    print(f"You are {{age}} years old")
    print(f"Next year you will be {{age + 1}}")

# Run the program
if __name__ == "__main__":
    main()''',
                'medium': f'''# {lang_name} Calculator
def calculator():
    print("=== {lang_name} Calculator ===")
    print("1. Add")
    print("2. Subtract") 
    print("3. Multiply")
    print("4. Divide")
    
    choice = int(input("Choose operation: "))
    num1 = float(input("First number: "))
    num2 = float(input("Second number: "))
    
    if choice == 1:
        result = num1 + num2
        op = "+"
    elif choice == 2:
        result = num1 - num2
        op = "-"
    elif choice == 3:
        result = num1 * num2
        op = "*"
    elif choice == 4:
        if num2 != 0:
            result = num1 / num2
            op = "/"
        else:
            return "Error: Division by zero"
    else:
        return "Invalid choice"
    
    return f"{{num1}} {{op}} {{num2}} = {{result}}"

print(calculator())''',
                'hard': f'''# {lang_name} Number Guessing Game
import random

def guess_the_number():
    print("=== Number Guessing Game ===")
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Guess (1-100), attempts left: {{max_attempts - attempts}}: "))
            attempts += 1
            
            if guess < secret:
                print("Too low! Try again.")
            elif guess > secret:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed in {{attempts}} attempts!")
                score = (max_attempts - attempts + 1) * 10
                print(f"Your score: {{score}} points")
                return
        except ValueError:
            print("Please enter a valid number!")
    
    print(f"Game over! The number was {{secret}}")
    print("Better luck next time!")

if __name__ == "__main__":
    guess_the_number()'''
            }
            return examples.get(difficulty, examples['easy'])
        
        def get_practice_exercises(lang_name, level):
            exercises = {
                'beginner': f"""
1. 📝 **Basic Output**: Write a program that prints "Hello, {lang_name}!"
2. 🔢 **Variables**: Create variables for your name, age, and favorite color, then print them
3. ➕ **Simple Calculator**: Write a program that adds two numbers entered by the user
4. 🔄 **Even or Odd**: Take a number input and check if it's even or odd
5. 📊 **Grade Calculator**: Ask for 3 test scores and calculate the average
""",
                'intermediate': f"""
1. 🎯 **Prime Numbers**: Write a function to check if a number is prime
2. 📋 **List Operations**: Create a program that finds the largest and smallest numbers in a list
3. 🔁 **Factorial**: Write a recursive function to calculate factorial
4. 🔑 **Password Validator**: Create a function that validates password strength
5. 📈 **Fibonacci Sequence**: Generate the first N numbers in the Fibonacci sequence
""",
                'advanced': f"""
1. 🎮 **Game Development**: Create a text-based game with multiple choices
2. 📊 **Data Analysis**: Write a program to analyze a dataset and find statistics
3. 🌐 **API Integration**: Build a program that fetches data from a public API
4. 🗄️ **File Processing**: Create a file reader/writer with error handling
5. 🔄 **Sorting Algorithm**: Implement bubble sort or quicksort manually
"""
            }
            return exercises.get(level, exercises['beginner'])
        
        def get_quiz_questions(lang_name, topic, level):
            base_quizzes = {
                'syntax': [
                    {"question": f"What is the correct way to print in {lang_name}?", "options": ["print()", "console.log()", "System.out.println()", "echo"], "correct": 0},
                    {"question": "Which of these is a valid variable name?", "options": ["2var", "_myVar", "my-var", "my var"], "correct": 1},
                    {"question": "What is used for single-line comments?", "options": ["//", "#", "<!-- -->", "/* */"], "correct": 0 if lang_name != "Python" else 1},
                ],
                'variables': [
                    {"question": "What is the correct way to create a variable?", "options": ["var x = 5", "x = 5", "int x = 5", "let x = 5"], "correct": 1},
                    {"question": "Which data type is used for whole numbers?", "options": ["float", "string", "int", "boolean"], "correct": 2},
                    {"question": "What is the result of 10 / 3 (integer division)?", "options": ["3.33", "3", "3.0", "4"], "correct": 1},
                ],
                'control': [
                    {"question": "What does 'break' do in a loop?", "options": ["Skips current iteration", "Exits the loop entirely", "Restarts the loop", "Does nothing"], "correct": 1},
                    {"question": "Which loop is best when you know the number of iterations?", "options": ["while loop", "for loop", "do-while loop", "infinite loop"], "correct": 1},
                    {"question": "What is the purpose of 'else' in conditional statements?", "options": ["Ends the program", "Executes when condition is false", "Restarts the program", "Creates a loop"], "correct": 1},
                ],
                'functions': [
                    {"question": "What keyword is used to define a function?", "options": ["def", "function", "func", "define"], "correct": 0},
                    {"question": "What is a return statement used for?", "options": ["Print output", "End program", "Return value to caller", "Create variable"], "correct": 2},
                    {"question": "What is a parameter?", "options": ["Function name", "Input to a function", "Output of function", "Variable type"], "correct": 1},
                ],
                'collections': [
                    {"question": "Which collection is immutable?", "options": ["List", "Array", "Tuple", "Dictionary"], "correct": 2},
                    {"question": "How do you access the first element of a list?", "options": ["list[0]", "list[1]", "list.first()", "list[begin]"], "correct": 0},
                    {"question": "What data structure stores key-value pairs?", "options": ["List", "Array", "Dictionary", "Set"], "correct": 2},
                ]
            }
            return base_quizzes.get(topic, base_quizzes['syntax'])
        
        # Get all courses that need content
        courses = LearningPath.objects.filter(is_active=True).exclude(
            slug__in=['python-mastery', 'java-enterprise-development', 'javascript-mastery', 'html-css-mastery']
        )
        
        self.stdout.write(self.style.SUCCESS(f'\n📚 Found {courses.count()} courses to update\n'))
        
        for course in courses:
            self.stdout.write(f'Processing: {course.title}...')
            
            # Clear existing lessons for this course
            existing_lessons = Lesson.objects.filter(learning_path=course)
            if existing_lessons.exists():
                existing_lessons.delete()
                self.stdout.write(self.style.WARNING(f'  Removed {existing_lessons.count()} existing lessons'))
            
            # Determine language and difficulty
            lang_name = course.title.split()[0] if course.title.split() else "Programming"
            difficulty = course.difficulty.lower()
            
            # Create 3-5 lessons based on course
            num_lessons = min(5, max(3, course.estimated_hours // 15))
            
            lessons_data = [
                {
                    'title': f'Introduction to {course.title}',
                    'slug': f'{course.slug}-intro',
                    'order': 1,
                    'xp': 50,
                    'topic': 'intro',
                    'content_type': 'intro'
                },
                {
                    'title': f'{lang_name} Syntax and Basics',
                    'slug': f'{course.slug}-syntax',
                    'order': 2,
                    'xp': 60,
                    'topic': 'syntax',
                    'content_type': 'syntax'
                },
                {
                    'title': f'Variables and Data Types',
                    'slug': f'{course.slug}-variables',
                    'order': 3,
                    'xp': 70,
                    'topic': 'variables',
                    'content_type': 'variables'
                },
                {
                    'title': f'Control Flow: Conditionals and Loops',
                    'slug': f'{course.slug}-control-flow',
                    'order': 4,
                    'xp': 80,
                    'topic': 'control',
                    'content_type': 'control'
                },
                {
                    'title': f'Functions and Code Organization',
                    'slug': f'{course.slug}-functions',
                    'order': 5,
                    'xp': 90,
                    'topic': 'functions',
                    'content_type': 'functions'
                }
            ][:num_lessons]
            
            for lesson_data in lessons_data:
                # Get quiz questions
                quiz_questions = get_quiz_questions(lang_name, lesson_data['topic'], difficulty)
                
                Lesson.objects.create(
                    learning_path=course,
                    title=lesson_data['title'],
                    slug=lesson_data['slug'],
                    order=lesson_data['order'],
                    xp_reward=lesson_data['xp'],
                    theory_content=get_basic_lesson(lang_name, lesson_data['order'], lesson_data['title'], lesson_data['content_type']),
                    example_code=get_code_example(lang_name, difficulty),
                    learning_objectives=f"By the end of this lesson, you will be able to understand and use {lesson_data['topic']} concepts in {lang_name}.",
                    key_concepts=f"{lang_name.capitalize()} {lesson_data['topic'].capitalize()}, Syntax, Best Practices",
                    practice_exercises=get_practice_exercises(lang_name, difficulty),
                    quiz_questions_json=json.dumps(quiz_questions),
                    is_locked=False
                )
                self.stdout.write(self.style.SUCCESS(f'    + Added: {lesson_data["title"]}'))
            
            lesson_count = Lesson.objects.filter(learning_path=course).count()
            total_xp = sum(lesson.xp_reward for lesson in Lesson.objects.filter(learning_path=course))
            self.stdout.write(self.style.SUCCESS(f'  ✓ Complete: {lesson_count} lessons, {total_xp} total XP'))
            self.stdout.write('')
        
        # Now update the detailed courses we already created
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✨ ALL COURSES UPDATED WITH DETAILED CONTENT! ✨'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Summary
        total_courses = LearningPath.objects.filter(is_active=True).count()
        total_lessons = Lesson.objects.count()
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'   Total Courses: {total_courses}')
        self.stdout.write(f'   Total Lessons: {total_lessons}')
        self.stdout.write(f'   Average Lessons per Course: {total_lessons/total_courses:.1f}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Visit: http://127.0.0.1:8000/learn/ to see all courses!'))

# Also create a command to add custom detailed content for specific courses
class CommandWithDetails(Command):
    pass