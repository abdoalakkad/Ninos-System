import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات المظهر (بيبي بلو، أبيض، أسود صريح)
st.set_page_config(page_title="Nino's System", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label, b { color: #000000 !important; font-family: 'Arial'; }
    .stButton>button { 
        background-color: #FFEB3B; color: black; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3.5em;
    }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. إعدادات الملفات
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_data.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # ** حط هنا لوكيشن Nino's بالظبط **

# عرض اللوجو (إذا كان موجوداً بنفس الاسم ninos_logo.png)
if os.path.exists("ninos_logo.png"):
    st.image("ninos_logo.png", width=130)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_final_v3")

# 3. واجهة الموظف (البصمة)
name = st.query_params.get("name", None)

if name:
    st.markdown(f"<h2 style='text-align: center;'>أهلاً بك في نينوس يا {name}</h2>", unsafe_allow_html=True)
    if loc:
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        if dist < 0.001:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("تسجيل حضور ✅"):
                    pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "حضور", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.success("تم تسجيل حضورك")
            with c2:
                if st.button("تسجيل انصراف 🏁"):
                    pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "انصراف", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.warning("تم تسجيل انصرافك")
        else:
            st.error("⚠️ أنت خارج نطاق الكافيه! لا يمكنك البصمة حالياً.")
    else:
        st.info("جاري التحقق من موقعك...")

# 4. واجهة الإدارة (الباسورد Ninos2026)
else:
    st.sidebar.title("🔐 إدارة Nino's")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        t1, t2, t3 = st.tabs(["💰 تقفيل الحسابات", "👤 إضافة موظف جديد", "📱 سجل البصمة"])
        
        with t1:
            st.markdown("### ملخص الرواتب والعمل")
            if os.path.isfile(STAFF_FILE):
                staff_df = pd.read_csv(STAFF_FILE)
                st.write("**بيانات الموظفين المسجلة:**")
                st.dataframe(staff_df, use_container_width=True)
                
                st.divider()
                st.markdown("### إضافة خصم أو مكافأة")
                target = st.selectbox("اختار الموظف:", staff_df['الاسم'].unique() if not staff_df.empty else [])
                amount = st.number_input("المبلغ (بالجنيه):", value=0)
                reason = st.text_input("السبب:")
                if st.button("تسجيل العملية"):
                    st.success(f"تم تسجيل {amount} ج.م لـ {target}")

        with t2:
            st.markdown("### إضافة موظف جديد وتوليد اللينك")
            with st.form("staff_form"):
                n = st.text_input("اسم الموظف:")
                s = st.number_input("المرتب الشهري:", value=11000)
                h = st.number_input("ساعات الشفت (مثلاً 8 أو 10):", value=8)
                if st.form_submit_button("حفظ البيانات"):
                    pd.DataFrame([[n, s, h]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    # توليد اللينك الصواب
                    final_link = f"https://ninos-system.streamlit.app/?name={n.replace(' ', '%20')}"
                    st.success(f"تم حفظ {n} بنجاح!")
                    st.markdown(f"**اللينك ده اللي تبعته للموظف على واتساب:**")
                    st.code(final_link)

        with t3:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
    else:
        st.markdown("<h3 style='text-align: center;'>يرجى إدخال كلمة السر للدخول للنظام</h3>", unsafe_allow_html=True)
