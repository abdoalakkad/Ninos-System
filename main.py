import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. المظهر (بيبي بلو وهدوء تام)
st.set_page_config(page_title="Nino's System", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label, b, span { color: #000000 !important; font-family: 'Arial'; text-align: center; }
    .stButton>button { 
        background-color: #FFEB3B; color: black; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3em;
    }
    .stDataFrame { background-color: white; border-radius: 10px; border: 1px solid #ccc; }
    </style>
""", unsafe_allow_html=True)

# 2. إعدادات النظام
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_data.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # ** حط لوكيشن نينوس هنا **

# عرض اللوجو
logo_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg')) and 'nino' in f.lower()]
if logo_files:
    st.image(logo_files[0], width=130)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_v200")

# 3. واجهة الموظف
name = st.query_params.get("name", None)

if name:
    st.markdown(f"## أهلاً بك في نينوس يا {name}")
    if loc:
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
        st.info("جاري التحقق من موقعك لفتح البصمة...")

# 4. لوحة الإدارة
else:
    st.sidebar.title("🔐 إدارة نينوس")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        t1, t2, t3 = st.tabs(["💰 تقفيل الحسابات", "👤 إضافة موظف", "📱 سجل البصمة"])
        
        with t1:
            st.markdown("### كشف حساب الموظفين")
            if os.path.isfile(STAFF_FILE):
                sdf = pd.read_csv(STAFF_FILE)
                sdf.columns = ['الاسم', 'المرتب', 'الساعات الأساسية']
                st.write("**بيانات التعاقد:**")
                st.table(sdf)
                
                st.divider()
                st.markdown("### تسجيل خصم أو أوفر تايم")
                target = st.selectbox("اختار الموظف:", sdf['الاسم'].unique())
                amount = st.number_input("المبلغ (بالجنيه):", value=0, key="amt")
                note = st.text_input("ملاحظات (سبب الخصم أو الأوفر تايم):")
                if st.button("حفظ العملية"):
                    st.success(f"تم تسجيل {amount} ج.م لـ {target} - {note}")
            else:
                st.info("لا يوجد موظفين مسجلين حالياً.")

        with t2:
            st.markdown("### إضافة موظف جديد")
            with st.form("add_staff_form"):
                n = st.text_input("اسم الموظف الثنائي:")
                s = st.number_input("الراتب الأساسي (11000):", value=11000)
                h = st.number_input("ساعات الشفت (8 أو 10):", value=8)
                if st.form_submit_button("حفظ الموظف"):
                    pd.DataFrame([[n, s, h]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    # الرابط الصريح اللي مش هيدخله على جيت هاب
                    clean_name = n.replace(' ', '%20')
                    st.success(f"تم الحفظ بنجاح!")
                    st.markdown("---")
                    st.write("### اللينك اللي تبعته للموظف (انسخه بالظبط):")
                    st.code(f"https://ninos-system.streamlit.app/?name={clean_name}")

        with t3:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
    else:
        st.markdown("### يرجى إدخال كلمة السر `Ninos2026` للبدء")
