import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

# Remove the background
def background_correction(img):
    # Write the data in terms of 3-dim points excluding the contact zone
    coord_background_intensity = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            coord_background_intensity.append([i, j, img[i,j]])

    # 3-dim data points
    data = np.array(coord_background_intensity)

    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = linalg.lstsq(A, data[:,2])

    # Copy the original img
    Background = np.ones(img.shape)

    # Fill the bacground with the values came from the fitting
    for X in range(img.shape[0]):
        for Y in range(img.shape[1]):
            Background[X,Y] = C[0] + C[1]*X + C[2]*Y + C[3]*X*Y + C[4]*X*X + C[5]*Y*Y

    return img - Background + Background.mean()


# PLot image and label
def plot_img_label(img, label, image_title='Image', label_title='Label'):
    fig, (ax_image, ax_label) = plt.subplots(1,2, figsize=(10, 6), tight_layout=True)
    ax_image.imshow(img, cmap='gray')
    ax_image.set_title(image_title)
    ax_image.set_axis_off()
    
    ax_label.imshow(label, cmap='gray')
    ax_label.set_title(label_title)
    ax_label.set_axis_off()