            SIMPLE INSURANCE SYSTEM - UC - 014

Problem Statement:

I am going to design a simple insurance management system that is easily accessible by the users via a command-line interface.

The system has 3 main actors they are,
--> Customer
--> Underwriter (Admin)
--> Risk Engine (System)

Approach & Logic used:

Tech Stacks used :

Frontend --
* Command Line Interface (CLI)
* Python standard I/O

Backend --
* Python

Database --
* SQLite3

Flow :

Customer --

The user registers as a customer by providing their name, age, gender, and address.

The customer submits an application to create a policy by entering their coverage amount, pre-existing conditions, and years without claims.

The system assesses the risk:

If the customer's age is 80 or above, the application is automatically rejected.

Premium is calculated dynamically based on base coverage, age factor, pre-existing conditions, and a no-claim bonus.

Once approved, the policy becomes active and the customer can pay their generated premium.

The customer can file a claim against their active policy.

In the current flow, filed claims are automatically approved and recorded.

Customers and Admins can view a consolidated list of all active policies, showing coverage, premium amounts, and valid-until dates.

Underwriter (Admin) --

Reviews applications and assesses risk based on customer age.

Approves or rejects applications automatically during the policy creation flow.

System (Risk Engine) --

Calculates the exact premium by applying specific financial logic (age loading, NCB, pre-existing penalties).

Generates policy records, schedules premium payments, and tracks expiration dates (valid for 365 days).

Tables / Classes used:

Customer - id, name, age, gender, address -- raiseClaim(), renewPolicy()

Policy / Application - id, customer_id, coverage, premium, status, valid_until -- activate(), lapse(), renew(), surrender()

Payment - id, policy_id, amount, date -- pay(), markOverdue()

Claim - id, policy_id, amount, status, date -- submit(), approve(), reject()

RiskEngine - application_id, customer, coverage_amount, pre_existing_conditions, years_no_claim -- calculate_premium(), scoreRisk()

Underwriting & Premium Policy:

Base Premium - 5% of Coverage Amount
Age <= 35 - No additional loading
Age 36-50 - 50% of base premium added
Age 51-65 - 100% of base premium added
Age > 65  - 200% of base premium added
Pre-existing Conditions - 500 flat fee per condition added
No Claim Bonus (NCB) - 5% discount per year (Maximum cap at 50% discount)
Age >= 80 - Auto-Rejected


How to run the code :

* directly run -- main.py 
	code:
		python main.py