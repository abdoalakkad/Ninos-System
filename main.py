import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. المظهر الاحترافي
st.set_page_config(page_title="Nino's System", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label, b { color: #000000 !important; font-family: 'Arial'; text-align: center; }
    .stButton>button { 
        background-color: #FFEB3B; color: black; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3.5em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إعداد الملفات
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_data.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # ** حط لوكيشن نينوس هنا **

# عرض اللوجو
if os.path.exists("ninos_logo.png"):
    st.image("ninos_logo.png", width=130)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_v100")

# 3. واجهة الموظف
name = st.query_params.get("name", None)

if name:
    st.markdown(f"## أهلاً يا {name} في نينوس ☕")
    if loc:
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        if dist < 0.005: # زوم واسع شوية عشان ما يعلقش
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
            st.error("⚠️ أنت خارج نطاق الكافيه!")
    else:
        st.info("جاري تحديد موقعك...")

# 4. لوحة الإدارة
else:
    st.sidebar.title("🔐 إدارة نينوس")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        t1, t2, t3 = st.tabs(["💰 الحسابات", "👤 إضافة موظف", "📱 السجل"])
        
        with t1:
            st.markdown("### ملخص الرواتب")
            if os.path.isfile(STAFF_FILE):
                sdf = pd.read_csv(STAFF_FILE)
                # حل مشكلة الـ KeyError: التأكد من أسماء الأعمدة
                sdf.columns = ['الاسم', 'المرتب', 'الساعات'] 
                st.dataframe(sdf, use_container_width=True)
                
                target = st.selectbox("اختار الموظف للخصم:", sdf['الاسم'].unique())
                amount = st.number_input("المبلغ:", value=0)
                if st.button("تأكيد العملية"):
                    st.success(f"تم تسجيل {amount} ج.م لـ {target}")
            else:
                st.info("لا يوجد موظفين حالياً. ضيف أول موظف من التابة التانية.")

        with t2:
            st.markdown("### إضافة موظف جديد")
            with st.form("staff_form"):
                n = st.text_input("الاسم:")
                s = st.number_input("المرتب:", value=11000)
                h = st.number_input("الساعات:", value=8)
                if st.form_submit_button("حفظ"):
                    pd.DataFrame([[n, s, h]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    link = f"https://ninos-system.streamlit.app/?name={n.replace(' ', '%20')}"
                    st.success(f"تم الحفظ! ابعت اللينك ده للموظف:")
                    st.code(link)

        with t3:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
    else:
        st.markdown("### ادخل كلمة السر (Ninos2026)")
