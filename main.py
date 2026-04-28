import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('insurance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers 
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, address TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS policies 
                 (id INTEGER PRIMARY KEY, customer_id INTEGER, coverage REAL, premium REAL, 
                  status TEXT, valid_until DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments 
                 (id INTEGER PRIMARY KEY, policy_id INTEGER, amount REAL, date DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS claims 
                 (id INTEGER PRIMARY KEY, policy_id INTEGER, amount REAL, status TEXT, date DATE)''')
    conn.commit()
    return conn



class User:
    def __init__(self,user_id,name):
        self.user_id = user_id
        self.name = name

class Customer(User):
    def __init__(self,user_id,name,age,gender,address):
        super().__init__(user_id,name)
        self.age = age
        self.gender = gender
        self.address = address
        
    def raiseClaim(self):
        pass
        
    def renewPolicy(self):
        pass

class RiskEngine:
    def __init__(self,application_id,customer,coverage_amount,age_factor,coverage_factor,history_factor):
        self.application_id=application_id
        self.customer=customer
        self.coverage_amount=coverage_amount
        self.status="PENDING"
        
       
        self.pre_existing_conditions = coverage_factor 
        self.years_no_claim = history_factor
        self.premium = 0
        
    def calculate_premium(self):
        base_premium = self.coverage_amount * 0.05
        if self.customer.age <= 35:
            age_loading = 0
        elif self.customer.age <= 50:
            age_loading = base_premium * 0.5
        elif self.customer.age <= 65:
            age_loading = base_premium * 1.0
        else:
            age_loading = base_premium * 2.0
           
        pre_existing = 500 * self.pre_existing_conditions
        
        ncb_discount = min(self.years_no_claim * 0.05, 0.50)
        no_claim_bonus = base_premium * ncb_discount
        
        self.premium = base_premium + age_loading + pre_existing - no_claim_bonus
        return self.premium
        
    def scoreRisk(self):
        pass

class Application:
    
    def __init__(self, application_id, customer, coverage_amount, pre_existing, no_claim_years):
        self.application_id = application_id
        self.customer = customer
        self.coverage_amount = coverage_amount
        self.pre_existing = pre_existing
        self.no_claim_years = no_claim_years
        self.status = "PENDING"

class Policy:
    def __init__(self, policy_id, application, premium_schedule):
        self.policy_id = policy_id
        self.application = application
        self.premium_schedule = premium_schedule
        self.status = "ACTIVE"
        self.validity_start = datetime.now()
        self.validity_end = self.validity_start + timedelta(days=365)

    def activate(self):
        self.status = "ACTIVE"
    def lapse(self):
        self.status = "LAPSED"
    def renew(self):
        self.validity_end += timedelta(days=365)
    def surrender(self):
        self.status = "SURRENDERED"

class Underwriter(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.underwriter_id = None

    def assessRisk(self):
        pass
    def approve(self):
        pass
    def reject(self):
        pass

    def review_application(self, application):
       
        if application.customer.age >= 80:
            application.status = "REJECTED"
        else:
            application.status = "APPROVED"
            
        if application.status == "APPROVED":
            
            engine = RiskEngine(
                application.application_id, 
                application.customer, 
                application.coverage_amount, 0,
                application.pre_existing, 
                application.no_claim_years
            )
            premium_amount = engine.calculate_premium()
            
            schedule = [Premium("PRM-1", application.application_id, premium_amount)]
            policy = Policy(application.application_id, application, schedule)
            return policy, premium_amount
        else:
            return None, 0

class Payment:
    def __init__(self, payment_id, policy, amount):
        self.payment_id = payment_id
        self.policy = policy
        self.amount = amount
        self.payment_date = datetime.now()

class Claim:
    def __init__(self, claim_id, policy, claim_amount):
        self.claim_id = claim_id
        self.policy = policy
        self.claim_amount = claim_amount
        self.status = "PENDING"
        self.claim_date = datetime.now()
        
    def submit(self):
        pass
    def approve(self):
        self.status = "APPROVED"
    def reject(self):
        self.status = "REJECTED"
    def surrender(self):
        pass

class Premium:
    def __init__(self, premium_id, policy, amount):
        self.premium_id = premium_id
        self.policy = policy
        self.amount = amount
        self.premium_date = datetime.now()
        self.premium_status = "PENDING"
        self.dueDate = datetime.now() + timedelta(days=30)
        
    def pay(self):
        self.premium_status = "PAID"
    def markOverdue(self):
        self.premium_status = "OVERDUE"
    def applyGracePeriod(self):
        pass


def main():
    conn = init_db()
    c = conn.cursor()
    

    underwriter = Underwriter("U1", "Default Underwriter")
    
    while True:
        print("\n=== Simple Insurance System ===")
        print("1. Add Customer")
        print("2. Create Policy (Submit Application)")
        print("3. Pay Premium")
        print("4. File Claim")
        print("5. View All Policies")
        print("0. Exit")
        
        choice = input("Enter choice (0-5): ")
        
        if choice == '1':
            name = input("Name: ")
            age = int(input("Age: "))
            gender = input("Gender (M/F): ")
            address = input("Address: ")
            
            c.execute("INSERT INTO customers (name, age, gender, address) VALUES (?, ?, ?, ?)", 
                      (name, age, gender, address))
            conn.commit()
            
   
            new_cust = Customer(c.lastrowid, name, age, gender, address)
            print(f"--> Customer added successfully! Customer ID: {new_cust.user_id}")
            
        elif choice == '2':
            cust_id = int(input("Customer ID: "))
            
            c.execute("SELECT name, age, gender, address FROM customers WHERE id = ?", (cust_id,))
            result = c.fetchone()
            
            if not result:
                print("--> Error: Customer not found!")
                continue
                

            customer = Customer(cust_id, result[0], result[1], result[2], result[3])
            
            coverage = float(input("Coverage Amount: "))
            pre_existing = int(input("Number of pre-existing conditions: "))
            no_claim_years = int(input("Years of no claim: "))
            
          
            app_id = f"APP-{datetime.now().strftime('%H%M%S')}"
            application = Application(app_id, customer, coverage, pre_existing, no_claim_years)
            
    
            policy, premium_amount = underwriter.review_application(application)
            
            if policy is None:
                print("--> Application REJECTED due to high risk age.")
            else:
                c.execute('''INSERT INTO policies (customer_id, coverage, premium, status, valid_until) 
                             VALUES (?, ?, ?, ?, ?)''', 
                          (cust_id, coverage, premium_amount, policy.status, policy.validity_end.date()))
                conn.commit()
                policy.policy_id = c.lastrowid
                print(f"--> Policy created! Policy ID: {policy.policy_id} | Annual Premium: {premium_amount}")
            
        elif choice == '3':
            pol_id = int(input("Policy ID: "))
            amount = float(input("Payment Amount: "))
            
            
            payment = Payment(f"PAY-{datetime.now().strftime('%H%M%S')}", pol_id, amount)
            
            c.execute("INSERT INTO payments (policy_id, amount, date) VALUES (?, ?, ?)", 
                      (payment.policy_id, payment.amount, payment.payment_date.date()))
            conn.commit()
            print("--> Payment recorded successfully!")
            
        elif choice == '4':
            pol_id = int(input("Policy ID: "))
            amount = float(input("Claim Amount: "))
            
            claim = Claim(f"CLM-{datetime.now().strftime('%H%M%S')}", pol_id, amount)
            claim.approve() 
            
            c.execute("INSERT INTO claims (policy_id, amount, status, date) VALUES (?, ?, ?, ?)", 
                      (claim.policy, claim.claim_amount, claim.status, claim.claim_date.date()))
            conn.commit()
            print("--> Claim filed and auto-approved!")
            
        elif choice == '5':
            c.execute('''SELECT p.id, c.name, p.coverage, p.premium, p.status, p.valid_until 
                         FROM policies p 
                         JOIN customers c ON p.customer_id = c.id''')
            policies_data = c.fetchall()
            
            if not policies_data:
                print("--> No policies found.")
            else:
                for p in policies_data:
                    print(f"Policy ID: {p[0]} | Customer: {p[1]} | Coverage: {p[2]} | Premium: {p[3]:.2f} | Status: {p[4]} | Valid Until: {p[5]}")
                
        elif choice == '0':
            print("Goodbye!")
            break
            
        else:
            print("--> Invalid choice, please try again.")

if __name__ == '__main__':
    main()
