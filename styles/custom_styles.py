# styles/custom_styles.py
from config.settings import COLORS

def get_custom_css():
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Exo+2:wght@300;400;600&display=swap');
        
        /* ============================================
           FONDO Y ESTRUCTURA GENERAL
           ============================================ */
        .main {{
            background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['space_dark']} 50%, {COLORS['gradient_end']} 100%);
            background-attachment: fixed;
            position: relative;
        }}
        
        /* Efecto de estrellas animadas */
        .main::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(2px 2px at 20% 30%, white, transparent),
                radial-gradient(2px 2px at 60% 70%, white, transparent),
                radial-gradient(1px 1px at 50% 50%, white, transparent),
                radial-gradient(1px 1px at 80% 10%, white, transparent),
                radial-gradient(2px 2px at 90% 60%, white, transparent),
                radial-gradient(1px 1px at 33% 85%, white, transparent),
                radial-gradient(1px 1px at 65% 25%, white, transparent);
            background-size: 200% 200%;
            background-position: 0% 0%;
            opacity: 0.3;
            animation: twinkle 60s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }}
        
        @keyframes twinkle {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 0.6; }}
        }}
        
        /* ============================================
           TIPOGRAFÍA
           ============================================ */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Orbitron', sans-serif !important;
            color: {COLORS['text']} !important;
            text-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
        }}
        
        h1 {{
            font-size: 3.5rem !important;
            font-weight: 900 !important;
            text-align: center;
            background: linear-gradient(90deg, {COLORS['secondary']}, {COLORS['space_purple']}, {COLORS['space_cyan']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem !important;
            animation: glow 3s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ filter: brightness(1); }}
            50% {{ filter: brightness(1.3); }}
        }}
        
        p, label {{
            font-family: 'Exo 2', sans-serif !important;
        }}
        
        /* ============================================
           SIDEBAR
           ============================================ */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(11, 61, 145, 0.95) 0%, rgba(10, 14, 39, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-right: 2px solid rgba(99, 102, 241, 0.3);
        }}
        
        section[data-testid="stSidebar"] > div {{
            padding-top: 2rem;
        }}
        
        /* ============================================
           BOTONES
           ============================================ */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS['space_purple']} 0%, {COLORS['secondary']} 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 35px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Orbitron', sans-serif;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton > button:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 30px rgba(99, 102, 241, 0.6);
        }}
        
        .stButton > button:active {{
            transform: translateY(-1px) scale(1.02);
        }}
        
        /* ============================================
           TARJETAS Y CONTENEDORES
           ============================================ */
        .metric-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin: 15px 0;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(99, 102, 241, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
            border-color: rgba(99, 102, 241, 0.6);
        }}
        
        .metric-card:hover::before {{
            left: 100%;
        }}
        
        /* ============================================
           MÉTRICAS
           ============================================ */
        div[data-testid="stMetric"] {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
        }}
        
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.5);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        }}
        
        div[data-testid="stMetric"] label {{
            color: {COLORS['text']} !important;
            font-weight: 600;
            font-size: 0.95rem;
        }}
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {COLORS['secondary']} !important;
            font-size: 2rem !important;
            font-weight: 700;
        }}
        
        /* ============================================
           INPUTS Y CONTROLES
           ============================================ */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 10px;
            color: white;
            padding: 10px 15px;
            transition: all 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {{
            border-color: {COLORS['secondary']};
            box-shadow: 0 0 15px rgba(0, 166, 237, 0.5);
            background: rgba(255, 255, 255, 0.15);
        }}
        
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 10px;
            color: white;
        }}
        
        /* ============================================
           CHECKBOXES
           ============================================ */
        .stCheckbox {{
            padding: 8px 0;
        }}
        
        .stCheckbox > label {{
            color: {COLORS['text']} !important;
            font-weight: 500;
        }}
        
        /* ============================================
           PROGRESS BAR
           ============================================ */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {COLORS['space_cyan']} 0%, {COLORS['space_purple']} 100%);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
        }}
        
        /* ============================================
           ALERTAS Y MENSAJES
           ============================================ */
        .stAlert {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-left: 4px solid {COLORS['secondary']};
            border-radius: 10px;
            padding: 15px;
            color: white;
        }}
        
        /* ============================================
           TABLAS
           ============================================ */
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        /* ============================================
           EXPANDERS
           ============================================ */
        .streamlit-expanderHeader {{
            background: rgba(99, 102, 241, 0.2);
            border-radius: 10px;
            color: white !important;
            font-weight: 600;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: rgba(99, 102, 241, 0.3);
        }}
        
        /* ============================================
           FOOTER
           ============================================ */
        .footer {{
            text-align: center;
            color: {COLORS['text']};
            padding: 30px;
            margin-top: 50px;
            background: linear-gradient(180deg, transparent 0%, rgba(11, 61, 145, 0.3) 100%);
            border-top: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 20px 20px 0 0;
        }}
        
        .footer p {{
            margin: 5px 0;
            font-family: 'Exo 2', sans-serif;
        }}
        
        /* ============================================
           ANIMACIONES ESPECIALES
           ============================================ */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animated {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                transform: scale(1);
            }}
            50% {{
                transform: scale(1.05);
            }}
        }}
        
        .pulse {{
            animation: pulse 2s ease-in-out infinite;
        }}
        
        /* ============================================
           EFECTOS DE VIDRIO (GLASSMORPHISM)
           ============================================ */
        .glass {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        /* ============================================
           SCROLLBAR PERSONALIZADA
           ============================================ */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(10, 14, 39, 0.5);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLORS['space_purple']}, {COLORS['secondary']});
            border-radius: 10px;
            border: 2px solid rgba(10, 14, 39, 0.5);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {COLORS['secondary']}, {COLORS['space_cyan']});
        }}
        
        /* ============================================
           RESPONSIVE
           ============================================ */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem !important;
            }}
            
            .metric-card {{
                padding: 15px;
            }}
        }}
    </style>
    """


def get_metric_card_html(title, value, description, icon="🔷", color=None):
    """Genera una tarjeta de métrica con estilo espacial"""
    card_color = color or COLORS['secondary']
    
    return f"""
    <div class="metric-card animated" style="border-left: 4px solid {card_color};">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 2.5rem; margin-right: 15px;">{icon}</span>
            <h3 style="margin: 0; color: {COLORS['text']}; font-size: 1.3rem;">{title}</h3>
        </div>
        <h2 style="color: {card_color}; margin: 15px 0; font-size: 2.5rem; font-weight: 700;">{value}</h2>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 0.95rem;">{description}</p>
    </div>
    """


def get_climate_badge(climate_type, size="medium"):
    """Genera un badge para tipos de clima"""
    from config.settings import MEXICAN_CLIMATE_ZONES
    
    if climate_type in MEXICAN_CLIMATE_ZONES:
        zone = MEXICAN_CLIMATE_ZONES[climate_type]
        emoji = zone['emoji']
        nombre = zone['nombre']
        color = zone['color']
    else:
        emoji = "🌍"
        nombre = climate_type
        color = COLORS['secondary']
    
    font_size = "1.2rem" if size == "large" else "1rem" if size == "medium" else "0.9rem"
    padding = "12px 20px" if size == "large" else "8px 15px" if size == "medium" else "6px 12px"
    
    return f"""
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, {color}22, {color}44);
        border: 2px solid {color};
        border-radius: 25px;
        padding: {padding};
        font-size: {font_size};
        font-weight: 600;
        color: white;
        box-shadow: 0 4px 15px {color}55;
        backdrop-filter: blur(10px);
        margin: 5px;
    ">
        {emoji} {nombre}
    </div>
    """