
import numpy as np
import streamlit as st
import cv2 as cv


# Title
st.title("Kontur Detection")
st.markdown("""---""")

# Upload Image
img = st.file_uploader("Upload Citra", type=["png", "jpg", "jpeg"])

if img is not None:
    img = np.frombuffer(img.read(), np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Deklarasi Array
    tab1, tab2, tab3 = st.tabs(
        ["Citra Asli", "Deteksi Kontur (Image)", "Deteksi Kontur (Array)"])

    # Konversi Grayscale
    imgray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Konversi Biner
    ret, imgbin = cv.threshold(imgray, 127, 255, 0)

    # Deteksi Kontur
    contours, hierarchy = cv.findContours(
        imgbin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Tab 1 - Citra Asli
    with tab1:
        # Citra Asli
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Citra Asli</h3>", unsafe_allow_html=True)
        st.image(img, use_column_width=True)

        # Array Citra Asli
        st.markdown(
            "<h4 style='text-align: center; color: white;'> Array Citra Asli</h4>", unsafe_allow_html=True)
        r, g, b = cv.split(img)
        with st.expander("RGB Channel"):
            st.write("Red Channel")
            st.write(r)
            st.write("Green Channel")
            st.write(g)
            st.write("Blue Channel")
            st.write(b)

    # Tab 2 - Deteksi Kontur (Image)
    with tab2:
        # Citra Biner
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Citra Biner</h4>", unsafe_allow_html=True)
        st.image(imgbin, use_column_width=True)

        # Citra Kontur
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Citra Kontur</h4>", unsafe_allow_html=True)
        img_result = cv.drawContours(img, contours, -1, (0, 255, 0), 3)
        st.image(img_result, use_column_width=True)

    # Tab 3 - Deteksi Kontur (Array)
    with tab3:
        # Array Citra Kontur
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Array Citra Kontur</h4>", unsafe_allow_html=True)
        st.write(contours)

else:
    st.markdown("<h4 style='text-align: center; color: white;'>Silahkan Upload Citra</h4>",
                unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown("""
<h5 style='text-align: center; color: white;'>Copyright 
<a href="https://google.com">MadPilot.Inc</a></h5>""", unsafe_allow_html=True)
