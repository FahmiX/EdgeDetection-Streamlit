# Library
import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd

# Function
# Show Image
def show_image(image, title="", type=""):
    # Set the size of the figure
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Show the image
    ax.imshow(image, cmap=type)
    
    # Set the title and turn off the axis
    ax.set_title(title)
    ax.axis("off")
    
    # Display the plot using Streamlit
    st.pyplot(fig)

# Save Array to Excel
def save_to_excel(array, filename):
    # Convert the Sobel array to a DataFrame
    df = pd.DataFrame(array)
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # Write the DataFrame to a sheet named 'Sheet1'
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file
    writer.save()

# Operator Sobel 
def operator_sobel(img):
    # Cek apakah gambar grayscale atau bukan
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # aplikasikan operator sobel pada gambar
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    # gabungkan hasil sobelx dan sobely
    sobel_img = np.sqrt(np.power(sobelx, 2) + np.power(sobely, 2))
    sobel_img = np.round(sobel_img)
    sobel_img = np.clip(sobel_img, 0, 255)
    
    return sobel_img, sobelx, sobely

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
    sobel_img, sobelx_img, sobely_img = operator_sobel(gray_img)

    # Tab 1 - Citra Asli
    with tab1:
        # Citra Asli
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Asli</h4>", unsafe_allow_html=True)
        # st.image(img, use_column_width=False)
        show_image(img, "Citra Asli", "gray")

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
        show_image(gray_img, "Citra Grayscale", "gray")

        # Citra Hasil Operator Sobel X
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Hasil Operator Sobel X</h4>", unsafe_allow_html=True)
        show_image(sobelx_img, "Citra Hasil Operator Sobel X", "gray")

        # Citra Hasil Operator Sobel Y
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Hasil Operator Sobel Y</h4>", unsafe_allow_html=True)
        show_image(sobely_img, "Citra Hasil Operator Sobel Y", "gray")

        # Citra Hasil Operator Sobel
        st.markdown("<h4 style='text-align: center; color: white;'>Citra Hasil Operator Sobel</h4>", unsafe_allow_html=True)
        show_image(sobel_img, "Citra Hasil", "gray")

    # Tab 3 - Operasi Sobel (Array)
    with tab3:
        # Array Citra Grayscale
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Grayscale</h4>", unsafe_allow_html=True)
        st.write(gray_img)

        if st.button("Save Grayscale to Excel"):
            save_to_excel(gray_img, 'grayscale_output.xlsx')
            st.success("Grayscale image saved to grayscale_output.xlsx")

        # Array Citra Hasil Operator Sobel X
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Hasil Operator Sobel X</h4>", unsafe_allow_html=True)
        st.write(sobelx_img)

        if st.button("Save Sobel X to Excel"):
            save_to_excel(sobelx_img, 'sobelx_output.xlsx')
            st.success("Sobel X image saved to sobelx_output.xlsx")

        # Array Citra Hasil Operator Sobel Y
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Hasil Operator Sobel Y</h4>", unsafe_allow_html=True)
        st.write(sobely_img)

        if st.button("Save Sobel Y to Excel"):
            save_to_excel(sobely_img, 'sobely_output.xlsx')
            st.success("Sobel Y image saved to sobely_output.xlsx")

        # Array Citra Hasil Operator Sobel
        st.markdown("<h4 style='text-align: center; color: white;'>Array Citra Hasil Operator Sobel</h4>", unsafe_allow_html=True)
        st.write(sobel_img)

        if st.button("Save Sobel to Excel"):
            save_to_excel(sobel_img, 'sobel_output.xlsx')
            st.success("Sobel image saved to sobel_output.xlsx")

else:
    st.markdown("<h4 style='text-align: center; color: white;'>Upload An Image</h4>", unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown("""
<h5 style='text-align: center; color: white;'>Copyright 
<a href="https://google.com">MadPilot.Inc</a></h5>""", unsafe_allow_html=True)

