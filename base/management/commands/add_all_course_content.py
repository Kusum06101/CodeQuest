# base/management/commands/add_all_course_content.py
from django.core.management.base import BaseCommand
from django.db import transaction
from base.models import LearningPath, Lesson, ProgrammingLanguage
import json

class Command(BaseCommand):
    help = 'Add comprehensive course content for all programming languages'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        
        # ============================================
        # PYTHON COURSE
        # ============================================
        python_lang, _ = ProgrammingLanguage.objects.get_or_create(
            name="Python",
            defaults={"slug": "python", "is_active": True}
        )
        
        python_path, created = LearningPath.objects.get_or_create(
            slug="python-mastery",
            defaults={
                "title": "Python Mastery",
                "description": "Complete Python programming from beginner to advanced",
                "language": python_lang,
                "difficulty": "BEGINNER",
                "estimated_hours": 60,
                "is_active": True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {python_path.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Updating course: {python_path.title}'))
            Lesson.objects.filter(learning_path=python_path).delete()
        
        # Lesson 1: Python Basics
        Lesson.objects.create(
            learning_path=python_path,
            title="Python Basics: Variables and Data Types",
            slug="python-variables-data-types",
            order=1,
            xp_reward=50,
            theory_content='<h2>Welcome to Python!</h2><p>Python is a high-level, interpreted programming language.</p><h3>Variables</h3><pre><code>name = "Alice"\nage = 25\nheight = 5.7\nis_student = True</code></pre><h3>Data Types</h3><ul><li>int - Integer numbers</li><li>float - Decimal numbers</li><li>str - Text strings</li><li>bool - True/False</li></ul>',
            example_code='name = input("Enter name: ")\nage = int(input("Enter age: "))\nprint(f"Hello {name}!")',
            learning_objectives="Understand Python variables and data types",
            key_concepts="Variables, Data Types, Input/Output",
            practice_exercises="1. Create variables for name and age\n2. Write a program to add two numbers\n3. Create a student dictionary",
            quiz_questions_json=json.dumps([
                {"question": "What is type(10.5)?", "options": ["int", "float", "str"], "correct": 1},
                {"question": "Valid variable name?", "options": ["2var", "_my_var", "my-var"], "correct": 1},
                {"question": "What does input() return?", "options": ["Integer", "String", "Float"], "correct": 1}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Python Basics'))
        
        # Lesson 2: Control Flow
        Lesson.objects.create(
            learning_path=python_path,
            title="Control Flow: If Statements and Loops",
            slug="python-control-flow",
            order=2,
            xp_reward=75,
            theory_content='<h2>Control Flow</h2><p>Control flow statements make decisions and repeat actions.</p><pre><code>age = 18\nif age >= 18:\n    print("You can vote!")\n\nfor i in range(5):\n    print(i)\n\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1</code></pre>',
            example_code='import random\nsecret = random.randint(1,100)\nfor attempt in range(10):\n    guess = int(input("Guess: "))\n    if guess == secret:\n        print("Correct!")\n        break',
            learning_objectives="Master conditional statements and loops",
            key_concepts="If-else, For loops, While loops, Break",
            practice_exercises="1. Check positive/negative number\n2. Create multiplication table\n3. Print prime numbers",
            quiz_questions_json=json.dumps([
                {"question": "What does break do?", "options": ["Exits loop", "Skips iteration", "Restarts"], "correct": 0},
                {"question": "Best loop for known iterations?", "options": ["while", "for"], "correct": 1}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Control Flow'))
        
        # Lesson 3: Functions
        Lesson.objects.create(
            learning_path=python_path,
            title="Functions and Modules",
           slug="python-functions",
            order=3,
            xp_reward=100,
            theory_content='<h2>Functions</h2><p>Functions are reusable code blocks.</p><pre><code>def greet(name):\n    return f"Hello, {name}!"\n\ndef add(a, b):\n    return a + b\n\nsquare = lambda x: x ** 2</code></pre>',
            example_code='def add(x,y): return x+y\ndef subtract(x,y): return x-y\nprint(f"5+3={add(5,3)}")',
            learning_objectives="Create reusable functions",
            key_concepts="Functions, Parameters, Return values, Lambda",
            practice_exercises="1. Create prime checker\n2. Write factorial function\n3. Build a calculator",
            quiz_questions_json=json.dumps([
                {"question": "Keyword to define function?", "options": ["def", "func", "define"], "correct": 0},
                {"question": "Lambda is?", "options": ["Named", "Anonymous"], "correct": 1}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Functions'))
        
        # Lesson 4: Collections
        Lesson.objects.create(
            learning_path=python_path,
            title="Lists, Tuples, and Dictionaries",
            slug="python-collections",
            order=4,
            xp_reward=85,
            theory_content='<h2>Python Collections</h2><p>Data structures for organizing data.</p><pre><code>fruits = ["apple", "banana", "cherry"]\nfruits.append("orange")\n\nstudent = {\n    "name": "Alice",\n    "age": 22,\n    "grades": [85, 90, 88]\n}</code></pre>',
            example_code='students = {}\nstudents["Alice"] = [85, 90, 88]\nstudents["Bob"] = [78, 82, 80]\nfor name, grades in students.items():\n    avg = sum(grades)/len(grades)\n    print(f"{name}: {avg:.1f}")',
            learning_objectives="Master Python collections",
            key_concepts="Lists, Tuples, Dictionaries, Sets",
            practice_exercises="1. Create to-do list\n2. Build word counter\n3. Remove duplicates from list",
            quiz_questions_json=json.dumps([
                {"question": "Which collection is immutable?", "options": ["List", "Tuple", "Dictionary"], "correct": 1},
                {"question": "How to access last list element?", "options": ["list[0]", "list[-1]", "list[end]"], "correct": 1}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Collections'))
        
        # ============================================
        # JAVA COURSE  
        # ============================================
        java_lang, _ = ProgrammingLanguage.objects.get_or_create(
            name="Java",
            defaults={"slug": "java", "is_active": True}
        )
        
        java_path, created = LearningPath.objects.get_or_create(
            slug="java-enterprise-development",
            defaults={
                "title": "Java Enterprise Development",
                "description": "Master Java Enterprise Edition",
                "language": java_lang,
                "difficulty": "INTERMEDIATE",
                "estimated_hours": 80,
                "is_active": True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'\nCreated course: {java_path.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'\nUpdating course: {java_path.title}'))
            Lesson.objects.filter(learning_path=java_path).delete()
        
        # Java Lesson 1
        Lesson.objects.create(
            learning_path=java_path,
            title="Introduction to Java EE",
            slug="java-enterprise-intro",
            order=1,
            xp_reward=50,
            theory_content='<h2>What is Java EE?</h2><p>Java Platform, Enterprise Edition for enterprise applications.</p><h3>Key Components:</h3><ul><li>Servlets - HTTP requests</li><li>JSP - Dynamic web content</li><li>EJB - Business logic</li><li>JPA - Database mapping</li></ul>',
            example_code='public class HelloServlet extends HttpServlet {\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) {\n        res.getWriter().println("Hello from Java EE!");\n    }\n}',
            learning_objectives="Understand Java EE architecture",
            key_concepts="Java EE, Servlets, JSP, EJB, JPA",
            practice_exercises="1. Set up Java EE environment\n2. Create first servlet\n3. Deploy web application",
            quiz_questions_json=json.dumps([
                {"question": "What does Java EE stand for?", "options": ["Java Enterprise Edition", "Java Extended Edition", "Java Embedded Edition"], "correct": 0},
                {"question": "Which component handles HTTP?", "options": ["EJB", "JPA", "Servlets"], "correct": 2}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Java EE Introduction'))
        
        # Java Lesson 2
        Lesson.objects.create(
            learning_path=java_path,
            title="Servlets and JSP",
            slug="servlets-jsp",
            order=2,
            xp_reward=75,
            theory_content='<h2>Servlets and JSP</h2><p>Servlets handle HTTP requests. JSP mixes HTML with Java.</p><h3>Servlet Lifecycle:</h3><ol><li>init() - First load</li><li>service() - Each request</li><li>destroy() - Unload</li></ol>',
            example_code='@WebServlet("/users")\npublic class UserServlet extends HttpServlet {\n    protected void doGet(HttpServletRequest req, HttpServletResponse res) {\n        req.getRequestDispatcher("/users.jsp").forward(req, res);\n    }\n}',
            learning_objectives="Create web apps with Servlets and JSP",
            key_concepts="Servlets, JSP, Servlet Lifecycle",
            practice_exercises="1. Create login servlet\n2. Build registration form\n3. Implement sessions",
            quiz_questions_json=json.dumps([
                {"question": "First method called in servlet?", "options": ["service()", "init()", "doGet()"], "correct": 1},
                {"question": "What does JSP stand for?", "options": ["Java Server Pages", "Java Servlet Pages", "JavaScript Pages"], "correct": 0}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: Servlets and JSP'))
        
        # Java Lesson 3
        Lesson.objects.create(
            learning_path=java_path,
            title="JPA and Database Integration",
            slug="jpa-database",
            order=3,
            xp_reward=100,
            theory_content='<h2>Java Persistence API (JPA)</h2><p>JPA is for object-relational mapping in Java.</p><h3>Key Annotations:</h3><ul><li>@Entity - Marks entity class</li><li>@Table - Table name</li><li>@Id - Primary key</li><li>@Column - Column mapping</li></ul>',
            example_code='@Entity\n@Table(name="products")\npublic class Product {\n    @Id\n    @GeneratedValue\n    private Long id;\n    private String name;\n    private BigDecimal price;\n}',
            learning_objectives="Master JPA for database operations",
            key_concepts="JPA, ORM, Entity Manager, JPQL",
            practice_exercises="1. Create Customer entity\n2. Implement CRUD\n3. Write JPQL queries",
            quiz_questions_json=json.dumps([
                {"question": "Entity annotation?", "options": ["@Table", "@Entity", "@Id"], "correct": 1},
                {"question": "What does ORM stand for?", "options": ["Object-Relational Mapping", "Object Request Management", "Object Relational Model"], "correct": 0}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: JPA and Database'))
        
        # ============================================
        # JAVASCRIPT COURSE
        # ============================================
        js_lang, _ = ProgrammingLanguage.objects.get_or_create(
            name="JavaScript",
            defaults={"slug": "javascript", "is_active": True}
        )
        
        js_path, created = LearningPath.objects.get_or_create(
            slug="javascript-mastery",
            defaults={
                "title": "JavaScript Mastery",
                "description": "Complete JavaScript programming from fundamentals to ES6+",
                "language": js_lang,
                "difficulty": "BEGINNER",
                "estimated_hours": 50,
                "is_active": True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'\nCreated course: {js_path.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'\nUpdating course: {js_path.title}'))
            Lesson.objects.filter(learning_path=js_path).delete()
        
        # JavaScript Lesson
        Lesson.objects.create(
            learning_path=js_path,
            title="JavaScript Fundamentals",
            slug="javascript-fundamentals",
            order=1,
            xp_reward=50,
            theory_content='<h2>JavaScript Basics</h2><p>JavaScript is the language of the web.</p><h3>Variables</h3><pre><code>let name = "Alice";\nconst age = 25;\nvar oldWay = "avoid";</code></pre><h3>Functions</h3><pre><code>function greet(name) {\n    return `Hello, ${name}!`;\n}\n\nconst add = (a, b) => a + b;</code></pre>',
            example_code='function calculate() {\n    let num1 = prompt("First number:");\n    let num2 = prompt("Second number:");\n    let result = Number(num1) + Number(num2);\n    alert("Sum: " + result);\n}\ncalculate();',
            learning_objectives="Master JavaScript fundamentals and ES6+",
            key_concepts="Variables, Functions, Arrow functions, DOM",
            practice_exercises="1. Reverse a string\n2. Build counter with closure\n3. Filter array of objects",
            quiz_questions_json=json.dumps([
                {"question": "Constant variable keyword?", "options": ["let", "var", "const"], "correct": 2},
                {"question": "What does map() do?", "options": ["Filters", "Transforms", "Reduces"], "correct": 1}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: JavaScript Fundamentals'))
        
        # ============================================
        # HTML/CSS COURSE
        # ============================================
        html_lang, _ = ProgrammingLanguage.objects.get_or_create(
            name="HTML/CSS",
            defaults={"slug": "html-css", "is_active": True}
        )
        
        html_path, created = LearningPath.objects.get_or_create(
            slug="html-css-mastery",
            defaults={
                "title": "HTML & CSS Mastery",
                "description": "Build beautiful, responsive websites",
                "language": html_lang,
                "difficulty": "BEGINNER",
                "estimated_hours": 40,
                "is_active": True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'\nCreated course: {html_path.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'\nUpdating course: {html_path.title}'))
            Lesson.objects.filter(learning_path=html_path).delete()
        
        # HTML Lesson
        Lesson.objects.create(
            learning_path=html_path,
            title="HTML Fundamentals",
            slug="html-fundamentals",
            order=1,
            xp_reward=50,
            theory_content='<h2>HTML Basics</h2><p>HTML structures web content.</p><h3>Basic Document</h3><pre><code><!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n</head>\n<body>\n    <h1>Hello World</h1>\n</body>\n</html></code></pre><h3>Common Tags</h3><ul><li>h1-h6 - Headings</li><li>p - Paragraph</li><li>a - Links</li><li>img - Images</li><li>div - Container</li></ul>',
            example_code='<div class="card">\n    <h2>Welcome</h2>\n    <p>This is a card component</p>\n    <a href="#">Learn More</a>\n</div>',
            learning_objectives="Create well-structured HTML documents",
            key_concepts="HTML tags, Semantic HTML, Forms, Links",
            practice_exercises="1. Create personal bio page\n2. Build navigation menu\n3. Design contact form",
            quiz_questions_json=json.dumps([
                {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup"], "correct": 0},
                {"question": "Which tag creates a link?", "options": ["link", "a", "href"], "correct": 1},
                {"question": "Correct HTML5 doctype?", "options": ["!DOCTYPE html", "!DOCTYPE HTML5", "!DOCTYPE html PUBLIC"], "correct": 0}
            ])
        )
        self.stdout.write(self.style.SUCCESS('  + Added: HTML Fundamentals'))
        
        # ============================================
        # SUMMARY
        # ============================================
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✨ All courses added successfully! ✨'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\n📚 Available courses:')
        self.stdout.write('  → /learn/python-mastery/ (4 lessons)')
        self.stdout.write('  → /learn/java-enterprise-development/ (3 lessons)')
        self.stdout.write('  → /learn/javascript-mastery/ (1 lesson)')
        self.stdout.write('  → /learn/html-css-mastery/ (1 lesson)')