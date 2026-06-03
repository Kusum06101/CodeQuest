from django.core.management.base import BaseCommand
from base.models import LearningPath, Lesson, ProgrammingLanguage
import json

class Command(BaseCommand):
    help = 'Add detailed content to courses'
    
    def handle(self, *args, **kwargs):
        
        # Get or create Java course
        java_lang, _ = ProgrammingLanguage.objects.get_or_create(
            name="Java",
            defaults={"slug": "java", "is_active": True}
        )
        
        java_path, _ = LearningPath.objects.get_or_create(
            slug="java-enterprise-development",
            defaults={
                "title": "Java Enterprise Development",
                "description": "Master Java Enterprise Edition for building scalable, secure enterprise applications",
                "language": java_lang,
                "difficulty": "INTERMEDIATE",
                "estimated_hours": 40,
                "is_active": True
            }
        )
        
        # Lesson 1: Introduction to Java EE
        lesson1, _ = Lesson.objects.get_or_create(
            learning_path=java_path,
            slug="java-enterprise-intro",
            defaults={
                "title": "Introduction to Java Enterprise Edition",
                "order": 1,
                "xp_reward": 50,
                "theory_content": """
<h2>What is Java EE?</h2>
<p>Java Platform, Enterprise Edition (Java EE) is a set of specifications that extend the Java SE platform to enable development of large-scale, multi-tiered, scalable, reliable, and secure enterprise applications.</p>

<h3>Key Components of Java EE:</h3>
<ul>
    <li><strong>Servlets</strong> - Handle HTTP requests and responses</li>
    <li><strong>JSP (JavaServer Pages)</strong> - Create dynamic web content</li>
    <li><strong>EJB (Enterprise JavaBeans)</strong> - Business logic components</li>
    <li><strong>JPA (Java Persistence API)</strong> - Object-relational mapping</li>
    <li><strong>CDI (Contexts and Dependency Injection)</strong> - Dependency injection</li>
</ul>

<h3>Why Use Java EE?</h3>
<p>Java EE provides a complete platform for enterprise development with built-in security, transaction management, and scalability features. It's used by banks, insurance companies, and large enterprises worldwide.</p>
                """,
                "example_code": """
// Simple Servlet Example
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h1>Hello from Java EE!</h1>");
        out.println("</body></html>");
    }
}
                """,
                "learning_objectives": "By the end of this lesson, you will understand what Java EE is, its key components, and why it's used for enterprise development.",
                "key_concepts": "Java EE, Servlets, JSP, EJB, JPA, CDI, Enterprise Applications",
                "practice_exercises": """
1. Research and list 5 companies that use Java EE for their enterprise applications.
2. Explain the difference between Java SE and Java EE.
3. Draw a diagram showing the Java EE architecture layers.
                """,
                "quiz_questions_json": json.dumps([
                    {
                        "question": "What does Java EE stand for?",
                        "options": ["Java Enterprise Edition", "Java Extended Edition", "Java Embedded Edition", "Java Express Edition"],
                        "correct": 0
                    },
                    {
                        "question": "Which component is used for handling HTTP requests in Java EE?",
                        "options": ["EJB", "JPA", "Servlets", "CDI"],
                        "correct": 2
                    },
                    {
                        "question": "What is JPA used for?",
                        "options": ["Web pages", "Object-relational mapping", "Dependency injection", "Security"],
                        "correct": 1
                    }
                ])
            }
        )
        
        # Lesson 2: Servlets and JSP
        lesson2, _ = Lesson.objects.get_or_create(
            learning_path=java_path,
            slug="servlets-jsp",
            defaults={
                "title": "Servlets and JSP: Building Web Applications",
                "order": 2,
                "xp_reward": 75,
                "theory_content": """
<h2>Understanding Servlets</h2>
<p>Servlets are Java classes that handle HTTP requests and generate responses. They are the foundation of Java web applications.</p>

<h3>Servlet Lifecycle:</h3>
<ol>
    <li><strong>init()</strong> - Called once when servlet is first loaded</li>
    <li><strong>service()</strong> - Handles each request</li>
    <li><strong>destroy()</strong> - Called when servlet is unloaded</li>
</ol>

<h3>JSP (JavaServer Pages)</h3>
<p>JSP allows you to mix HTML with Java code for dynamic content generation. JSP pages are compiled into servlets at runtime.</p>

<h3>JSP Elements:</h3>
<ul>
    <li><strong>Scriptlets</strong> - &lt;% Java code %&gt;</li>
    <li><strong>Expressions</strong> - &lt;%= expression %&gt;</li>
    <li><strong>Declarations</strong> - &lt;%! declaration %&gt;</li>
    <li><strong>Directives</strong> - &lt;%@ directive %&gt;</li>
</ul>
                """,
                "example_code": """
// Complete Servlet Example with Database Connection
@WebServlet("/users")
public class UserServlet extends HttpServlet {
    
    @Inject
    private UserService userService;
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        List<User> users = userService.findAll();
        request.setAttribute("users", users);
        request.getRequestDispatcher("/WEB-INF/views/users.jsp")
               .forward(request, response);
    }
}

// JSP Example (users.jsp)
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head><title>User List</title></head>
<body>
    <h1>Users</h1>
    <table border="1">
        <tr><th>ID</th><th>Name</th><th>Email</th></tr>
        <c:forEach items="${users}" var="user">
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
                """,
                "learning_objectives": "Create dynamic web applications using Servlets and JSP, understand the servlet lifecycle, and implement MVC pattern.",
                "key_concepts": "Servlets, JSP, Servlet Container, Request/Response, Session Management, JSTL",
                "practice_exercises": """
1. Create a login servlet that validates username and password.
2. Build a registration form using JSP and process it with a servlet.
3. Implement session management to track logged-in users.
                """,
                "quiz_questions_json": json.dumps([
                    {
                        "question": "Which method is called once when a servlet is first loaded?",
                        "options": ["service()", "doGet()", "init()", "destroy()"],
                        "correct": 2
                    },
                    {
                        "question": "What does JSP stand for?",
                        "options": ["Java Server Pages", "Java Servlet Pages", "JavaScript Pages", "Java Server Protocols"],
                        "correct": 0
                    },
                    {
                        "question": "Which JSP element is used to include Java code?",
                        "options": ["&lt;%@ directive %&gt;", "&lt;%= expression %&gt;", "&lt;% scriptlet %&gt;", "&lt;%! declaration %&gt;"],
                        "correct": 2
                    }
                ])
            }
        )
        
        # Lesson 3: JPA and Database Integration
        lesson3, _ = Lesson.objects.get_or_create(
            learning_path=java_path,
            slug="jpa-database",
            defaults={
                "title": "JPA and Database Integration",
                "order": 3,
                "xp_reward": 100,
                "theory_content": """
<h2>Java Persistence API (JPA)</h2>
<p>JPA is a specification for object-relational mapping (ORM) in Java. It allows you to map Java objects to database tables.</p>

<h3>Key JPA Annotations:</h3>
<ul>
    <li><strong>@Entity</strong> - Marks a class as a JPA entity</li>
    <li><strong>@Table</strong> - Specifies the database table name</li>
    <li><strong>@Id</strong> - Marks the primary key</li>
    <li><strong>@GeneratedValue</strong> - Auto-generates ID values</li>
    <li><strong>@Column</strong> - Maps to a database column</li>
    <li><strong>@OneToMany</strong>, <strong>@ManyToOne</strong> - Define relationships</li>
</ul>

<h3>Entity Manager Operations:</h3>
<ul>
    <li><strong>persist()</strong> - Insert a new entity</li>
    <li><strong>find()</strong> - Retrieve an entity by ID</li>
    <li><strong>merge()</strong> - Update an existing entity</li>
    <li><strong>remove()</strong> - Delete an entity</li>
    <li><strong>createQuery()</strong> - Execute JPQL queries</li>
</ul>
                """,
                "example_code": """
// JPA Entity Example
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(nullable = false)
    private BigDecimal price;
    
    @ManyToOne
    @JoinColumn(name = "category_id")
    private Category category;
    
    // Getters and setters
}

// Repository Pattern with JPA
@Stateless
public class ProductRepository {
    @PersistenceContext
    private EntityManager em;
    
    public Product findById(Long id) {
        return em.find(Product.class, id);
    }
    
    public List<Product> findAll() {
        return em.createQuery("SELECT p FROM Product p", Product.class)
                 .getResultList();
    }
    
    public void save(Product product) {
        if (product.getId() == null) {
            em.persist(product);
        } else {
            em.merge(product);
        }
    }
    
    public void delete(Long id) {
        Product product = findById(id);
        if (product != null) {
            em.remove(product);
        }
    }
}
                """,
                "learning_objectives": "Master JPA for database operations, create entity mappings, and implement CRUD operations.",
                "key_concepts": "JPA, ORM, Entity Manager, JPQL, Relationships, Transactions",
                "practice_exercises": """
1. Create a JPA entity for a Customer with name, email, and address fields.
2. Implement a repository class with find, save, update, and delete methods.
3. Write a JPQL query to find customers by email domain.
                """,
                "quiz_questions_json": json.dumps([
                    {
                        "question": "Which annotation marks a class as a JPA entity?",
                        "options": ["@Table", "@Entity", "@Id", "@Column"],
                        "correct": 1
                    },
                    {
                        "question": "What does ORM stand for?",
                        "options": ["Object-Relational Mapping", "Object Request Management", "Object Relational Model", "Online Resource Management"],
                        "correct": 0
                    },
                    {
                        "question": "Which method is used to insert a new entity?",
                        "options": ["merge()", "find()", "persist()", "remove()"],
                        "correct": 2
                    }
                ])
            }
        )
        
        # Lesson 4: CDI and Dependency Injection
        lesson4, _ = Lesson.objects.get_or_create(
            learning_path=java_path,
            slug="cdi-dependency-injection",
            defaults={
                "title": "CDI and Dependency Injection",
                "order": 4,
                "xp_reward": 85,
                "theory_content": """
<h2>Contexts and Dependency Injection (CDI)</h2>
<p>CDI is the standard dependency injection framework in Java EE. It helps manage the lifecycle of objects and their dependencies.</p>

<h3>Core CDI Concepts:</h3>
<ul>
    <li><strong>@Inject</strong> - Inject dependencies automatically</li>
    <li><strong>@Named</strong> - Give a bean a name for EL access</li>
    <li><strong>@RequestScoped</strong> - Bean lives for one HTTP request</li>
    <li><strong>@SessionScoped</strong> - Bean lives for a user session</li>
    <li><strong>@ApplicationScoped</strong> - Bean lives for application lifetime</li>
    <li><strong>@Produces</strong> - Factory method for creating beans</li>
</ul>

<h3>Benefits of CDI:</h3>
<ul>
    <li>Loose coupling between components</li>
    <li>Better testability</li>
    <li>Automatic lifecycle management</li>
    <li>Type-safe injection</li>
    <li>Interceptor and decorator support</li>
</ul>
                """,
                "example_code": """
// Service with CDI
@ApplicationScoped
public class UserService {
    @Inject
    private UserRepository userRepository;
    
    @Inject
    @LoggedIn
    private User currentUser;
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    @Transactional
    public void updateUser(User user) {
        userRepository.save(user);
    }
}

// Producer method
@ApplicationScoped
public class Resources {
    @Produces
    @PersistenceContext
    private EntityManager em;
    
    @Produces
    @LoggedIn
    @SessionScoped
    public User getCurrentUser(@Inject HttpServletRequest request) {
        return (User) request.getSession().getAttribute("user");
    }
}

// Qualifier annotation
@Qualifier
@Retention(RUNTIME)
@Target({FIELD, TYPE, METHOD})
public @interface LoggedIn {}
                """,
                "learning_objectives": "Master CDI for dependency injection, understand scopes, and create loosely coupled applications.",
                "key_concepts": "CDI, Dependency Injection, Scopes, Qualifiers, Producers, Interceptors",
                "practice_exercises": """
1. Create a service with CDI injection and appropriate scope.
2. Implement a custom qualifier annotation.
3. Create a producer method for a configuration object.
                """,
                "quiz_questions_json": json.dumps([
                    {
                        "question": "Which annotation is used for dependency injection in CDI?",
                        "options": ["@Autowired", "@Resource", "@Inject", "@Dependency"],
                        "correct": 2
                    },
                    {
                        "question": "Which scope keeps a bean alive for the entire application?",
                        "options": ["@RequestScoped", "@SessionScoped", "@ApplicationScoped", "@Dependent"],
                        "correct": 2
                    },
                    {
                        "question": "What is a key benefit of CDI?",
                        "options": ["Loose coupling", "Faster execution", "Smaller code", "Better security"],
                        "correct": 0
                    }
                ])
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added content to {java_path.title}'))
        self.stdout.write(self.style.SUCCESS(f'Added {Lesson.objects.filter(learning_path=java_path).count()} lessons'))