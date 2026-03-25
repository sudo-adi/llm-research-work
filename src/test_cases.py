"""
Ground-truth test cases for all 5 domains.
Each case has: input, expected_output, and domain tag.
"""

JSON_EXTRACTION_CASES = [
    {
        "input": "John Smith is 34 years old and lives in New York. He works as a software engineer.",
        "expected": {"name": "John Smith", "age": 34, "city": "New York", "job": "software engineer"},
    },
    {
        "input": "Maria Garcia, 28, from Chicago. She is a doctor at St. Mary's hospital.",
        "expected": {"name": "Maria Garcia", "age": 28, "city": "Chicago", "job": "doctor"},
    },
    {
        "input": "The product SKU is AB-1042, priced at $29.99, available in red and blue.",
        "expected": {"sku": "AB-1042", "price": 29.99, "colors": ["red", "blue"]},
    },
    {
        "input": "Flight AA204 departs at 08:30 from Dallas, arrives at 11:45 in Los Angeles.",
        "expected": {"flight": "AA204", "departure": "08:30", "from": "Dallas", "arrival": "11:45", "to": "Los Angeles"},
    },
    {
        "input": "Order #5523 placed on March 12 for 3 units of Widget X at $15 each.",
        "expected": {"order_id": "5523", "date": "March 12", "quantity": 3, "item": "Widget X", "unit_price": 15},
    },
    {
        "input": "Dr. Raj Patel, 45, is a cardiologist based in Houston with 20 years of experience.",
        "expected": {"name": "Dr. Raj Patel", "age": 45, "specialty": "cardiologist", "city": "Houston", "experience_years": 20},
    },
    {
        "input": "The laptop model XPS-15 has 16GB RAM, 512GB SSD, and costs $1,299.",
        "expected": {"model": "XPS-15", "ram_gb": 16, "storage_gb": 512, "price": 1299},
    },
    {
        "input": "Emma Wilson, age 22, studies computer science at MIT. She is from Boston.",
        "expected": {"name": "Emma Wilson", "age": 22, "field": "computer science", "university": "MIT", "city": "Boston"},
    },
    {
        "input": "Invoice INV-8821 for client TechCorp, total amount $4,500, due April 30.",
        "expected": {"invoice_id": "INV-8821", "client": "TechCorp", "amount": 4500, "due_date": "April 30"},
    },
    {
        "input": "Restaurant La Bella opens at 11am and closes at 10pm. It is located at 45 Main St.",
        "expected": {"name": "La Bella", "open": "11am", "close": "10pm", "address": "45 Main St"},
    },
    {
        "input": "Package tracking ID TRK9901 shipped on Jan 5, expected delivery Jan 10, from Seattle.",
        "expected": {"tracking_id": "TRK9901", "shipped_date": "Jan 5", "expected_delivery": "Jan 10", "origin": "Seattle"},
    },
    {
        "input": "Professor Alan Moore teaches physics at Stanford. He has a PhD from Caltech.",
        "expected": {"name": "Prof. Alan Moore", "subject": "physics", "university": "Stanford", "degree": "PhD", "degree_from": "Caltech"},
    },
    {
        "input": "Car model Tesla Model 3 year 2023, mileage 12000 km, color white, price $38000.",
        "expected": {"model": "Tesla Model 3", "year": 2023, "mileage_km": 12000, "color": "white", "price": 38000},
    },
    {
        "input": "Meeting scheduled for Feb 14 at 3pm in Conference Room B with the design team.",
        "expected": {"date": "Feb 14", "time": "3pm", "location": "Conference Room B", "team": "design"},
    },
    {
        "input": "Subscription plan Gold costs $49/month, includes 5 users and 100GB storage.",
        "expected": {"plan": "Gold", "monthly_price": 49, "users": 5, "storage_gb": 100},
    },
    {
        "input": "Ticket #T-2210 reported by user alice@gmail.com on Dec 3, priority high, status open.",
        "expected": {"ticket_id": "T-2210", "reporter": "alice@gmail.com", "date": "Dec 3", "priority": "high", "status": "open"},
    },
    {
        "input": "Employee ID E-4421, name Sarah Kim, department marketing, salary $62000 per year.",
        "expected": {"employee_id": "E-4421", "name": "Sarah Kim", "department": "marketing", "salary": 62000},
    },
    {
        "input": "Warehouse WH-07 holds 5000 units of item code IC-330, located in Phoenix, AZ.",
        "expected": {"warehouse": "WH-07", "units": 5000, "item_code": "IC-330", "location": "Phoenix, AZ"},
    },
    {
        "input": "Loan amount $250,000 at 6.5% interest rate, 30-year term, applicant James Brown.",
        "expected": {"amount": 250000, "interest_rate": 6.5, "term_years": 30, "applicant": "James Brown"},
    },
    {
        "input": "Event 'Tech Summit 2025' on July 18, venue Convention Center, expected 2000 attendees.",
        "expected": {"event": "Tech Summit 2025", "date": "July 18", "venue": "Convention Center", "attendees": 2000},
    },
]

MATH_WORD_PROBLEM_CASES = [
    {"input": "A shop sells apples for $2 each and oranges for $3 each. Tom buys 4 apples and 3 oranges. How much does Tom spend?", "expected": "17"},
    {"input": "A train travels 60 km/h for 2 hours then 80 km/h for 3 hours. What is the total distance?", "expected": "360"},
    {"input": "A class has 30 students. 40% are girls. How many boys are in the class?", "expected": "18"},
    {"input": "A rectangle has length 12 cm and width 5 cm. What is its perimeter?", "expected": "34"},
    {"input": "If 5 workers finish a job in 8 days, how many days will 10 workers take for the same job?", "expected": "4"},
    {"input": "A shirt costs $40. A 25% discount is applied. What is the final price?", "expected": "30"},
    {"input": "A tank holds 500 liters. It leaks 5 liters per hour. After 20 hours how many liters remain?", "expected": "400"},
    {"input": "Sarah saves $15 every week. How much will she save in 52 weeks?", "expected": "780"},
    {"input": "A pizza is cut into 8 equal slices. 3 people each eat 2 slices. How many slices are left?", "expected": "2"},
    {"input": "A car uses 6 liters of fuel per 100 km. How much fuel is needed for a 350 km trip?", "expected": "21"},
    {"input": "The sum of two numbers is 48 and their difference is 12. What is the larger number?", "expected": "30"},
    {"input": "A book has 320 pages. Mia reads 40 pages per day. In how many days will she finish?", "expected": "8"},
    {"input": "A school bus seats 45 students. How many buses are needed for 180 students?", "expected": "4"},
    {"input": "If 3x + 7 = 22, what is x?", "expected": "5"},
    {"input": "A square has a side of 9 cm. What is its area?", "expected": "81"},
    {"input": "Peter earns $18 per hour. He works 8 hours a day for 5 days. What is his weekly salary?", "expected": "720"},
    {"input": "A jar has 60 red and 40 blue marbles. What fraction of the marbles are red?", "expected": "3/5"},
    {"input": "A bicycle costs $250. You pay $70 upfront and the rest in 6 equal instalments. How much is each instalment?", "expected": "30"},
    {"input": "Temperature dropped from 15°C to -5°C. What is the total drop in temperature?", "expected": "20"},
    {"input": "Two friends share 3/4 of a cake equally. What fraction does each get?", "expected": "3/8"},
]

SQL_GENERATION_CASES = [
    {
        "input": "Get the names of all employees in the 'Sales' department from the employees table.",
        "expected_keywords": ["SELECT", "name", "employees", "WHERE", "department", "Sales"],
    },
    {
        "input": "Find the total number of orders placed by each customer from the orders table.",
        "expected_keywords": ["COUNT", "orders", "GROUP BY", "customer"],
    },
    {
        "input": "List all products whose price is greater than 100 from the products table.",
        "expected_keywords": ["SELECT", "products", "WHERE", "price", "100"],
    },
    {
        "input": "Get the top 5 highest-paid employees from the employees table.",
        "expected_keywords": ["SELECT", "employees", "ORDER BY", "salary", "DESC", "LIMIT", "5"],
    },
    {
        "input": "Find all customers who have not placed any orders. Use customers and orders tables.",
        "expected_keywords": ["LEFT JOIN", "NULL", "orders", "customers"],
    },
    {
        "input": "Calculate the average salary per department from the employees table.",
        "expected_keywords": ["AVG", "salary", "department", "GROUP BY"],
    },
    {
        "input": "Get the names and emails of customers who signed up after January 1, 2024.",
        "expected_keywords": ["SELECT", "name", "email", "WHERE", "2024"],
    },
    {
        "input": "Count the number of products in each category from the products table.",
        "expected_keywords": ["COUNT", "category", "GROUP BY", "products"],
    },
    {
        "input": "Find the most recent order date from the orders table.",
        "expected_keywords": ["MAX", "order_date", "orders"],
    },
    {
        "input": "List employees who earn more than the average salary of their department.",
        "expected_keywords": ["salary", "AVG", "department", "subquery"],
    },
    {
        "input": "Get all orders placed in the last 30 days from the orders table.",
        "expected_keywords": ["SELECT", "orders", "WHERE", "date", "INTERVAL", "30"],
    },
    {
        "input": "Find the second highest salary from the employees table.",
        "expected_keywords": ["salary", "LIMIT", "OFFSET", "ORDER BY", "DESC"],
    },
    {
        "input": "Update the price of product with id 55 to 199.99 in the products table.",
        "expected_keywords": ["UPDATE", "products", "SET", "price", "199.99", "WHERE", "id", "55"],
    },
    {
        "input": "Delete all orders older than 2 years from the orders table.",
        "expected_keywords": ["DELETE", "orders", "WHERE", "date"],
    },
    {
        "input": "Insert a new customer with name 'Alice', email 'alice@mail.com' into customers table.",
        "expected_keywords": ["INSERT", "customers", "VALUES", "Alice", "alice@mail.com"],
    },
    {
        "input": "Get product names and their category names by joining products and categories tables.",
        "expected_keywords": ["JOIN", "products", "categories", "category_id"],
    },
    {
        "input": "Find customers who have placed more than 5 orders using the orders table.",
        "expected_keywords": ["COUNT", "HAVING", "GROUP BY", "customer"],
    },
    {
        "input": "Get the total revenue for each month from the orders table where each order has an amount field.",
        "expected_keywords": ["SUM", "amount", "GROUP BY", "month", "MONTH"],
    },
    {
        "input": "Find all employees whose names start with the letter 'A'.",
        "expected_keywords": ["SELECT", "WHERE", "name", "LIKE", "A%"],
    },
    {
        "input": "Get the distinct job titles from the employees table.",
        "expected_keywords": ["DISTINCT", "job_title", "employees"],
    },
]

CODE_DEBUG_CASES = [
    {
        "input": """def sum_list(numbers):
    total = 0
    for i in range(len(numbers) + 1):
        total += numbers[i]
    return total""",
        "bug": "range(len(numbers) + 1) causes index out of bounds",
        "fix": "range(len(numbers))",
    },
    {
        "input": """def is_palindrome(s):
    return s == s.reverse()""",
        "bug": "str.reverse() does not exist in Python",
        "fix": "return s == s[::-1]",
    },
    {
        "input": """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n)""",
        "bug": "Infinite recursion — should be factorial(n-1)",
        "fix": "return n * factorial(n-1)",
    },
    {
        "input": """def divide(a, b):
    return a / b""",
        "bug": "No check for division by zero",
        "fix": "if b == 0: raise ValueError('Cannot divide by zero')",
    },
    {
        "input": """def find_max(lst):
    max_val = 0
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val""",
        "bug": "Initializing max_val to 0 fails for all-negative lists",
        "fix": "max_val = lst[0] or use float('-inf')",
    },
    {
        "input": """def count_vowels(s):
    count = 0
    for char in s:
        if char in 'aeiou':
            count += 1
    return count""",
        "bug": "Does not handle uppercase vowels",
        "fix": "if char.lower() in 'aeiou'",
    },
    {
        "input": """def binary_search(arr, target):
    left, right = 0, len(arr)
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "bug": "right should be len(arr) - 1 to avoid index out of bounds",
        "fix": "right = len(arr) - 1",
    },
    {
        "input": """def remove_duplicates(lst):
    seen = []
    for item in lst:
        if item not in seen:
            seen.append(item)
    return seen""",
        "bug": "Logic is correct but O(n²) — should use a set for O(n)",
        "fix": "Use seen = set()",
    },
    {
        "input": """def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32""",
        "bug": "No bug — but test if LLM correctly identifies it as correct",
        "fix": "No fix needed",
    },
    {
        "input": """def merge_dicts(d1, d2):
    for key, value in d2:
        d1[key] = value
    return d1""",
        "bug": "d2 should be iterated with .items()",
        "fix": "for key, value in d2.items()",
    },
    {
        "input": """def flatten(lst):
    result = []
    for item in lst:
        if type(item) == list:
            result.extend(flatten(item))
        else:
            result.append(item)
    return result""",
        "bug": "type(item) == list should be isinstance(item, list) for subclasses",
        "fix": "isinstance(item, list)",
    },
    {
        "input": """def calculate_average(scores):
    return sum(scores) / len(scores)""",
        "bug": "No handling for empty list — ZeroDivisionError",
        "fix": "if not scores: return 0",
    },
    {
        "input": """class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop(0)""",
        "bug": "pop(0) removes from the front, should be pop() for stack LIFO behavior",
        "fix": "return self.items.pop()",
    },
    {
        "input": """def word_count(sentence):
    words = sentence.split(' ')
    return len(words)""",
        "bug": "split(' ') fails for multiple spaces — should use split() with no args",
        "fix": "sentence.split()",
    },
    {
        "input": """def power(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result""",
        "bug": "Does not handle negative exponents",
        "fix": "if exp < 0: return 1 / power(base, -exp)",
    },
    {
        "input": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True""",
        "bug": "Correct but inefficient — should check up to sqrt(n)",
        "fix": "range(2, int(n**0.5) + 1)",
    },
    {
        "input": """def reverse_string(s):
    result = ''
    for i in range(len(s)):
        result = s[i] + result
    return result""",
        "bug": "Functionally correct but O(n²) due to string concatenation",
        "fix": "Use list and join, or return s[::-1]",
    },
    {
        "input": """import json
def load_config(path):
    with open(path) as f:
        return json.loads(f)""",
        "bug": "json.loads takes a string, should be json.load(f) for file objects",
        "fix": "return json.load(f)",
    },
    {
        "input": """def chunk_list(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size - 1)]""",
        "bug": "Step should be size, not size - 1 — causes overlapping chunks",
        "fix": "range(0, len(lst), size)",
    },
    {
        "input": """def truncate(text, max_len):
    if len(text) > max_len:
        return text[:max_len] + '...'
    return text""",
        "bug": "No handling for max_len <= 0",
        "fix": "if max_len <= 0: return '...'",
    },
]

TEXT_SUMMARIZATION_CASES = [
    {
        "input": "The Amazon rainforest, often referred to as the lungs of the Earth, produces about 20% of the world's oxygen. It covers over 5.5 million square kilometers and is home to 10% of all species on Earth. Deforestation has accelerated in recent decades due to agriculture, logging, and infrastructure development, threatening biodiversity and contributing to climate change.",
        "key_points": ["lungs of the Earth", "20% oxygen", "5.5 million km²", "10% species", "deforestation threat"],
    },
    {
        "input": "Artificial intelligence has transformed industries from healthcare to finance. Machine learning models now diagnose diseases with accuracy comparable to doctors, automate stock trading, and power recommendation engines. Despite these advances, ethical concerns around bias, privacy, and job displacement remain significant challenges.",
        "key_points": ["AI transforms industries", "disease diagnosis", "stock trading", "bias and privacy concerns"],
    },
    {
        "input": "The Great Wall of China stretches over 21,000 kilometers and was built over many centuries by various Chinese dynasties. Its primary purpose was military defense. Today it is a UNESCO World Heritage Site and one of the most visited tourist attractions in the world, drawing over 10 million visitors annually.",
        "key_points": ["21,000 km", "military defense", "UNESCO heritage", "10 million visitors"],
    },
    {
        "input": "Quantum computing uses qubits instead of classical bits, allowing computations to occur in superposition. This enables quantum computers to solve certain problems exponentially faster than classical computers. Applications include drug discovery, cryptography, and optimization problems. IBM and Google are leading the race to achieve quantum advantage.",
        "key_points": ["qubits", "superposition", "exponentially faster", "drug discovery cryptography", "IBM Google"],
    },
    {
        "input": "Sleep is essential for physical and mental health. During sleep, the brain consolidates memories, the body repairs tissues, and the immune system strengthens. Adults need 7-9 hours of sleep per night. Chronic sleep deprivation is linked to obesity, diabetes, cardiovascular disease, and cognitive decline.",
        "key_points": ["memory consolidation", "tissue repair", "7-9 hours", "sleep deprivation risks"],
    },
    {
        "input": "Climate change is causing global temperatures to rise at an unprecedented rate. The past decade has been the hottest on record, with consequences including rising sea levels, more frequent extreme weather events, and shifting ecosystems. International agreements like the Paris Accord aim to limit warming to 1.5°C above pre-industrial levels.",
        "key_points": ["temperatures rising", "hottest decade", "sea levels", "Paris Accord 1.5°C"],
    },
    {
        "input": "The human genome contains approximately 3 billion base pairs and around 20,000 protein-coding genes. The Human Genome Project, completed in 2003, mapped the entire genome. This has enabled advances in personalized medicine, genetic disease diagnosis, and gene therapies like CRISPR.",
        "key_points": ["3 billion base pairs", "20,000 genes", "Human Genome Project 2003", "personalized medicine CRISPR"],
    },
    {
        "input": "Social media platforms have fundamentally changed how people communicate and consume information. While they enable global connectivity and grassroots movements, they also spread misinformation rapidly and have been linked to increased anxiety and depression, especially among teenagers.",
        "key_points": ["global connectivity", "grassroots movements", "misinformation", "anxiety depression teenagers"],
    },
    {
        "input": "Electric vehicles are becoming increasingly mainstream as battery technology improves and charging infrastructure expands. EVs produce zero direct emissions and have lower lifetime operating costs than gasoline vehicles. Governments worldwide are setting targets to phase out internal combustion engines by 2035-2040.",
        "key_points": ["zero emissions", "lower operating costs", "battery technology", "phase out 2035-2040"],
    },
    {
        "input": "The microbiome refers to the trillions of microorganisms living in the human gut. These bacteria play critical roles in digestion, immune function, and even mental health through the gut-brain axis. Diet, antibiotics, and lifestyle significantly affect microbiome composition, with imbalances linked to conditions like IBS and depression.",
        "key_points": ["trillions of microorganisms", "digestion immune function", "gut-brain axis", "IBS depression"],
    },
    {
        "input": "Space exploration has expanded beyond government agencies with private companies like SpaceX, Blue Origin, and Virgin Galactic entering the field. SpaceX's Falcon 9 became the first orbital rocket to successfully land and be reused, dramatically reducing launch costs. The goal of human Mars colonization is now considered achievable within decades.",
        "key_points": ["private companies SpaceX", "reusable rocket Falcon 9", "lower launch costs", "Mars colonization"],
    },
    {
        "input": "The Renaissance was a cultural and intellectual movement that began in Italy in the 14th century and spread across Europe. It emphasized humanism, science, and the arts, producing figures like Leonardo da Vinci, Michelangelo, and Galileo. It marked the transition from the Middle Ages to the modern era.",
        "key_points": ["14th century Italy", "humanism science arts", "da Vinci Michelangelo Galileo", "Middle Ages to modern era"],
    },
    {
        "input": "Blockchain is a decentralized digital ledger that records transactions across a network of computers. It is the underlying technology behind cryptocurrencies like Bitcoin. Each block contains a cryptographic hash of the previous block, making the chain tamper-resistant. Applications extend to supply chain, healthcare records, and smart contracts.",
        "key_points": ["decentralized ledger", "Bitcoin", "cryptographic hash tamper-resistant", "supply chain smart contracts"],
    },
    {
        "input": "Meditation has been practiced for thousands of years and is increasingly validated by neuroscience. Regular practice reduces cortisol levels, improves focus and working memory, and can physically increase grey matter density in the prefrontal cortex. Even 10 minutes per day has measurable benefits on stress and attention.",
        "key_points": ["reduces cortisol", "improves focus memory", "grey matter prefrontal cortex", "10 minutes daily"],
    },
    {
        "input": "Ocean plastic pollution has reached crisis levels with an estimated 8 million metric tons entering oceans annually. The Great Pacific Garbage Patch spans an area twice the size of Texas. Microplastics have been found in human blood, fish tissue, and even Arctic ice, raising serious health and environmental concerns.",
        "key_points": ["8 million metric tons", "Great Pacific Garbage Patch", "microplastics in human blood", "environmental health risk"],
    },
    {
        "input": "5G networks promise speeds up to 100 times faster than 4G with ultra-low latency. This enables real-time communication for autonomous vehicles, remote surgery, and smart city infrastructure. However, the rollout requires dense installation of small cell towers and has faced resistance over health concerns and security risks.",
        "key_points": ["100x faster than 4G", "ultra-low latency", "autonomous vehicles remote surgery", "security concerns"],
    },
    {
        "input": "The opioid epidemic in the United States has claimed over 500,000 lives since 1999. It began with over-prescription of opioid painkillers, evolved to heroin, and now is driven largely by synthetic opioids like fentanyl. Government responses include naloxone distribution, prescription monitoring, and addiction treatment funding.",
        "key_points": ["500,000 deaths since 1999", "over-prescription", "fentanyl", "naloxone addiction treatment"],
    },
    {
        "input": "The Large Hadron Collider at CERN is the world's largest and most powerful particle accelerator. It discovered the Higgs boson in 2012, confirming a key prediction of the Standard Model of particle physics. Scientists use it to recreate conditions similar to just after the Big Bang.",
        "key_points": ["largest accelerator", "Higgs boson 2012", "Standard Model", "Big Bang conditions"],
    },
    {
        "input": "Urban farming is the practice of growing food within cities, using rooftops, vertical farms, and community gardens. It reduces food miles, increases access to fresh produce in food deserts, and can lower urban heat island effects. Advances in hydroponics and LED lighting have made year-round production viable.",
        "key_points": ["food miles reduction", "food deserts", "hydroponics LED", "year-round production"],
    },
    {
        "input": "The gig economy, characterized by short-term contracts and freelance work, has grown substantially with platforms like Uber, Fiverr, and Upwork. While it offers flexibility and income opportunities, it lacks traditional benefits like health insurance, paid leave, and job security, raising questions about worker rights.",
        "key_points": ["short-term contracts", "Uber Fiverr Upwork", "flexibility", "no benefits job security"],
    },
]

ALL_CASES = {
    "json_extraction": JSON_EXTRACTION_CASES,
    "math_word_problems": MATH_WORD_PROBLEM_CASES,
    "sql_generation": SQL_GENERATION_CASES,
    "code_debugging": CODE_DEBUG_CASES,
    "text_summarization": TEXT_SUMMARIZATION_CASES,
}
