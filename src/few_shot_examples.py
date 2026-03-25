"""
Few-shot examples per domain at three quality levels.
HIGH: Accurate, well-formed input-output pairs.
MEDIUM: Mostly correct but imprecise/incomplete outputs.
LOW: Wrong answers, bad formatting, misleading pairs.

We have 10 examples per domain per quality level.
The experiment will sample 1, 3, 5, or 10 from these.
"""

import random

# ─── JSON EXTRACTION ──────────────────────────────────────────────────────────

JSON_EXAMPLES = {
    "high": [
        {"input": "Alice, 30, is a nurse from Boston.", "output": '{"name": "Alice", "age": 30, "job": "nurse", "city": "Boston"}'},
        {"input": "Bob Chen is 25 and works as a designer in Seattle.", "output": '{"name": "Bob Chen", "age": 25, "job": "designer", "city": "Seattle"}'},
        {"input": "Order #1023 placed on June 5 for 2 units of Laptop Y at $800 each.", "output": '{"order_id": "1023", "date": "June 5", "quantity": 2, "item": "Laptop Y", "unit_price": 800}'},
        {"input": "Flight BA309 departs at 14:00 from London, arrives at 17:30 in Paris.", "output": '{"flight": "BA309", "departure": "14:00", "from": "London", "arrival": "17:30", "to": "Paris"}'},
        {"input": "Subscription Basic costs $9/month, includes 1 user and 10GB storage.", "output": '{"plan": "Basic", "monthly_price": 9, "users": 1, "storage_gb": 10}'},
        {"input": "Employee E-100, name Tom Hardy, department engineering, salary $90000.", "output": '{"employee_id": "E-100", "name": "Tom Hardy", "department": "engineering", "salary": 90000}'},
        {"input": "Car Toyota Camry year 2021, mileage 45000 km, color silver, price $22000.", "output": '{"model": "Toyota Camry", "year": 2021, "mileage_km": 45000, "color": "silver", "price": 22000}'},
        {"input": "Dr. Chen Lee teaches chemistry at Harvard. She has a PhD from Yale.", "output": '{"name": "Dr. Chen Lee", "subject": "chemistry", "university": "Harvard", "degree": "PhD", "degree_from": "Yale"}'},
        {"input": "Invoice INV-0091 for client DataCorp, total $1200, due May 15.", "output": '{"invoice_id": "INV-0091", "client": "DataCorp", "amount": 1200, "due_date": "May 15"}'},
        {"input": "Meeting on March 3 at 10am in Room A with the finance team.", "output": '{"date": "March 3", "time": "10am", "location": "Room A", "team": "finance"}'},
    ],
    "medium": [
        {"input": "Alice, 30, is a nurse from Boston.", "output": '{"name": "Alice", "age": "30", "job": "nurse"}'},
        {"input": "Bob Chen is 25 and works as a designer in Seattle.", "output": '{"name": "Bob", "job": "designer", "city": "Seattle"}'},
        {"input": "Order #1023 placed on June 5 for 2 units of Laptop Y at $800 each.", "output": '{"order": "1023", "quantity": 2, "item": "Laptop Y"}'},
        {"input": "Flight BA309 departs at 14:00 from London, arrives at 17:30 in Paris.", "output": '{"flight": "BA309", "from": "London", "to": "Paris"}'},
        {"input": "Subscription Basic costs $9/month, includes 1 user and 10GB storage.", "output": '{"plan": "Basic", "price": "$9/month", "users": 1}'},
        {"input": "Employee E-100, name Tom Hardy, department engineering, salary $90000.", "output": '{"name": "Tom Hardy", "department": "engineering"}'},
        {"input": "Car Toyota Camry year 2021, mileage 45000 km, color silver, price $22000.", "output": '{"model": "Toyota Camry", "year": "2021", "price": "$22000"}'},
        {"input": "Dr. Chen Lee teaches chemistry at Harvard.", "output": '{"name": "Dr. Chen Lee", "university": "Harvard"}'},
        {"input": "Invoice INV-0091 for client DataCorp, total $1200, due May 15.", "output": '{"invoice": "INV-0091", "amount": "$1200"}'},
        {"input": "Meeting on March 3 at 10am in Room A with the finance team.", "output": '{"date": "March 3", "time": "10am"}'},
    ],
    "low": [
        {"input": "Alice, 30, is a nurse from Boston.", "output": "Alice is a nurse. She is 30 years old."},
        {"input": "Bob Chen is 25 and works as a designer in Seattle.", "output": '{"name": "Bob", "age": "twenty five"}'},
        {"input": "Order #1023 placed on June 5 for 2 units of Laptop Y at $800 each.", "output": "Order number 1023, June, laptops, 800 dollars"},
        {"input": "Flight BA309 departs at 14:00 from London, arrives at 17:30 in Paris.", "output": '{"flight_number": "BA-309", "departure_time": "2pm", "destination": "France"}'},
        {"input": "Subscription Basic costs $9/month, includes 1 user and 10GB storage.", "output": "Basic plan, nine dollars, storage"},
        {"input": "Employee E-100, name Tom Hardy, department engineering, salary $90000.", "output": '{"id": 100, "dept": "eng", "pay": "90k"}'},
        {"input": "Car Toyota Camry year 2021, mileage 45000 km, color silver, price $22000.", "output": "Toyota 2021 silver car 22000"},
        {"input": "Dr. Chen Lee teaches chemistry at Harvard.", "output": '{"professor": "Chen", "teaches": "Harvard"}'},
        {"input": "Invoice INV-0091 for client DataCorp, total $1200, due May 15.", "output": "invoice for datacorp, 1200 dollars"},
        {"input": "Meeting on March 3 at 10am in Room A with the finance team.", "output": '{"meeting": "yes", "room": "A"}'},
    ],
}

# ─── MATH WORD PROBLEMS ───────────────────────────────────────────────────────

MATH_EXAMPLES = {
    "high": [
        {"input": "A bag has 5 red and 3 blue balls. How many balls total?", "output": "Step 1: Total = red + blue = 5 + 3 = 8\nFinal Answer: 8"},
        {"input": "A book costs $12. Buy 4 books. Total cost?", "output": "Step 1: Total = 12 × 4 = 48\nFinal Answer: 48"},
        {"input": "A train goes 50 km/h for 3 hours. Distance?", "output": "Step 1: Distance = speed × time = 50 × 3 = 150\nFinal Answer: 150"},
        {"input": "20% discount on a $50 item. Final price?", "output": "Step 1: Discount = 20% of 50 = 10\nStep 2: Price = 50 - 10 = 40\nFinal Answer: 40"},
        {"input": "Class has 40 students. 25% are absent. How many present?", "output": "Step 1: Absent = 25% of 40 = 10\nStep 2: Present = 40 - 10 = 30\nFinal Answer: 30"},
        {"input": "Sum of two numbers is 20, difference is 4. Larger number?", "output": "Step 1: x + y = 20, x - y = 4\nStep 2: 2x = 24, x = 12\nFinal Answer: 12"},
        {"input": "A worker earns $15/hour. Works 8 hours. Daily wage?", "output": "Step 1: Wage = 15 × 8 = 120\nFinal Answer: 120"},
        {"input": "Rectangle length 10m, width 4m. Area?", "output": "Step 1: Area = length × width = 10 × 4 = 40\nFinal Answer: 40"},
        {"input": "6 friends share a $90 bill equally. Each pays?", "output": "Step 1: Each = 90 ÷ 6 = 15\nFinal Answer: 15"},
        {"input": "A bottle has 1.5 liters. Pour 300ml. Remaining in liters?", "output": "Step 1: 1.5L = 1500ml\nStep 2: 1500 - 300 = 1200ml = 1.2L\nFinal Answer: 1.2"},
    ],
    "medium": [
        {"input": "A bag has 5 red and 3 blue balls. How many balls total?", "output": "8 balls total"},
        {"input": "A book costs $12. Buy 4 books. Total cost?", "output": "$48"},
        {"input": "A train goes 50 km/h for 3 hours. Distance?", "output": "150 km"},
        {"input": "20% discount on a $50 item. Final price?", "output": "$40"},
        {"input": "Class has 40 students. 25% are absent. How many present?", "output": "30 students"},
        {"input": "Sum of two numbers is 20, difference is 4. Larger number?", "output": "12"},
        {"input": "A worker earns $15/hour. Works 8 hours. Daily wage?", "output": "$120"},
        {"input": "Rectangle length 10m, width 4m. Area?", "output": "40 square meters"},
        {"input": "6 friends share a $90 bill equally. Each pays?", "output": "15"},
        {"input": "A bottle has 1.5 liters. Pour 300ml. Remaining in liters?", "output": "1.2 liters"},
    ],
    "low": [
        {"input": "A bag has 5 red and 3 blue balls. How many balls total?", "output": "5"},
        {"input": "A book costs $12. Buy 4 books. Total cost?", "output": "16"},
        {"input": "A train goes 50 km/h for 3 hours. Distance?", "output": "53"},
        {"input": "20% discount on a $50 item. Final price?", "output": "10"},
        {"input": "Class has 40 students. 25% are absent. How many present?", "output": "10"},
        {"input": "Sum of two numbers is 20, difference is 4. Larger number?", "output": "16"},
        {"input": "A worker earns $15/hour. Works 8 hours. Daily wage?", "output": "23"},
        {"input": "Rectangle length 10m, width 4m. Area?", "output": "28"},
        {"input": "6 friends share a $90 bill equally. Each pays?", "output": "84"},
        {"input": "A bottle has 1.5 liters. Pour 300ml. Remaining in liters?", "output": "0.3"},
    ],
}

# ─── SQL GENERATION ───────────────────────────────────────────────────────────

SQL_EXAMPLES = {
    "high": [
        {"input": "Get all users from the users table.", "output": "SELECT * FROM users;"},
        {"input": "Find employees with salary above 50000.", "output": "SELECT * FROM employees WHERE salary > 50000;"},
        {"input": "Count total orders in the orders table.", "output": "SELECT COUNT(*) FROM orders;"},
        {"input": "Get names of customers in New York.", "output": "SELECT name FROM customers WHERE city = 'New York';"},
        {"input": "Find the maximum age from the users table.", "output": "SELECT MAX(age) FROM users;"},
        {"input": "Get distinct job titles from employees.", "output": "SELECT DISTINCT job_title FROM employees;"},
        {"input": "Find products with price between 10 and 50.", "output": "SELECT * FROM products WHERE price BETWEEN 10 AND 50;"},
        {"input": "Count customers grouped by country.", "output": "SELECT country, COUNT(*) AS customer_count FROM customers GROUP BY country;"},
        {"input": "Get the 10 most recent orders.", "output": "SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;"},
        {"input": "Update user with id 5 to have email 'new@mail.com'.", "output": "UPDATE users SET email = 'new@mail.com' WHERE id = 5;"},
    ],
    "medium": [
        {"input": "Get all users from the users table.", "output": "select * from users"},
        {"input": "Find employees with salary above 50000.", "output": "SELECT * FROM employees where salary > 50000"},
        {"input": "Count total orders in the orders table.", "output": "select count(*) from orders"},
        {"input": "Get names of customers in New York.", "output": "SELECT name from customers WHERE city = New York"},
        {"input": "Find the maximum age from the users table.", "output": "select max(age) from users"},
        {"input": "Get distinct job titles from employees.", "output": "SELECT DISTINCT job_title from employees"},
        {"input": "Find products with price between 10 and 50.", "output": "select * from products where price > 10 and price < 50"},
        {"input": "Count customers grouped by country.", "output": "select country, count(*) from customers group by country"},
        {"input": "Get the 10 most recent orders.", "output": "select * from orders order by order_date desc limit 10"},
        {"input": "Update user with id 5 to have email 'new@mail.com'.", "output": "update users set email = new@mail.com where id = 5"},
    ],
    "low": [
        {"input": "Get all users from the users table.", "output": "SHOW users;"},
        {"input": "Find employees with salary above 50000.", "output": "GET employees salary 50000"},
        {"input": "Count total orders in the orders table.", "output": "count orders"},
        {"input": "Get names of customers in New York.", "output": "SELECT * FROM customers WHERE New York"},
        {"input": "Find the maximum age from the users table.", "output": "SELECT age FROM users ORDER BY age"},
        {"input": "Get distinct job titles from employees.", "output": "SELECT job_title FROM employees"},
        {"input": "Find products with price between 10 and 50.", "output": "SELECT * FROM products"},
        {"input": "Count customers grouped by country.", "output": "SELECT country FROM customers"},
        {"input": "Get the 10 most recent orders.", "output": "SELECT * FROM orders LIMIT 10"},
        {"input": "Update user with id 5 to have email 'new@mail.com'.", "output": "INSERT INTO users email = 'new@mail.com'"},
    ],
}

# ─── CODE DEBUGGING ───────────────────────────────────────────────────────────

CODE_EXAMPLES = {
    "high": [
        {"input": "def add(a, b):\n    return a - b", "output": "BUG: Subtraction used instead of addition.\nFIX: return a + b"},
        {"input": "for i in range(1, 10):\n    print(i)", "output": "BUG: Range ends at 9, not 10. If 10 is required use range(1, 11).\nFIX: for i in range(1, 11): if inclusive of 10 is intended."},
        {"input": "lst = [1,2,3]\nprint(lst[3])", "output": "BUG: Index 3 is out of bounds for a list of length 3 (valid indices 0-2).\nFIX: print(lst[2]) or access within bounds."},
        {"input": "def greet(name):\n    print('Hello ' + name + '!')\ngreet()", "output": "BUG: Function called with no argument but requires 'name'.\nFIX: greet('World') or add a default: def greet(name='World')."},
        {"input": "x = '5'\ny = x + 3", "output": "BUG: TypeError — cannot add string and integer.\nFIX: y = int(x) + 3"},
        {"input": "def square(n):\n    return n * n\nprint(square)", "output": "BUG: Function is not called — just referenced.\nFIX: print(square(5)) — provide an argument."},
        {"input": "d = {'a': 1}\nprint(d['b'])", "output": "BUG: KeyError — key 'b' does not exist in the dictionary.\nFIX: print(d.get('b', 'default'))"},
        {"input": "while True:\n    x = int(input())\n    if x = 0:\n        break", "output": "BUG: Assignment operator = used inside if condition instead of == (equality check).\nFIX: if x == 0:"},
        {"input": "def double(n):\n    n * 2", "output": "BUG: Missing return statement — function returns None.\nFIX: return n * 2"},
        {"input": "nums = [3, 1, 4, 1, 5]\nnums.sort\nprint(nums)", "output": "BUG: sort is referenced but not called — missing parentheses.\nFIX: nums.sort()"},
    ],
    "medium": [
        {"input": "def add(a, b):\n    return a - b", "output": "Should use + not -. Fix: return a + b"},
        {"input": "lst = [1,2,3]\nprint(lst[3])", "output": "Index error, list only has 3 elements. Fix: use lst[2]"},
        {"input": "x = '5'\ny = x + 3", "output": "Can't add string and int. Fix: int(x) + 3"},
        {"input": "def greet(name):\n    print('Hello ' + name)\ngreet()", "output": "Missing argument. Pass a name when calling."},
        {"input": "def double(n):\n    n * 2", "output": "No return statement. Add return."},
        {"input": "d = {'a': 1}\nprint(d['b'])", "output": "Key b doesn't exist. Use .get() instead."},
        {"input": "while True:\n    x = int(input())\n    if x = 0:\n        break", "output": "Should use == not = in if statement."},
        {"input": "def square(n):\n    return n * n\nprint(square)", "output": "Missing parentheses in function call."},
        {"input": "nums = [3,1,4]\nnums.sort\nprint(nums)", "output": "sort needs parentheses: nums.sort()"},
        {"input": "for i in range(1, 10):\n    print(i)", "output": "Range goes to 9 not 10."},
    ],
    "low": [
        {"input": "def add(a, b):\n    return a - b", "output": "The code looks fine"},
        {"input": "lst = [1,2,3]\nprint(lst[3])", "output": "Use lst[4] instead"},
        {"input": "x = '5'\ny = x + 3", "output": "Change x to 5.0"},
        {"input": "def greet(name):\n    print('Hello ' + name)\ngreet()", "output": "Works fine as is"},
        {"input": "def double(n):\n    n * 2", "output": "Change n * 2 to n + n"},
        {"input": "d = {'a': 1}\nprint(d['b'])", "output": "Add b to the print statement"},
        {"input": "while True:\n    if x = 0:\n        break", "output": "Remove the if statement"},
        {"input": "def square(n):\n    return n * n\nprint(square)", "output": "square is correct"},
        {"input": "nums = [3,1,4]\nnums.sort\nprint(nums)", "output": "Already sorted"},
        {"input": "for i in range(1, 10):\n    print(i)", "output": "Correct, prints 1 to 10"},
    ],
}

# ─── TEXT SUMMARIZATION ───────────────────────────────────────────────────────

SUMMARIZATION_EXAMPLES = {
    "high": [
        {
            "input": "The sun is a star at the center of our solar system. It provides heat and light that sustains life on Earth. Scientists estimate the sun is about 4.6 billion years old.",
            "output": "The sun, a 4.6-billion-year-old star, is central to our solar system and provides the heat and light necessary to sustain life on Earth."
        },
        {
            "input": "Coffee is one of the world's most popular beverages. It contains caffeine, which stimulates the central nervous system. Studies show moderate consumption can reduce risk of type 2 diabetes.",
            "output": "Coffee, widely consumed globally, contains caffeine that stimulates the nervous system, and moderate intake has been associated with a reduced risk of type 2 diabetes."
        },
        {
            "input": "Mount Everest is the highest peak on Earth at 8,849 meters. It lies on the Nepal-Tibet border. Thousands of climbers have attempted to summit it since Edmund Hillary first reached the top in 1953.",
            "output": "Mount Everest, standing at 8,849 meters on the Nepal-Tibet border, is Earth's highest peak; since Edmund Hillary's first ascent in 1953, thousands of climbers have attempted the summit."
        },
        {
            "input": "Electric cars run on battery-powered motors rather than combustion engines. They emit no direct pollutants and are cheaper to operate. Adoption is rising as battery range and charging infrastructure improve.",
            "output": "Electric cars use battery-powered motors, producing no direct emissions and lower operating costs; their adoption is growing as battery technology and charging infrastructure continue to improve."
        },
        {
            "input": "The internet transformed global communication by enabling instant information exchange. E-commerce, social media, and remote work all depend on it. Today over 5 billion people are connected online.",
            "output": "The internet has fundamentally changed global communication and enabled e-commerce, social media, and remote work; over 5 billion people worldwide are now connected online."
        },
        {
            "input": "Honey bees are vital pollinators responsible for fertilizing many crops humans rely on. Colony collapse disorder has reduced bee populations significantly since 2006. Pesticides and habitat loss are key contributing factors.",
            "output": "Honey bees are essential crop pollinators, but their populations have declined sharply since 2006 due to colony collapse disorder driven primarily by pesticide exposure and habitat destruction."
        },
        {
            "input": "The printing press, invented by Gutenberg around 1440, made books widely available for the first time. It accelerated the spread of literacy and was central to the Renaissance and Reformation.",
            "output": "Gutenberg's printing press, invented around 1440, democratized access to books, significantly boosted literacy rates, and played a pivotal role in both the Renaissance and Reformation."
        },
        {
            "input": "Yoga originated in ancient India and combines physical postures, breathing exercises, and meditation. It has been shown to reduce stress and improve flexibility. It now has over 300 million practitioners worldwide.",
            "output": "Yoga, an ancient Indian practice integrating postures, breathing, and meditation, has proven benefits for stress reduction and flexibility, and today is practiced by over 300 million people globally."
        },
        {
            "input": "Dark matter is a hypothetical form of matter that does not emit light or energy. It is thought to make up about 27% of the universe. Scientists infer its existence through its gravitational effects on visible matter.",
            "output": "Dark matter, believed to constitute approximately 27% of the universe, is a hypothetical substance that emits no light and is detected only through its gravitational influence on visible matter."
        },
        {
            "input": "Antibiotics are drugs that kill or inhibit bacteria. They have saved millions of lives since penicillin was discovered in 1928. However, overuse has led to antibiotic-resistant bacteria, a growing global health threat.",
            "output": "Antibiotics, life-saving drugs since penicillin's 1928 discovery, are now threatened by widespread resistance caused by overuse, posing an escalating global public health crisis."
        },
    ],
    "medium": [
        {"input": "The sun is a star providing heat and light. It is 4.6 billion years old.", "output": "The sun is an old star that gives us heat and light."},
        {"input": "Coffee contains caffeine and may reduce diabetes risk with moderate use.", "output": "Coffee has caffeine and can be good for health in moderation."},
        {"input": "Mount Everest is 8,849 meters high on the Nepal-Tibet border.", "output": "Everest is the tallest mountain and was first climbed in 1953."},
        {"input": "Electric cars use batteries and are cheaper to operate than gas cars.", "output": "EVs don't pollute and are getting more popular."},
        {"input": "The internet connects over 5 billion people and enables e-commerce and remote work.", "output": "The internet changed how people communicate and work."},
        {"input": "Honey bees are pollinators declining due to pesticides and habitat loss.", "output": "Bees are important but their numbers are falling."},
        {"input": "The printing press made books widely available and boosted literacy.", "output": "Gutenberg's press spread literacy and helped the Renaissance."},
        {"input": "Yoga reduces stress and improves flexibility with 300 million practitioners.", "output": "Yoga is a popular practice from India that is good for health."},
        {"input": "Dark matter is 27% of the universe and detected through gravity.", "output": "Dark matter is mysterious and makes up much of the universe."},
        {"input": "Antibiotics fight bacteria but overuse causes resistance.", "output": "Antibiotics save lives but resistance is a problem now."},
    ],
    "low": [
        {"input": "The sun is a star providing heat and light. It is 4.6 billion years old.", "output": "Sun is hot and bright."},
        {"input": "Coffee contains caffeine and may reduce diabetes risk.", "output": "Coffee is a drink people like."},
        {"input": "Mount Everest is 8,849 meters high and was first climbed in 1953.", "output": "Everest is very big."},
        {"input": "Electric cars use batteries and produce no emissions.", "output": "Cars run on electricity maybe."},
        {"input": "The internet connects 5 billion people and enabled e-commerce.", "output": "Internet is everywhere."},
        {"input": "Honey bees are vital pollinators declining due to pesticides.", "output": "Bees make honey."},
        {"input": "The printing press boosted literacy and fueled the Renaissance.", "output": "Books were made by a machine."},
        {"input": "Yoga reduces stress and has 300 million practitioners worldwide.", "output": "Yoga is exercise."},
        {"input": "Dark matter is 27% of the universe and detected via gravity.", "output": "Dark matter is dark."},
        {"input": "Antibiotics kill bacteria but resistance is growing.", "output": "Antibiotics are medicine."},
    ],
}

ALL_EXAMPLES = {
    "json_extraction": JSON_EXAMPLES,
    "math_word_problems": MATH_EXAMPLES,
    "sql_generation": SQL_EXAMPLES,
    "code_debugging": CODE_EXAMPLES,
    "text_summarization": SUMMARIZATION_EXAMPLES,
}


def get_examples(domain: str, quality: str, n: int, seed: int = 42) -> list:
    """Return n examples for the given domain and quality level."""
    pool = ALL_EXAMPLES[domain][quality]
    rng = random.Random(seed)
    if n >= len(pool):
        return pool
    return rng.sample(pool, n)
