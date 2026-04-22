import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات الألوان (بيبي بلو، أصفر، أبيض)
st.set_page_config(page_title="Nino's Management", page_icon="☕")

st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; } /* بيبي بلو */
    h1, h3 { color: #0D47A1; text-align: center; font-family: 'Arial'; }
    .stButton>button { 
        background-color: #FFF176; /* أصفر */
        color: #0D47A1; 
        border-radius: 15px; 
        font-weight: bold; 
        border: 2px solid #1E88E5;
    }
    .stTextInput>div>div>input { background-color: white; }
    </style>
""", unsafe_allow_html=True)

# عرض اللوجو
if os.path.exists("ninos_logo.png"):
    st.image("ninos_logo.png", width=150)

# 2. إعدادات الموقع والبيانات
BASIC_SALARY = 11000
WORKING_DAYS = 26
LOG_FILE = "attendance.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # ** حط هنا إحداثيات الكافيه بالظبط **

# جلب بيانات الجهاز والموقع
ua_string = get_user_agent() # نوع التليفون
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps")

name = st.query_params.get("name", None)

if name:
    st.write(f"### مرحباً {name}")
    if loc:
        # حساب المسافة (تبسيط للزوم)
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        
        if dist < 0.001: # داخل الزوم (حوالي 100 متر)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("بصمة حضور ✅"):
                    data = [[name, datetime.now(), "حضور", ua_string]]
                    pd.DataFrame(data).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.success("تم تسجيل حضورك بنجاح")
            with c2:
                if st.button("بصمة انصراف 🏁"):
                    data = [[name, datetime.now(), "انصراف", ua_string]]
                    pd.DataFrame(data).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.warning("تم تسجيل انصرافك")
        else:
            st.error("⚠️ أنت خارج الزوم! لازم تكون موجود في الكافيه عشان تبصم.")
else:
    # لوحة الإدارة
    st.sidebar.title("🔐 الإدارة")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        st.write("### مراجعة الرواتب والأجهزة")
        user_h = st.number_input("شفت الموظف (ساعات):", value=8)
        hour_rate = BASIC_SALARY / (WORKING_DAYS * user_h)
        st.info(f"سعر الساعة لهذا الموظف: {round(hour_rate, 2)} ج.م (بناءً على شفت {user_h} ساعات)")
        
        if os.path.isfile(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            df.columns = ['الموظف', 'الوقت', 'الحالة', 'نوع الجهاز']
            st.dataframe(df)
