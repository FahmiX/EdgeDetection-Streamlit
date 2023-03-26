import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def sobel_edge_detection(img):
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

# Same as operator_sobel() but more sharp for any image
def sobel_edge_detection2(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Sobel filter
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    
    # Calculate gradient magnitude
    mag = np.sqrt(sobelx**2 + sobely**2)
    mag = np.uint8(mag)
    
    # Apply thresholding to obtain binary image
    thresh = cv2.threshold(mag, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    return thresh

def freeman_chain_code(contour):
    # Create dictionary for the directions
    directions = {
        (0, 1): 0,
        (1, 1): 1,
        (1, 0): 2,
        (1, -1): 3,
        (0, -1): 4,
        (-1, -1): 5,
        (-1, 0): 6,
        (-1, 1): 7
    }
    
    # Define the starting point and starting direction
    current = contour[0][0]
    prev_dir = 0
    
    # Iterate over the contour and calculate the chain code
    chain_code = []
    for i in range(1, len(contour)):
        next_point = contour[i][0]
        diff = tuple(np.subtract(next_point, current))
        direction = directions.get(diff)
        if direction is not None:
            # Calculate the difference between the current and previous direction
            diff_dir = direction - prev_dir
            if diff_dir < 0:
                diff_dir += 8
            chain_code.append(diff_dir)
            prev_dir = direction
            current = next_point
    
    return chain_code

def decode_freeman_chain_code(chain_code):
    # Create dictionary for the directions
    directions = {
        0: (0, 1),
        1: (1, 1),
        2: (1, 0),
        3: (1, -1),
        4: (0, -1),
        5: (-1, -1),
        6: (-1, 0),
        7: (-1, 1)
    }
    
    # Define the starting point and starting direction
    current = (0, 0)
    prev_dir = 0
    
    # Iterate over the chain code and calculate the contour
    contour = []
    for i in range(len(chain_code)):
        # Calculate the current direction
        direction = (prev_dir + chain_code[i]) % 8
        diff = directions.get(direction)
        if diff is not None:
            # Calculate the next point
            next_point = tuple(np.add(current, diff))
            contour.append(next_point)
            prev_dir = direction
            current = next_point
    
    return np.array(contour)

# Title
st.title("Freeman Chain Code & Decoding")
st.markdown("""---""")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Deklarasi Array
    tab1, tab2, tab3 = st.tabs(
        ["Transformasi", "Freeman Chain Code", "Decoding"])

    # Load the image and perform edge detection
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    edges = sobel_edge_detection(img)
    
    # Find the contours and draw them on the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contours = np.zeros(img.shape, dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

    with tab1:
        # Display the original image, sobel, and the contours image side by side
        fig, ax = plt.subplots(1, 3, figsize=(15, 15))
        ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original Image")
        ax[1].imshow(edges, cmap="gray")
        ax[1].set_title("Sobel Edge Detection")
        ax[2].imshow(cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB))
        ax[2].set_title("Contours")
        st.pyplot(fig)

    with tab2:
        # otomatis pilih contour terbesar
        if len(contours) > 0:
            selected_contour = np.argmax([len(c) for c in contours])        
        else:
            selected_contour = None
        
        # jika selected_contour null maka tidak akan dijalankan
        if selected_contour is not None:
            contour = contours[selected_contour]

            # Calculate the Freeman Chain Code for the contour
            chain_code = freeman_chain_code(contour)

            # Display the chain code as a string
            st.write("Chain Code:")
            st.write("".join([str(c) for c in chain_code]))

    with tab3:
        # Decode the chain code and display the contour
        st.write("Decoded Contour:")
        decoded_contour = decode_freeman_chain_code(chain_code)
        img_decoded_contour = np.zeros(img.shape, dtype=np.uint8)
        cv2.drawContours(img_decoded_contour, [decoded_contour], -1, (0, 0, 255), 2)
        st.image(img_decoded_contour, caption="Decoded Contour")
else:
    st.warning("Silahkan upload gambar terlebih dahulu")