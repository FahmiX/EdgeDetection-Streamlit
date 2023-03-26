import streamlit as st

st.set_page_config(
    page_title="Home Page",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.snow()
st.title("Home Page")
st.markdown("""---""")

# Creator
st.markdown("<h2 style='color: red;'>Creator</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>Nama : Achmadya Ridwan Ilyawan</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>NIM : 211511001</h5>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>Nama : Fahmi Ahmad Fadilah</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>NIM : 211511013</h5>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>Nama : Hilman Permana</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='color: white;'>NIM : 211511015</h5>", unsafe_allow_html=True)
st.markdown("""---""")

# Requirements
st.markdown("<h3 style='color: blue;'>Requirements</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='color: white;'>- Streamlit</h6>", unsafe_allow_html=True)
st.code("pip install streamlit", language="python")
st.markdown("<h6 style='color: white;'>- Numpy</h6>", unsafe_allow_html=True)
st.code("pip install numpy", language="python")
st.markdown("<h6 style='color: white;'>- OpenCV</h6>", unsafe_allow_html=True)
st.code("pip install opencv-python-headless", language="python")
st.markdown("<h6 style='color: white;'>- Pandas</h6>", unsafe_allow_html=True)
st.code("pip install pandas", language="python")
st.markdown("<h6 style='color: white;'>- Matplotlib</h6>", unsafe_allow_html=True)
st.code("pip install matplotlib", language="python")
st.markdown("""---""")

# Copy Right
st.markdown("<h6 style='color: green;'>© 2023 - MatPilot.Inc</h6>", unsafe_allow_html=True)