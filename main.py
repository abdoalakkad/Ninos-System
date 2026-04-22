import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_user_agent

# 1. إعدادات الثيم والاحترافية
st.set_page_config(page_title="Nino's Business System", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    h1, h2, h3, p, label { color: #000000 !important; font-family: 'Arial'; text-align: center; }
    .stButton>button { 
        background-color: #FFEB3B; color: black; border-radius: 10px; 
        font-weight: bold; border: 2px solid black; width: 100%; height: 3.5em;
    }
    .sidebar .sidebar-content { background-color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. الملفات والإعدادات
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_list.csv"
BASIC_SALARY = 11000
WORKING_DAYS = 26

# عرض اللوجو
logo_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg')) and 'nino' in f.lower()]
if logo_files:
    st.image(logo_files[0], width=150)
else:
    st.markdown("<h1>NINO'S SYSTEM</h1>", unsafe_allow_html=True)

# جلب بيانات الجهاز والموقع
ua = get_user_agent()
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: true})", key="gps_final")

# 3. واجهة الموظفين (بصمة الحضور)
name = st.query_params.get("name", None)

if name:
    st.markdown(f"## مرحباً بك يا {name}")
    if loc:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("تسجيل حضور ✅"):
                data = [[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "حضور", ua]]
                pd.DataFrame(data).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.success("تم تسجيل الحضور")
        with col2:
            if st.button("تسجيل انصراف 🏁"):
                data = [[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "انصراف", ua]]
                pd.DataFrame(data).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.warning("تم تسجيل الانصراف")
    else:
        st.info("جاري تحديد موقعك لضمان البصمة داخل الكافيه...")

# 4. لوحة الإدارة (الباسورد Ninos2026)
else:
    st.sidebar.title("🔐 لوحة التحكم")
    pwd = st.sidebar.text_input("كلمة السر", type="password")
    
    if pwd == "Ninos2026":
        tab1, tab2, tab3 = st.tabs(["📊 السجلات والرواتب", "👤 إضافة موظف", "📝 قائمة الموظفين"])
        
        with tab1:
            st.markdown("### مراجعة البيانات الحية")
            if os.path.isfile(LOG_FILE):
                df = pd.read_csv(LOG_FILE)
                df.columns = ['الموظف', 'التوقيت', 'الحالة', 'الجهاز']
                st.dataframe(df, use_container_width=True)
                
                st.divider()
                st.markdown("### حاسبة الرواتب الذكية")
                s_hours = st.number_input("حدد عدد ساعات الشفت لهذا الموظف:", min_value=1.0, value=8.0, step=0.5)
                h_rate = BASIC_SALARY / (WORKING_DAYS * s_hours)
                st.metric("سعر الساعة بناءً على الشفت", f"{round(h_rate, 2)} ج.م")
            else:
                st.write("لا توجد سجلات حضور حتى الآن.")

        with tab2:
            st.markdown("### إضافة موظف جديد للسيستم")
            new_staff = st.text_input("اسم الموظف الثنائي:")
            if st.button("حفظ الموظف"):
                if new_staff:
                    pd.DataFrame([[new_staff]]).to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                    st.success(f"تم إضافة {new_staff} بنجاح")
                    st.code(f"رابط البصمة الخاص به:\nhttps://ninos-system.streamlit.app/?name={new_staff.replace(' ', '%20')}")

        with tab3:
            if os.path.isfile(STAFF_FILE):
                staff_df = pd.read_csv(STAFF_FILE)
                staff_df.columns = ['أطقم العمل المسجلة']
                st.table(staff_df)
    else:
        st.markdown("### يرجى إدخال كلمة السر للوصول للإدارة")
