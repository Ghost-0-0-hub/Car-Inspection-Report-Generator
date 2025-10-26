import streamlit as st
from fpdf import FPDF
import traceback
from transformers import pipeline  # 🧠 AI summarization

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Car Inspection Form",
    page_icon="🚘",
    layout="wide"
)
st.title("🚘 Car Inspection Form")

# --- FORM SECTIONS ---
with st.expander("Basic Information", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        owner_name = st.text_input("Owner Name").strip()
    with col2:
        car_model = st.text_input("Car Model").strip()
    with col3:
        car_year = st.number_input("Year", min_value=1980, max_value=2030, step=1)
    license_plate = st.text_input("License Plate").strip()

with st.expander("Engine & Transmission"):
    col1, col2, col3 = st.columns(3)
    with col1:
        engine_condition = st.selectbox("Engine Condition", ["Excellent", "Good", "Average", "Poor"])
    with col2:
        transmission_condition = st.selectbox("Transmission Condition", ["Excellent", "Good", "Average", "Poor"])
    with col3:
        oil_leaks = st.radio("Oil Leaks?", ["Yes", "No"])

with st.expander("Brakes & Suspension"):
    col1, col2, col3 = st.columns(3)
    with col1:
        brakes_condition = st.selectbox("Brakes Condition", ["Excellent", "Good", "Average", "Poor"])
    with col2:
        suspension_condition = st.selectbox("Suspension Condition", ["Excellent", "Good", "Average", "Poor"])
    with col3:
        steering_condition = st.selectbox("Steering Condition", ["Excellent", "Good", "Average", "Poor"])

with st.expander("Tires & Wheels"):
    col1, col2 = st.columns(2)
    with col1:
        tire_condition = st.selectbox("Tire Condition", ["Excellent", "Good", "Average", "Poor"])
    with col2:
        wheel_condition = st.selectbox("Wheel Condition", ["Excellent", "Good", "Average", "Poor"])

with st.expander("Lights & Electricals"):
    col1, col2, col3 = st.columns(3)
    with col1:
        headlight_condition = st.selectbox("Headlights", ["Working", "Not Working"])
    with col2:
        indicator_condition = st.selectbox("Indicators", ["Working", "Not Working"])
    with col3:
        battery_condition = st.selectbox("Battery Condition", ["Excellent", "Good", "Average", "Poor"])

with st.expander("Interior & Exterior"):
    col1, col2, col3 = st.columns(3)
    with col1:
        interior_condition = st.selectbox("Interior Condition", ["Excellent", "Good", "Average", "Poor"])
    with col2:
        exterior_condition = st.selectbox("Exterior Condition", ["Excellent", "Good", "Average", "Poor"])
    with col3:
        paint_condition = st.selectbox("Paint Condition", ["Excellent", "Good", "Average", "Poor"])

with st.expander("Safety & Features"):
    col1, col2, col3 = st.columns(3)
    with col1:
        airbags = st.radio("Airbags Functional?", ["Yes", "No"])
    with col2:
        ac_condition = st.selectbox("AC Condition", ["Excellent", "Good", "Average", "Poor"])
    with col3:
        infotainment = st.selectbox("Infotainment System", ["Excellent", "Good", "Average", "Poor"])

with st.expander("Additional Comments / Photos"):
    comments = st.text_area("Comments")
    photos = st.file_uploader("Upload Car Photos", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# --- PDF GENERATION ---
def generate_pdf(data, summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{data['Owner Name']} - {data['Car Model']}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "AI Inspection Summary", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, summary_text)
    pdf.ln(10)

    for section, details in data.items():
        if isinstance(details, dict):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, section, ln=True)
            pdf.set_font("Arial", '', 12)
            for key, value in details.items():
                pdf.cell(0, 8, f"{key}: {value}", ln=True)
            pdf.ln(4)

    return pdf.output(dest='S').encode('latin-1')


# --- AI SUMMARIZATION FUNCTION ---
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# --- SUBMIT BUTTON ---
if st.button("Submit Inspection"):
    try:
        if not owner_name or not car_model:
            st.warning("⚠️ Please fill in at least Owner Name and Car Model before submitting.")
            st.stop()

        # --- STRUCTURED DATA ---
        data = {
            'Owner Name': owner_name,
            'Car Model': car_model,
            'Year': car_year,
            'License Plate': license_plate,
            'Engine & Transmission': {
                'Engine Condition': engine_condition,
                'Transmission Condition': transmission_condition,
                'Oil Leaks': oil_leaks
            },
            'Brakes & Suspension': {
                'Brakes Condition': brakes_condition,
                'Suspension Condition': suspension_condition,
                'Steering Condition': steering_condition
            },
            'Tires & Wheels': {
                'Tire Condition': tire_condition,
                'Wheel Condition': wheel_condition
            },
            'Lights & Electricals': {
                'Headlights': headlight_condition,
                'Indicators': indicator_condition,
                'Battery Condition': battery_condition
            },
            'Interior & Exterior': {
                'Interior Condition': interior_condition,
                'Exterior Condition': exterior_condition,
                'Paint Condition': paint_condition
            },
            'Safety & Features': {
                'Airbags Functional': airbags,
                'AC Condition': ac_condition,
                'Infotainment System': infotainment
            },
            'Additional Comments': {
                'Comments': comments if comments else "No additional comments provided."
            }
        }

        # --- NATURAL LANGUAGE INPUT FOR AI ---
        # --- Make a short natural summary input ---
        inspection_text = f"""
        The vehicle inspected is a {car_year} {car_model} owned by {owner_name}.
        Engine: {engine_condition}. Transmission: {transmission_condition}. Oil leaks: {oil_leaks}.
        Brakes: {brakes_condition}. Suspension: {suspension_condition}. Steering: {steering_condition}.
        Tires: {tire_condition}. Wheels: {wheel_condition}.
        Electrical: Headlights {headlight_condition}, Indicators {indicator_condition}, Battery {battery_condition}.
        Interior: {interior_condition}. Exterior: {exterior_condition}. Paint: {paint_condition}.
        Safety: Airbags functional: {airbags}. AC: {ac_condition}. Infotainment: {infotainment}.
        Comments: {comments if comments else "No additional comments provided."}
"""

# --- Give the model a simple summarization input ---
        model_input = (
            f"Inspection report for {car_year} {car_model}: {inspection_text}"
        )

        summary = summarizer(model_input, max_length=120, min_length=50, do_sample=False)[0]['summary_text']


        # --- GENERATE PDF ---
        pdf_bytes = generate_pdf(data, summary)

        st.success("✅ Inspection report generated successfully with AI Summary!")
        st.subheader("🧾 AI Summary:")
        st.info(summary)

        st.download_button(
            label="📄 Download Inspection Report PDF",
            data=pdf_bytes,
            file_name=f"{owner_name}_{car_model}_Inspection.pdf",
            mime="application/pdf"
        )

        st.balloons()

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.code(traceback.format_exc())

