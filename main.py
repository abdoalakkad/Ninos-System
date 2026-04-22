import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Nino's System", page_icon="☕")

# --- عرض اللوجو الجديد ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("ninos_logo.png"):
        st.image("ninos_logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #4E342E;'>NINO'S</h1>", unsafe_allow_html=True)

# --- الإعدادات الأساسية ---
BASIC_SALARY = 11000 
WORKING_DAYS = 26
LOG_FILE = "attendance.csv"

# الموقع الجغرافي (البصمة)
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: false})", key="loc_v11")

name = st.query_params.get("name", None)

if name:
    st.subheader(f"صباح الفل يا {name} ☕")
    if loc:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("تسجيل حضور ✅"):
                pd.DataFrame([[name, datetime.now(), "حضور"]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.success("تم تسجيل الحضور")
        with c2:
            if st.button("تسجيل انصراف 🏁"):
                pd.DataFrame([[name, datetime.now(), "انصراف"]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.warning("تم تسجيل الانصراف")
else:
    st.sidebar.title("🔐 لوحة الإدارة")
    if st.sidebar.text_input("كلمة السر:", type="password") == "Ninos2026":
        st.write("### مراجعة الرواتب والساعات")
        
        # اختيار عدد الساعات (عشان مصطفى الـ 10 ساعات)
        shift_h = st.number_input("عدد ساعات الشفت للموظف:", min_value=1, max_value=24, value=8)
        
        total_monthly_h = WORKING_DAYS * shift_h
        hour_rate = BASIC_SALARY / total_monthly_h
        
        st.metric("سعر ساعة الموظف ده", f"{round(hour_rate, 2)} EGP")
        st.info(f"الحسبة بناءً على {shift_h} ساعات يومياً لـ {WORKING_DAYS} يوم في الشهر.")

        if os.path.isfile(LOG_FILE):
            st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
