import numpy as np
import streamlit as st
import cv2 as cv


# Title
st.title("Kontur Detection")
st.markdown("""---""")

# Upload Image
img = st.file_uploader("Upload Citra", type=["png", "jpg", "jpeg"])


# Fungsi untuk menampilkan citra dengan Streamlit
def show_image(img):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    st.image(img_rgb)


def freeman_chain_code(contours, i):
    codes = []
    for j in range(len(contours[i])):
        if j == len(contours[i])-1:
            break
        else:
            x1 = contours[i][j][0][0]
            y1 = contours[i][j][0][1]
            x2 = contours[i][j+1][0][0]
            y2 = contours[i][j+1][0][1]
            if x1 == x2 and y1 < y2:
                codes.append("0")
            elif x1 < x2 and y1 < y2:
                codes.append("1")
            elif x1 < x2 and y1 == y2:
                codes.append("2")
            elif x1 < x2 and y1 > y2:
                codes.append("3")
            elif x1 == x2 and y1 > y2:
                codes.append("4")
            elif x1 > x2 and y1 > y2:
                codes.append("5")
            elif x1 > x2 and y1 == y2:
                codes.append("6")
            elif x1 > x2 and y1 < y2:
                codes.append("7")
            else:
                codes.append("error")
    return codes

# Fungsi untuk mendekode Freeman Chain Code


def decode_freeman_chain_code(code, start_point, img_shape):
    x, y = start_point
    chain_code = [int(c) for c in code]
    points = [(x, y)]

    # Calculate image center
    center_x = int(img_shape[1] / 2)
    center_y = int(img_shape[0] / 2)

    for i, c in enumerate(chain_code):
        if i >= len(code):
            break
        if c == 0:
            y += 1
        elif c == 1:
            x += 1
            y += 1
        elif c == 2:
            x += 1
        elif c == 3:
            x += 1
            y -= 1
        elif c == 4:
            y -= 1
        elif c == 5:
            x -= 1
            y -= 1
        elif c == 6:
            x -= 1
        elif c == 7:
            x -= 1
            y += 1

        # Check if point is out of bounds
        if x < 0:
            x = 0
        elif x >= img_shape[1]:
            x = img_shape[1] - 1

        if y < 0:
            y = 0
        elif y >= img_shape[0]:
            y = img_shape[0] - 1

        points.append((x, y))

    # Calculate offset from center to start point
    offset_x = center_x - start_point[0]
    offset_y = center_y - start_point[1]

    # Shift all points by the offset
    shifted_points = []
    for point in points:
        x = point[0] + offset_x
        y = point[1] + offset_y
        shifted_points.append((x, y))

    return shifted_points


if img is not None:
    img = np.frombuffer(img.read(), np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Deklarasi Array
    tab1, tab2, tab3 = st.tabs(
        ["Citra Asli", "Deteksi Kontur (Image)", "Freeman Chain Code"])
    
    # Konversi Grayscale
    imgray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)


    kernel = np.ones((3, 3), np.uint8)

    # Konversi Grayscale
    imgray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# Konversi Biner
    ret, imgbin = cv.threshold(imgray, 127, 255, 0)

# Dilasi
    imgdil = cv.dilate(imgbin, kernel, iterations=1)

# Erosi
    imgero = cv.erode(imgdil, kernel, iterations=1)

# Deteksi Kontur
    contours, hierarchy = cv.findContours(
    imgero, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    code = freeman_chain_code(contours, 1)
    start_point = tuple(contours[1][0][0])
    decoded_points = decode_freeman_chain_code(code, start_point, img.shape)

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
        img_result = cv.drawContours(img, contours, 1, (0, 255, 0), 3)
        st.image(img_result, use_column_width=True)

    # Tab 3 - Freeman Chain Code
    with tab3:
        # Freeman Chain Code
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Freeman Chain Code</h4>", unsafe_allow_html=True)
        # print as string
        st.write("".join(code))
    

        # Dekode Freeman Chain Code
        st.markdown(
            "<h4 style='text-align: center; color: white;'>Dekode Freeman Chain Code</h4>", unsafe_allow_html=True)
            # Dekode Freeman Chain Code dan tampilkan citra hasil decode


        # Mendekode Freeman Chain Code dan menampilkan citra hasil decode
        decoded_img = np.zeros_like(img)

        decoded_contours = np.array([decoded_points], dtype=np.int32)
        decoded_img = cv.drawContours(decoded_img, decoded_contours, -1, (0, 255, 0), 3)
        st.image(decoded_img, use_column_width=True)
else:
    st.markdown("<h4 style='text-align: center; color: white;'>Silahkan Upload Citra</h4>",
                unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown("""
<h5 style='text-align: center; color: white;'>Copyright 
<a href="https://google.com">Matsuhisa.Inc</a></h5>""", unsafe_allow_html=True)
