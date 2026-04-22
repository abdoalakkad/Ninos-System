import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات الصفحة والألوان (تعديل التباين للوضوح التام)
st.set_page_config(page_title="Nino's System", page_icon="☕")

st.markdown("""
    <style>
    /* خلفية بيبي بلو هادية جداً */
    .stApp { 
        background-color: #F0F8FF; 
    } 
    /* كل الكلام بالأسود الصريح عشان الوضوح */
    h1, h2, h3, p, span, label { 
        color: #000000 !important; 
        text-align: center; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* تنسيق الزراير: أصفر بحدود واضحة */
    .stButton>button { 
        background-color: #FFEB3B; 
        color: #000000; 
        border-radius: 12px; 
        font-weight: bold; 
        border: 2px solid #000000;
        height: 3em;
        width: 100%;
    }
    /* مدخلات البيانات */
    .stTextInput>div>div>input { 
        color: black;
        border: 1px solid #000000;
    }
    </style>
""", unsafe_allow_html=True)

# 2. عرض اللوجو
logo_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg')) and 'nino' in f.lower()]
if logo_files:
    st.image(logo_files[0], width=180)
else:
    st.markdown("<h1>NINO'S COFFEE</h1>", unsafe_allow_html=True)

# 3. إعدادات الحسبة (الـ 11000 جنيه)
BASIC_SALARY = 11000
WORKING_DAYS = 26
LOG_FILE = "attendance.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # تأكد من وضع إحداثياتك هنا

# جلب البيانات
ua_string = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_v13")

name = st.query_params.get("name", None)

if name:
    st.markdown(f"## صباح الفل يا {name}")
    if loc:
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        if dist < 0.001: 
            c1, c2 = st.columns(2)
            with c1:
                if st.button("بصمة حضور ✅"):
                    pd.DataFrame([[name, datetime.now(), "حضور", ua_string]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.success("تم تسجيل الحضور")
            with c2:
                if st.button("بصمة انصراف 🏁"):
                    pd.DataFrame([[name, datetime.now(), "انصراف", ua_string]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.warning("تم تسجيل الانصراف")
        else:
            st.error("⚠️ إنت بره الزوم! لازم تكون في الكافيه عشان تبصم.")
else:
    st.sidebar.title("🔐 الإدارة")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        st.markdown("### مراجعة الرواتب والأجهزة")
        user_h = st.number_input("ساعات الشفت (8 أو 10 لمصطفى):", value=8)
        hour_rate = BASIC_SALARY / (WORKING_DAYS * user_h)
        st.write(f"**سعر الساعة حالياً:** {round(hour_rate, 2)} ج.م")
        
        if os.path.isfile(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            df.columns = ['الموظف', 'الوقت', 'الحالة', 'الجهاز']
            st.dataframe(df)
