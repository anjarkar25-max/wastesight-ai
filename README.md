# ♻️ WasteSight AI Pro — Autonomous IoT Waste Triage & Smart City OS

**Live Web Application:** [https://wastesight-ai-od2we5hnbdhqcd9n5ycwqv.streamlit.app/](https://wastesight-ai-od2we5hnbdhqcd9n5ycwqv.streamlit.app/)  
**Hackathon Track:** Arbiter Hacks V1 — Theme Track (Rethinking Waste)

WasteSight AI Pro is an end-to-end computer vision, surface-contamination analysis, and physical IoT smart-bin actuation platform designed to eliminate household "wish-cycling" at the point of disposal. It combines a 100-epoch custom YOLOv8s detector, an OpenCV HSV grease/stain analyzer, quantized LiteRT edge weights, a hyper-local scrap resale marketplace, and an automated Cloud-to-Arduino hardware relay.

---

## 🎯 Theme Track Problem Statement & Empirical Measurement

Municipal Material Recovery Facilities (MRFs) lose 30% to 40% of recyclable batches due to source contamination and "wish-cycling"—citizens tossing greasy cardboard, food-soiled plastics, or hazardous lithium-ion e-waste into dry recycling bins. WasteSight AI Pro targets household and campus source segregation at the exact moment of disposal using dual-engine YOLOv8 computer vision, OpenCV HSV surface-stain analysis, and physical Arduino Uno smart-bin actuation.

To measure whether our system works in practice, we conducted a controlled two-round empirical trial across 10 independent participants sorting 200 diverse household waste items (comparing unassisted human sorting against WasteSight AI Pro guidance). Unassisted participants misclassified 76 of 200 items (a 38.0% batch contamination rate), whereas WasteSight AI Pro reduced sorting errors to 8 items (a 4.0% error rate)—achieving an 89.5% relative reduction in source contamination while diverting 100% of hazardous e-waste to authorized buyback hubs.

| Waste Stream | Items Tested | Human Errors | WasteSight Errors | Error Reduction |
| :--- | :--- | :--- | :--- | :--- |
| Dry Recyclables | 80 | 22 | 3 | 86.4% |
| Soiled / Greasy Packaging | 50 | 31 | 3 | 90.3% |
| Wet Organic Scraps | 40 | 11 | 2 | 81.8% |
| Hazardous E-Waste | 30 | 12 | 0 | 100.0% |
| Total / Overall | 200 | 76 (38.0%) | 8 (4.0%) | 89.5% |

Detailed empirical trial charts and 100-epoch model convergence curves are available in the repository and inside Pillar 4 of the live application.

---

## 🏗️ System Architecture & Key Capabilities

### 1. Dual-Engine Vision & OpenCV Surface Contamination Override
* **Multi-Pass Detection:** Pairs custom-trained **WasteSight v3 (YOLOv8s 100-Epoch)** weights with a household object detector to isolate crushed bottles, paper, corrugated cardboard, metal cans, glass, styrofoam, organic fruit peels, and e-waste.
* **Automated Grease & Stain Scoring:** Crops each detected packaging bounding box and computes an OpenCV HSV color-saturation and brightness-variance score. Soiled paper or greasy pizza boxes are automatically rerouted from the Blue Dry Bin to the Green Compost / Red Reject stream before they can ruin clean paper-pulping batches.
* **Air-Gapped Edge Quantization:** Exported to quantized LiteRT (**best_v2.tflite** — 42.7 MB) for zero-cloud execution on single-core ARM CPUs and Raspberry Pi kiosks.

### 2. Autonomous Cloud-to-Arduino Physical Bin Actuation
* **Zero-Touch Hardware Relay:** When an item is classified in the Streamlit Cloud web app, an HTTP pub/sub payload is dispatched via **ntfy.sh** to the local Python serial listener (**bridge.py**).
* **Microcontroller Execution:** The local bridge forwards a 1-byte UART command over USB Serial (9600 baud) to an **Arduino Uno** (**smart_bin_uno.ino**), lighting the matching bin indicator LED and rotating an SG90 servo motor to 90 degrees for 3.5 seconds of contactless disposal.

| Waste Stream | Assigned Bin | Serial Byte | Arduino LED Pin | Servo Action |
| :--- | :--- | :--- | :--- | :--- |
| Dry Recyclable | Blue Bin | B | Pin 2 + 1x Pin 13 | 90 deg Open (3.5s) |
| Wet Compost | Green Bin | G | Pin 3 + 2x Pin 13 | 90 deg Open (3.5s) |
| E-Waste | Black Bin | E | Pin 4 + 3x Pin 13 | 90 deg Open (3.5s) |
| Reject / Soiled | Red Bin | R | Pin 5 + 4x Pin 13 | 90 deg Open (3.5s) |

### 3. Circular Kitchen Engine & Hyper-Local Scrap Marketplace
* **Zero-Waste Upcycling:** Generates culinary recipes (such as spiced banana peel fry and zero-waste apple cinnamon syrup) and 1:3:10 citrus bio-enzyme floor cleaner formulas when organic scraps are scanned.
* **Scrap-to-Cash & Geo-Routing:** Calculates live resale payouts in INR per kg and routes users to verified Kabadiwalas, Raddi depots, E-Waste recyclers, and Municipal MRFs across Nashik, Mumbai, Pune, or any global city via Google Maps search queries.
* **Citizen Eco-Rewards:** Awards Eco-Credits on every verified scan redeemable for municipal transit passes and property tax rebates.

### 4. B2B Smart City OS & Society Compliance Audits
* **Certified CSV Audit Exporter:** Generates downloadable solid-waste compliance certificates for apartment societies and university campuses with verified diversion rates and CO2e lifecycle offsets.
* **Ward Contamination Heatmap:** Displays municipal ward-level contamination alerts, smart bin fill percentages, and collection truck dispatch priorities.

---

## 📂 Repository Structure

* **app.py** — Main 4-pillar Streamlit web application, OpenCV stain analyzer, and cloud IoT publisher
* **bridge.py** — Local Python USB Serial bridge that auto-detects the Arduino COM port and streams live scan triggers
* **smart_bin_uno.ino** — Arduino Uno C++ firmware for LED indicator signaling and SG90 servo lid actuation
* **wastesight_yolov8_training.ipynb** — Google Colab notebook for 100-epoch YOLOv8 training and LiteRT export
* **best_v3.pt / best_v2.pt / best.pt** — Iterative PyTorch model weights across training milestones
* **best_v2.tflite / best.tflite** — Quantized LiteRT edge deployment models
* **trial_benchmark.png** — 200-item empirical contamination reduction benchmark chart
* **results.png & confusion_matrix.png** — 100-epoch mAP@50 training convergence and class confusion matrix
* **requirements.txt & packages.txt** — Python and system dependencies for cloud deployment

---

## 🚀 Local Setup & Hardware Bridge Instructions

### 1. Run the Web Application Locally
```bash
git clone [https://github.com/anjarkar25-max/wastesight-ai.git](https://github.com/anjarkar25-max/wastesight-ai.git)
cd wastesight-ai
pip install -r requirements.txt
streamlit run app.py
