import datetime
import bcrypt
import random
from faker import Faker
from database import get_users_collection, get_mongo_client

def hash_pw(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def main():
    client = get_mongo_client()
    db = client["clinical_db"]
    users_coll = db["users"]
    patients_coll = db["patients"]
    summaries_coll = db["summaries"]
    
    # Clear existing data
    users_coll.delete_many({})
    patients_coll.delete_many({})
    summaries_coll.delete_many({})
    print("Cleared existing users, patients, and summaries from the database.")
    
    fake = Faker()
    
    # 1. Users
    roles = ["Clinical", "Research", "Administrative", "Legal"]
    docs_to_insert = []
    
    for role in roles:
        doc = {
            "username": f"{role.lower()}_user",
            "password": hash_pw(f"{role.lower()}123"),
            "role": role,
            "full_name": fake.name()
        }
        docs_to_insert.append(doc)
    
    users_coll.insert_many(docs_to_insert)
    
    # 2. Patients
    patients = []
    for _ in range(10):
        patients.append({
            "patient_id": fake.bothify(text='P-#####-?').upper(),
            "patient_name": fake.name(),
            "age": fake.random_int(min=5, max=95),
            "disease": fake.word().capitalize(),
            "medication": fake.word().capitalize(),
            "billing_info": fake.credit_card_provider(),
            "contact_no": fake.phone_number(),
            "isVerified": fake.boolean()
        })
    
    if patients:
        patients_coll.insert_many(patients)

    # 3. Summaries
    context_purposes = {
        "Clinical": ["Treatment", "Routine Checkup", "Consultation"],
        "Research": ["Cohort Study", "Clinical Trial", "Epidemiological Study"],
        "Administrative": ["Insurance Verification", "Billing Issue", "Scheduling"],
        "Legal": ["Subpoena Response", "Court Order", "Internal Audit"]
    }
    
    summaries = []
    for p in patients:
        for _ in range(random.randint(2, 3)):
            context = random.choice(roles)
            purpose = random.choice(context_purposes[context])
            
            # For timezone-aware UTC datetime
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            
            summaries.append({
                "Patient_ID": p["patient_id"],
                "Content_Data": fake.paragraph(nb_sentences=3),
                "Context_Type": context,
                "Purpose_Name": purpose,
                "Generated_Timestamp": now_utc.isoformat()
            })
            
    if summaries:
        summaries_coll.insert_many(summaries)
        
    print(f"\nInserted {len(roles)} test users, {len(patients)} mock patients, and {len(summaries)} mock summaries.\n")
    print("-" * 50)
    print(f"{'Role':<15} | {'Username':<15} | {'Password'}")
    print("-" * 50)
    for role in roles:
        print(f"{role:<15} | {role.lower()}_user   | {role.lower()}123")
    print("-" * 50)

if __name__ == "__main__":
    main()
