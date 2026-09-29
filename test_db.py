from database.db import get_connection, init_db

# 1. Initialize DB tables
init_db()

# 2. Try inserting a sample policy manually
conn = get_connection()
cursor = conn.cursor()

# Ensure user 1 exists
cursor.execute("INSERT OR IGNORE INTO users (id, full_name, email, password_hash, phone_number, emergency_contact) VALUES (1, 'Test User', 'test@example.com', 'pass', '123', '456')")

# Insert test policy
cursor.execute("""
    INSERT OR REPLACE INTO insurance_policies (user_id, policy_provider, policy_number, coverage_type, claim_limit, status, expiry_date)
    VALUES (1, 'HDFC ERGO TEST', 'POL-12345', 'Comprehensive', '₹1,50,000', 'Active', '2027-01-01')
""")
conn.commit()

# 3. Read back from database
cursor.execute("SELECT * FROM insurance_policies WHERE user_id = 1")
rows = cursor.fetchall()

print("--- POLICIES FOUND IN DATABASE ---")
for r in rows:
    print(dict(r))
conn.close()