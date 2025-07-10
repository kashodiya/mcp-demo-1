import sqlite3
import random
import os
from datetime import datetime, timedelta
from database import init_database, get_db_connection

def seed_database():
    print("Starting database seeding...")
    
    # Delete existing database file
    if os.path.exists('bmo_data.db'):
        os.remove('bmo_data.db')
        print("Deleted existing database file")
    
    conn = None
    try:
        init_database()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM error_comments")
        cursor.execute("DELETE FROM validation_errors")
        cursor.execute("DELETE FROM reports")
        cursor.execute("DELETE FROM banks")
        cursor.execute("DELETE FROM users")
        
        # Seed users
        users = [
            ('analyst1', '123456', 'analyst'),
            ('analyst2', '123456', 'analyst'),
            ('analyst3', '123456', 'analyst'),
            ('analyst4', '123456', 'analyst'),
            ('analyst5', '123456', 'analyst'),
            ('analyst6', '123456', 'analyst'),
            ('analyst7', '123456', 'analyst'),
            ('analyst8', '123456', 'analyst'),
            ('analyst9', '123456', 'analyst'),
            ('analyst0', '123456', 'analyst'),
            ('supervisor', '123456', 'supervisor'),
            ('admin', '123456', 'admin'),
            ('reviewer', '123456', 'reviewer')
        ]
        
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)
        print(f"Seeded {len(users)} users")
        
        # Seed banks
        banks = [
            ('021000021', 'JPMorgan Chase Bank'),
            ('026009593', 'Bank of America'),
            ('121000248', 'Wells Fargo Bank'),
            ('111000025', 'Citibank'),
            ('036001808', 'Fifth Third Bank'),
            ('044000024', 'PNC Bank'),
            ('053000196', 'U.S. Bank'),
            ('122000247', 'Union Bank'),
            ('071000013', 'Regions Bank'),
            ('063100277', 'SunTrust Bank'),
            ('091000019', 'Ally Bank'),
            ('124003116', 'Capital One Bank'),
            ('031176110', 'HSBC Bank USA'),
            ('021001088', 'Santander Bank'),
            ('122105155', 'Silicon Valley Bank'),
            ('031100209', 'TD Bank'),
            ('021200025', 'M&T Bank'),
            ('043000096', 'KeyBank'),
            ('071923909', 'Comerica Bank'),
            ('122016066', 'First Republic Bank')
        ]
        
        cursor.executemany("INSERT INTO banks (aba_code, name) VALUES (?, ?)", banks)
        print(f"Seeded {len(banks)} banks")
        
        # Seed reports
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 6, 30)
        
        reports = []
        for i in range(30):
            bank_id = random.randint(1, 20)
            report_code = f"RPT-{2025}-{random.randint(1000, 9999)}"
            submission_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            has_errors = random.choice([True, False])
            is_accepted = None if has_errors else random.choice([True, False, None])
            
            reports.append((bank_id, report_code, submission_date.strftime('%Y-%m-%d'), has_errors, is_accepted))
        
        cursor.executemany("INSERT INTO reports (bank_id, report_code, submission_date, has_errors, is_accepted) VALUES (?, ?, ?, ?, ?)", reports)
        print(f"Seeded {len(reports)} reports")
        
        # Seed validation errors
        error_types = ['Data Format', 'Missing Field', 'Invalid Value', 'Calculation Error', 'Regulatory Compliance']
        field_names = ['total_assets', 'loan_amount', 'deposit_balance', 'interest_rate', 'customer_count']
        
        errors = []
        error_reports = cursor.execute("SELECT id FROM reports WHERE has_errors = 1").fetchall()
        
        for report in error_reports:
            num_errors = random.randint(1, 4)
            for _ in range(num_errors):
                error_type = random.choice(error_types)
                field_name = random.choice(field_names)
                error_message = f"{error_type} error in {field_name}: {random.choice(['Value exceeds limit', 'Required field missing', 'Invalid format', 'Calculation mismatch'])}"
                errors.append((report[0], error_type, error_message, field_name))
        
        cursor.executemany("INSERT INTO validation_errors (report_id, error_type, error_message, field_name) VALUES (?, ?, ?, ?)", errors)
        print(f"Seeded {len(errors)} validation errors")
        
        # Seed error comments
        comments = []
        all_errors = cursor.execute("SELECT id FROM validation_errors").fetchall()
        
        for error in random.sample(all_errors, min(len(all_errors), 25)):
            user_id = random.randint(1, 5)
            comment_text = random.choice([
                "This error needs immediate attention",
                "Bank has been notified to resubmit",
                "Similar error pattern observed in previous reports",
                "Escalating to supervisor for review",
                "Error resolved after bank clarification"
            ])
            comments.append((error[0], user_id, comment_text))
        
        cursor.executemany("INSERT INTO error_comments (error_id, user_id, comment) VALUES (?, ?, ?)", comments)
        print(f"Seeded {len(comments)} error comments")
        
        conn.commit()
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    seed_database()