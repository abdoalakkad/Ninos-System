import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات الثيم (بيبي بلو وأسود صريح)
st.set_page_config(page_title="Nino's Accounting System", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label, .stMarkdown { color: #000000 !important; font-family: 'Arial'; }
    .stButton>button { 
        background-color: #FFEB3B; color: black; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3em;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 5px; border: 1px solid #ccc; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. ملفات النظام
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_data.csv"
CAFE_LAT, CAFE_LON = 30.0123, 31.0456 # حط إحداثيات الكافيه هنا

# عرض اللوجو
logo_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg')) and 'nino' in f.lower()]
if logo_files:
    st.image(logo_files[0], width=120)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_final")

name = st.query_params.get("name", None)

# --- واجهة الموظف ---
if name:
    st.markdown(f"## نورت شفتك يا {name} ☕")
    if loc:
        dist = abs(loc['latitude'] - CAFE_LAT) + abs(loc['longitude'] - CAFE_LON)
        if dist < 0.001:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("تسجيل حضور ✅"):
                    pd.DataFrame([[name, datetime.now(), "حضور", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.success("تم تسجيل الحضور")
            with c2:
                if st.button("تسجيل انصراف 🏁"):
                    pd.DataFrame([[name, datetime.now(), "انصراف", ua]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                    st.warning("تم تسجيل الانصراف")
        else:
            st.error("⚠️ إنت بره الزوم! لازم تكون في الكافيه عشان تبصم.")

# --- واجهة الإدارة ---
else:
    st.sidebar.title("🔐 إدارة نينوس")
    if st.sidebar.text_input("كلمة السر", type="password") == "Ninos2026":
        t1, t2, t3 = st.tabs(["💰 تقفيل الرواتب", "➕ إضافة موظف", "📱 سجل البصمة"])
        
        with t1:
            st.markdown("### مراجعة حسابات الشهر")
            if os.path.isfile(STAFF_FILE) and os.path.isfile(LOG_FILE):
                staff_df = pd.read_csv(STAFF_FILE)
                # هنا بنحط منطق الحسابات لكل موظف (ساعات، أوفر تايم، خصم)
                st.write("**بيانات الموظفين والرواتب:**")
                st.dataframe(staff_df, use_container_width=True)
                
                selected_user = st.selectbox("اختار الموظف عشان تنزل خصم:", staff_df['الاسم'].unique())
                discount = st.number_input(f"قيمة الخصم لـ {selected_user}:", min_value=0)
                if st.button("تأكيد الخصم"):
                    st.info(f"تم تسجيل خصم بقيمة {discount} ج.م على {selected_user}")
            else:
                st.info("لا توجد بيانات كافية للحسابات حالياً.")

        with t2:
            st.markdown("### إضافة موظف جديد")
            with st.form("add_staff"):
                new_n = st.text_input("الاسم الثنائي:")
                new_s = st.number_input("الراتب الأساسي (مثلاً 11000):", value=11000)
                new_h = st.number_input("عدد ساعات الشفت الأساسي:", value=8)
                if st.form_submit_button("حفظ الموظف"):
                    pd.DataFrame([[new_n, new_s, new_h]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    st.success(f"تم إضافة {new_n} بنجاح.")
                    st.code(f"رابط البصمة: https://ninos-system.streamlit.app/?name={new_n.replace(' ', '%20')}")

        with t3:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
    else:
        st.markdown("### ادخل الباسورد للدخول للبيانات.")
