import streamlit as st
import requests
import os
import base64

# --- CONFIGURATION ---
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="P-RAG-DF",
    page_icon="frontend/assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ASSETS LOADER ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    logo_base64 = get_base64_of_bin_file("frontend/assets/logo.png")
except:
    logo_base64 = ""

# --- ADVANCED JS PARTICLES (Background Effect) ---
# We inject a script that creates a canvas and renders reacting particles
particles_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d');
    var particles = [];
    var mouse = { x: null, y: null };

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    window.addEventListener('mousemove', function(e) {
        mouse.x = e.x;
        mouse.y = e.y;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Mouse interaction (repel)
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 100) {
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (100 - distance) / 100;
                this.speedX -= forceDirectionX * force * 0.5;
                this.speedY -= forceDirectionY * force * 0.5;
            }

            if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
            if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
        }
        draw() {
            ctx.fillStyle = 'rgba(139, 92, 246, 0.5)'; // Violet particles
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function init() {
        for (let i = 0; i < 100; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            
            // Connect particles
            for (let j = i; j < particles.length; j++) {
                let dx = particles[i].x - particles[j].x;
                let dy = particles[i].y - particles[j].y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.1)';
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                    ctx.closePath();
                }
            }
        }
        requestAnimationFrame(animate);
    }

    init();
    animate();
});
</script>
"""

st.components.v1.html(particles_js, height=0, width=0)


# --- CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* GLOBAL */
    .stApp {
        background-color: #0b0c15; /* Deep Space Black */
    }
    
    body {
        font-family: 'Inter', sans-serif;
    }

    /* HEADER LAYOUT */
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-bottom: 50px;
    }
    .header-text {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: 0.2rem;
        background: linear-gradient(to right, #ffffff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(165, 180, 252, 0.3);
    }
    .header-logo {
        width: 80px;
        height: 80px;
        filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.8));
        animation: pulse 4s infinite ease-in-out;
    }
    
    @keyframes pulse {
        0% { filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.6)); }
        50% { filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.9)); }
        100% { filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.6)); }
    }

    /* GLASS CARDS */
    .glass-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: border 0.3s ease;
    }
    .glass-box:hover {
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    /* ANSWER BOX (Top) */
    .answer-box {
        min-height: 200px;
        border-left: 3px solid #8b5cf6;
        background: linear-gradient(90deg, rgba(139, 92, 246, 0.05) 0%, rgba(0,0,0,0) 100%);
        padding: 20px;
        margin-bottom: 30px;
        border-radius: 0 12px 12px 0;
        color: #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    /* BUTTONS */
    div.stButton > button {
        background: transparent;
        border: 1px solid #8b5cf6;
        color: #a5b4fc;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    div.stButton > button:hover {
        background: rgba(139, 92, 246, 0.1);
        border-color: #c084fc;
        color: #fff;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (P-RAG-DF TEXT ONLY) ---
st.markdown("""
    <div class="header-container">
        <span class="header-text">P-RAG-DF</span>
    </div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

# --- LEFT COLUMN: UPLOAD ---
with col1:
    st.markdown('<div class="glass-box" style="height: 100%">', unsafe_allow_html=True)
    st.subheader("SYSTEM UPLINK")
    
    uploaded_file = st.file_uploader("Select Encrypted Document", type=["pdf"])
    
    if uploaded_file:
        if st.button("EXECUTE UPLOAD"):
            with st.spinner("Encrypting & Transmitting..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    res = requests.post(f"{BACKEND_URL}/upload/", files=files)
                    
                    if res.status_code == 200:
                        st.session_state.uploaded = True
                        st.success(f"SYSTEM: Indexed {uploaded_file.name}")
                    else:
                        st.error(f"SYSTEM ERROR: {res.status_code}")
                except Exception as e:
                    st.error(f"FATAL ERROR: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT COLUMN: Q&A (Answer ABOVE Question) ---
with col2:
    st.markdown('<div class="glass-box" style="height: 100%">', unsafe_allow_html=True)
    st.subheader("NEURAL RESPONSE")
    
    # 1. ANSWER BLOCK (Display placeholder or previous answer)
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = "Awaiting input sequence..."
        st.session_state.last_sources = []

    st.markdown(f"""
        <div class="answer-box">
            {st.session_state.last_answer}
        </div>
    """, unsafe_allow_html=True)

    # Sources dropdown
    if st.session_state.last_sources:
        with st.expander("REFERENCE DATA"):
            for src in st.session_state.last_sources:
                st.code(f"FILE: {src.get('file')} \nPAGE: {src.get('page')}", language="bash")

    # 2. INPUT BLOCK (Below Answer)
    st.markdown("---")
    query = st.text_input("INPUT QUERY", key="query_input")
    
    if st.button("PROCESS REQUEST"):
        if not query:
            st.warning("Input required.")
        elif not st.session_state.get("uploaded", False):
            st.warning("Database empty. Initiate Uplink first.")
        else:
            with st.spinner("Processing..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat/",
                        json={"query": query}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        # Update session state to show in the Answer Box above
                        st.session_state.last_answer = data.get("answer")
                        st.session_state.last_sources = data.get("sources")
                        st.rerun() # Rerun to update the answer block at the top
                    else:
                        st.error("Server Compute Failure")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
