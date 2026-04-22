import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات المظهر والوضوح (أسود صريح وخلفية هادية)
st.set_page_config(page_title="Nino's System", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label, b, span, div { color: #000000 !important; font-family: 'Arial'; }
    .stButton>button { 
        background-color: #FFEB3B; color: black !important; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3.5em;
    }
    .stDataFrame { background-color: white; border: 1px solid #000; }
    </style>
""", unsafe_allow_html=True)

# 2. ملفات السيستم
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_data.csv"
# *** نصيحة: عشان البصمة تظبط، افتح جوجل ماب من الكافيه وخد الإحداثيات وحطها هنا ***
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 

# عرض اللوجو
if os.path.exists("ninos_logo.png"):
    st.image("ninos_logo.png", width=120)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_final_fix")

# 3. واجهة الموظف (البصمة)
name = st.query_params.get("name", None)

if name:
    st.markdown(f"## نورت نينوس يا {name} ☕")
    if loc:
        # حساب المسافة (زوم 200 متر تقريباً)
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        if dist < 0.002:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("تسجيل حضور ✅"):
                    pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "حضور", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.success("تم الحضور")
            with c2:
                if st.button("تسجيل انصراف 🏁"):
                    pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "انصراف", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.warning("تم الانصراف")
        else:
            st.error("⚠️ لازم تكون جوه الكافيه عشان تبصم!")
    else:
        st.info("جاري تحديد موقعك...")

# 4. لوحة الإدارة
else:
    st.sidebar.title("🔐 إدارة نينوس")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        t1, t2, t3 = st.tabs(["💰 حسابات الشهر", "👤 إضافة موظف", "📱 سجل البصمة"])
        
        with t1:
            st.markdown("### تقفيل الحسابات والرواتب")
            if os.path.isfile(STAFF_FILE):
                sdf = pd.read_csv(STAFF_FILE)
                sdf.columns = ['الاسم', 'المرتب الأساسي', 'ساعات الشفت']
                st.table(sdf)
                
                st.divider()
                st.markdown("### تسجيل (خصم / مكافأة)")
                target = st.selectbox("اختار الموظف:", sdf['الاسم'].unique())
                amount = st.number_input("المبلغ (جنيه):", value=0)
                reason = st.text_input("السبب:")
                if st.button("حفظ الحسبة"):
                    st.success(f"تم تسجيل {amount} ج.م لـ {target} بنجاح")
            else:
                st.info("لسه مفيش موظفين.")

        with t2:
            st.markdown("### إضافة موظف جديد")
            with st.form("new_staff"):
                n = st.text_input("الاسم:")
                s = st.number_input("المرتب (مثلاً 11000):", value=11000)
                h = st.number_input("عدد ساعات الشفت:", value=8)
                if st.form_submit_button("حفظ"):
                    pd.DataFrame([[n, s, h]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    st.success(f"تم حفظ {n}")
                    
                    # اللينك الصافي اللي مستحيل يروح لجيت هاب
                    final_link = f"https://ninos-system.streamlit.app/?name={n.replace(' ', '%20')}"
                    st.markdown("### انسخ اللينك ده وابعته للموظف:")
                    st.code(final_link)

        with t3:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
    else:
        st.markdown("### اكتب الباسورد `Ninos2026` لفتح الإدارة")
