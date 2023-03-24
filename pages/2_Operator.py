# Library
import streamlit as st
import numpy as np
import cv2

# Function
def operator_sobel(img):
    # Cek apakah gambar grayscale atau bukan
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Kernel
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                        [-1, 0, 1]])

    kernel_y = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
    
    # Operasi Sobel
    img_x = cv2.filter2D(img, -1, kernel_x)
    img_y = cv2.filter2D(img, -1, kernel_y)
    img = cv2.add(img_x, img_y)

    return img

# Title 
st.title("Operator Sobel")
st.markdown("""---""")

# Upload Image
img = st.file_uploader("Upload Citra", type=["png", "jpg", "jpeg"])

if img is not None:
    img = np.frombuffer(img.read(), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Deklarasi Array
    tab1, tab2, tab3 = st.tabs(["Citra Asli", "Operasi Sobel (Image)", "Operasi Sobel (Array)"])

    # Konversi Grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Operasi Sobel
    sobel_img = operator_sobel(gray_img)

    # Tab 1 - Citra Asli
    with tab1:
        # Citra Asli
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Asli</h4>", unsafe_allow_html=True)
        st.image(img, use_column_width=True)

        # Array Citra Asli
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Asli</h4>", unsafe_allow_html=True)
        r, g, b = cv2.split(img)
        with st.expander("RGB Channel"):
            st.write("Red Channel")
            st.write(r)
            st.write("Green Channel")
            st.write(g)
            st.write("Blue Channel")
            st.write(b)

    # Tab 2 - Operasi Sobel (Image)
    with tab2:
        # Citra Grayscale
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Grayscale</h4>", unsafe_allow_html=True)
        st.image(gray_img, use_column_width=True)

        # Citra Hasil
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Hasil</h4>", unsafe_allow_html=True)
        st.image(sobel_img, use_column_width=True)

    # Tab 3 - Operasi Sobel (Array)
    with tab3:
        # Array Citra Grayscale
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Grayscale</h4>", unsafe_allow_html=True)
        st.write(gray_img)

        # Array Citra Hasil
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Hasil</h4>", unsafe_allow_html=True)
        st.write(sobel_img)

else:
    st.markdown("<h4 style='text-align: center; color: white;'>Upload An Image</h4>", unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown("""
<h5 style='text-align: center; color: white;'>Copyright 
<a href="https://google.com">Matsuhisa.Inc</a></h5>""", unsafe_allow_html=True)

