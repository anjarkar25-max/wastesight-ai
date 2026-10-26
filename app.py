import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="WasteSight AI", page_icon="♻️", layout="centered")

st.title("♻️ WasteSight AI")
st.subheader("Real-Time Computer Vision Waste Segregation")
st.write("Scan an item with your camera or upload a photo to check which municipal bin it belongs in.")

# Sidebar settings & Hackathon Impact Metrics
st.sidebar.header("⚙️ AI Scanner Settings")
conf_threshold = st.sidebar.slider(
    "AI Sensitivity (Confidence Threshold)", 
    min_value=0.05, max_value=0.80, value=0.12, step=0.01,
    help="Lower values help detect crushed or overlapping waste items."
)

if "scans" not in st.session_state:
    st.session_state.scans = 0
if "diverted_g" not in st.session_state:
    st.session_state.diverted_g = 0

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Live Impact Tracker")
st.sidebar.metric("Items Segregated", st.session_state.scans)
st.sidebar.metric("Waste Diverted from Landfill", f"{st.session_state.diverted_g} g")

# Comprehensive rules mapping custom Waste-TACO classes + common household/food/e-waste items
SORTING_RULES = {
    "plastik": {
        "name": "Plastic Packaging / Bottle",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 25,
        "tip": "Rinse off any food residue, remove the cap, and crush the bottle/container before placing it in the Dry Bin."
    },
    "metal": {
        "name": "Metal / Aluminum Can",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 15,
        "tip": "Empty all liquid, rinse briefly, and place in the Dry Recyclable bin."
    },
    "cam": {
        "name": "Glass Bottle / Jar",
        "bin": "🟦 Dry Waste (Recyclable / Glass)",
        "weight_g": 180,
        "tip": "Rinse clean. If broken, wrap securely in newspaper and label clearly before handing to waste collectors."
    },
    "kagit": {
        "name": "Paper",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 10,
        "tip": "Keep clean and dry. Greasy or food-soiled paper should go into Wet/Compost or Reject waste."
    },
    "karton": {
        "name": "Cardboard / Carton",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 85,
        "tip": "Flatten the box completely to save space and remove any plastic tape or bubble wrap."
    },
    "kopuk": {
        "name": "Styrofoam / Thermocol",
        "bin": "🟥 Domestic Reject / Landfill Waste",
        "weight_g": 12,
        "tip": "Styrofoam cannot be recycled in standard municipal bins. Place in Reject/Landfill waste."
    },
    # Secondary Object Detector Mappings (Bottles, Cups, Organic Food, E-Waste)
    "bottle": {
        "name": "Plastic / Beverage Bottle",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 30,
        "tip": "Empty liquid, rinse, crush the bottle, and place in the Dry Recyclable bin."
    },
    "cup": {
        "name": "Disposable Cup / Container",
        "bin": "🟦 Dry Waste (or 🟥 Reject if wax-lined paper)",
        "weight_g": 15,
        "tip": "Rinse out liquid. Clear plastic cups go in Dry Recycling; heavily soiled paper cups go in Reject waste."
    },
    "wine glass": {
        "name": "Glassware",
        "bin": "🟦 Dry Waste (Glass)",
        "weight_g": 150,
        "tip": "Wrap carefully if cracked or broken so sanitation workers are protected."
    },
    "bowl": {
        "name": "Food Bowl / Container",
        "bin": "🟦 Dry Waste (Recyclable)",
        "weight_g": 40,
        "tip": "Scrape any leftover food into the Wet Bin first, then rinse the container for the Dry Bin."
    },
    "banana": {
        "name": "Organic Food Scrap (Fruit Peel)",
        "bin": "🟩 Wet Waste (Compost / Biodegradable)",
        "weight_g": 45,
        "tip": "Place directly into the Green Wet Waste bin for composting or biomethanation. Never mix with plastic bags."
    },
    "apple": {
        "name": "Organic Food Waste",
        "bin": "🟩 Wet Waste (Compost / Biodegradable)",
        "weight_g": 50,
        "tip": "Dispose of in the Green Wet Waste bin for composting."
    },
    "orange": {
        "name": "Citrus / Organic Peel",
        "bin": "🟩 Wet Waste (Compost / Biodegradable)",
        "weight_g": 45,
        "tip": "Place in the Green Wet Waste bin."
    },
    "pizza": {
        "name": "Leftover Food Scrap",
        "bin": "🟩 Wet Waste (Compost / Biodegradable)",
        "weight_g": 80,
        "tip": "Food scraps go in the Green Wet Bin. Grease-stained cardboard parts should be torn off and composted."
    },
    "cell phone": {
        "name": "Electronic Device (Mobile Phone)",
        "bin": "⬛ E-Waste (Authorized Collection Center)",
        "weight_g": 170,
        "tip": "Contains lithium-ion batteries and precious metals. Never throw in regular bins—drop at an E-Waste collection point."
    },
    "laptop": {
        "name": "Electronic Waste (Laptop/Hardware)",
        "bin": "⬛ E-Waste (Authorized Collection Center)",
        "weight_g": 1200,
        "tip": "Hand over to a certified E-Waste recycler or municipal hazardous/e-waste drive."
    },
    "mouse": {
        "name": "Electronic Accessory (Mouse)",
        "bin": "⬛ E-Waste (Authorized Collection Center)",
        "weight_g": 80,
        "tip": "Remove batteries and dispose of in the designated E-Waste bin."
    },
    "keyboard": {
        "name": "Electronic Peripheral (Keyboard)",
        "bin": "⬛ E-Waste (Authorized Collection Center)",
        "weight_g": 400,
        "tip": "Place in the E-Waste bin for plastic and circuit board recovery."
    },
    "book": {
        "name": "Paper / Book / Magazine",
        "bin": "🟦 Dry Waste (Recyclable Paper)",
        "weight_g": 200,
        "tip": "Keep dry and place in the Dry Recyclable bin, or donate if still usable."
    },
    "scissors": {
        "name": "Metal / Sharp Object",
        "bin": "🟦 Dry Waste (Scrap Metal)",
        "weight_g": 65,
        "tip": "Wrap sharp blades in thick paper before placing in the Dry Metal bin."
    }
}

@st.cache_resource
def load_models():
    custom_model = YOLO("best(1).pt")
    general_model = YOLO("yolov8n.pt")
    return custom_model, general_model

custom_model, general_model = load_models()

tab1, tab2 = st.tabs(["📷 Scan with Camera", "📁 Upload Photo"])

with tab1:
    camera_img = st.camera_input("Point your camera at a waste item")

with tab2:
    uploaded_img = st.file_uploader("Upload an image of waste", type=["jpg", "jpeg", "png", "webp"])

input_file = camera_img if camera_img is not None else uploaded_img

if input_file is not None:
    image = Image.open(input_file).convert("RGB")
    img_array = np.array(image)

    with st.spinner("Analyzing waste material..."):
        # 1. Run custom Waste-TACO model first
        res_custom = custom_model.predict(img_array, conf=conf_threshold)
        boxes_found = []

        for box in res_custom[0].boxes:
            cls_id = int(box.cls[0])
            label = custom_model.names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            boxes_found.append((label, conf, xyxy))

        # 2. Also check general model for bottles, cups, organic food, or e-waste
        res_gen = general_model.predict(img_array, conf=conf_threshold)
        for box in res_gen[0].boxes:
            cls_id = int(box.cls[0])
            label = general_model.names[cls_id]
            if label in SORTING_RULES:
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                boxes_found.append((label, conf, xyxy))

        # 3. Fallback ultra-low threshold pass for tricky overlapping piles like terracycle.jpg
        if len(boxes_found) == 0:
            res_low = custom_model.predict(img_array, conf=0.03)
            for box in res_low[0].boxes[:3]:
                cls_id = int(box.cls[0])
                label = custom_model.names[cls_id]
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                boxes_found.append((label, conf, xyxy))

        # 4. Draw bounding boxes on the image
        annotated_img = img_array.copy()
        for label, conf, (x1, y1, x2, y2) in boxes_found:
            rule_name = SORTING_RULES.get(label, {}).get("name", label.capitalize())
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (34, 197, 94), 3)
            cv2.putText(
                annotated_img, f"{rule_name} ({conf*100:.0f}%)",
                (max(10, x1), max(25, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (34, 197, 94), 2
            )

    st.image(annotated_img, caption="WasteSight AI Detection", use_container_width=True)

    if len(boxes_found) == 0:
        st.warning("No distinct single item isolated. Try lowering the AI Sensitivity slider in the left sidebar or scanning a single item.")
    else:
        st.success(f"✅ Detected {len(boxes_found)} waste item(s)!")
        for label, conf, _ in boxes_found:
            rule = SORTING_RULES.get(label, {
                "name": label.capitalize(),
                "bin": "🟦 Dry Waste (Recyclable)",
                "weight_g": 20,
                "tip": "Ensure the item is clean and dry before placing it in the recycling bin."
            })
            st.session_state.scans += 1
            st.session_state.diverted_g += rule["weight_g"]

            with st.container(border=True):
                st.markdown(f"### {rule['name']} ({conf*100:.1f}% confidence)")
                st.markdown(f"**Recommended Bin:** {rule['bin']}")
                st.info(f"**Preparation Tip:** {rule['tip']}")
