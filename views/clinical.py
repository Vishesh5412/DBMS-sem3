import streamlit as st
from database import get_mongo_client
from bson.objectid import ObjectId

def get_patients_collection():
    return get_mongo_client()["clinical_db"]["patients"]

def get_summaries_collection():
    return get_mongo_client()["clinical_db"]["summaries"]

def view_patient_context():
    st.title("Patient Context")
    
    patients_coll = get_patients_collection()
    summaries_coll = get_summaries_collection()

    st.markdown("### Real-time Patient Lookup")
    entered_patient_id = st.text_input("Enter Patient ID (e.g., P-12345-X)")

    if entered_patient_id:
        # Prevent data leakage by explicitly selecting safe columns at the DB level
        patient_projection = {
            "_id": 0,
            "patient_name": 1,
            "age": 1,
            "disease": 1,
            "medication": 1,
            "patient_id": 1  # Required for summaries link mapped earlier
        }
        
        # Querying securely using native MongoDB via entered Patient ID in real-time
        patient = patients_coll.find_one({"patient_id": entered_patient_id}, patient_projection)
        
        if patient:
            st.subheader("Patient Information")
            
            st.markdown(f"**Name:** {patient.get('patient_name', 'N/A')}")
            st.markdown(f"**Age:** {patient.get('age', 'N/A')}")
            st.markdown(f"**Disease:** {patient.get('disease', 'N/A')}")
            st.markdown(f"**Medication:** {patient.get('medication', 'N/A')}")
                
            st.markdown("---")
            st.subheader("Clinical Summaries")
            
            # Strict Context Filtering & Projection
            summary_projection = {
                "_id": 0,
                "Content_Data": 1,
                "Purpose_Name": 1,
                "Generated_Timestamp": 1
            }
            
            selected_patient_string_id = patient.get("patient_id")
            
            clinical_summaries = list(summaries_coll.find({
                "Patient_ID": selected_patient_string_id,
                "Context_Type": "Clinical"
            }, summary_projection))
            
            # Display Summaries
            if clinical_summaries:
                for summary in clinical_summaries:
                    purpose = summary.get("Purpose_Name", "General")
                    timestamp = summary.get("Generated_Timestamp")
                    
                    title = f"Summary: {purpose}"
                    if timestamp:
                        title += f" ({timestamp})"
                        
                    with st.expander(title, expanded=True):
                        st.markdown(summary.get("Content_Data", "No content available."))
            else:
                st.info("No clinical summaries found for this patient.")
        else:
            st.error(f"Patient record for ID '{entered_patient_id}' not found.")

def view_generate_summary():
    st.title("Generate Summary")
    
    st.markdown("### Generate Referral")
    entered_patient_id = st.text_input("Enter Patient ID for Referral (e.g., P-12345-X)")
    
    # Referral Action
    if st.button("Generate Referral-Specific Summary"):
        if entered_patient_id:
            patients_coll = get_patients_collection()
            patient = patients_coll.find_one({"patient_id": entered_patient_id}, {"_id": 0, "patient_name": 1, "disease": 1, "medication": 1})
            
            if patient:
                patient_name = patient.get("patient_name", "The patient")
                disease = patient.get("disease", "an unspecified condition")
                medication = patient.get("medication", "no active medication")
                
                st.success("Successfully generated referral summary.")
                narrative = (
                    f"**Referral Draft for {entered_patient_id}:**\n\n"
                    f"Dear Specialist,\n\n"
                    f"{patient_name} is presenting with {disease}, exhibiting symptoms and biological indicators consistent "
                    f"with recent metabolic and risk panels. Current disease management includes {medication}. "
                    f"I am referring this patient for further rigorous clinical workup and continued specialist monitoring."
                )
                st.markdown(narrative)
            else:
                st.error(f"Patient record for ID '{entered_patient_id}' not found. Cannot synthesize referral.")
        else:
            st.warning("Please enter a valid Patient ID to generate the referral.")
