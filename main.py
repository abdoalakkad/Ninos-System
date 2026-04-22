import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval

# إعدادات نينوس
st.set_page_config(page_title="Nino's Management", page_icon="☕")

# التصميم
st.markdown("<h1 style='text-align: center; color: #4E342E;'>NINO'S SYSTEM</h1>", unsafe_allow_html=True)

# ملفات البيانات
LOG_FILE = "attendance.csv"
STAFF_FILE = "staff_list.csv"

# تحميل قائمة الموظفين
if os.path.isfile(STAFF_FILE):
    staff_df = pd.read_csv(STAFF_FILE)
    staff_names = staff_df['name'].tolist()
else:
    staff_names = ["عبدالرحمن"] # الموظف الافتراضي

# الموقع الجغرافي
loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(s => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: s.coords}, '*'); }, e => {}, {enableHighAccuracy: false})", key="loc_v6")

name = st.query_params.get("name", None)

# --- واجهة الموظف ---
if name:
    st.subheader(f"أهلاً بك: {name} 👋")
    if loc:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("حضور ✅"):
                pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M"), "حضور"]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.success("تم تسجيل حضورك بنجاح")
        with col2:
            if st.button("انصراف 🏁"):
                pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M"), "انصراف"]]).to_csv(LOG_FILE, mode='a', index=False, header=not os.path.isfile(LOG_FILE))
                st.warning("تم تسجيل انصرافك")
    else:
        st.info("جاري طلب الموقع.. تأكد من تفعيل GPS")

# --- لوحة الإدارة (هنا التحكم كله) ---
else:
    st.sidebar.title("🔐 لوحة تحكم نينوس")
    pw = st.sidebar.text_input("كلمة السر:", type="password")
    
    if pw == "Ninos2026":
        tab1, tab2, tab3 = st.tabs(["سجل الحضور", "إدارة الموظفين", "الرواتب"])
        
        with tab1:
            if os.path.isfile(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
            else:
                st.write("لا يوجد سجلات حضور بعد.")

        with tab2:
            st.subheader("إضافة موظف جديد")
            new_staff = st.text_input("اسم الموظف الرباعي:")
            if st.button("إضافة الموظف للسيستم"):
                new_data = pd.DataFrame([[new_staff]], columns=['name'])
                new_data.to_csv(STAFF_FILE, mode='a', index=False, header=not os.path.isfile(STAFF_FILE))
                st.success(f"تم إضافة {new_staff} بنجاح!")
        
        with tab3:
            st.subheader("حساب الرواتب")
            selected_user = st.selectbox("اختار الموظف:", staff_names)
            salary = st.number_input("الراتب الأساسي:", value=11000)
            deduction = st.number_input("إجمالي الخصومات:", value=0)
            st.metric("الصافي المستحق", f"{salary - deduction} EGP")
