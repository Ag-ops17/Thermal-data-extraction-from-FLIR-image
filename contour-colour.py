from PIL import Image, ImageDraw
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

# Read the IR image using Pillow
image_path = r'D:\urmita\FLIR0005.jpg'
image = Image.open(image_path)

# Convert the image to NumPy array
image_np = np.array(image)

# Convert the image to HSV color space
hsv = Image.fromarray(image_np).convert('HSV')

# Define color ranges in HSV along with corresponding temperature ranges
color_and_temp_ranges = [
    ((0, 50, 20), (20, 255, 255), (25, 28)),   # Red tones
    ((21, 50, 20), (40, 255, 255), (28.1, 30)),  # Orange tones
    ((41, 50, 20), (80, 255, 255), (30.1, 31)),  # Yellow tones
    ((81, 50, 20), (120, 255, 255), (31.1, 32)), # Green tones
    ((121, 50, 20), (180, 255, 255), (32.1, 33)), # Blue and purple tones
    ((181, 50, 20), (220, 255, 255), (33.1, 34)), # Additional temperature range
    ((221, 50, 20), (255, 255, 255), (34.1, 100)) # Additional temperature range
]

# Initialize variables for tracking regions, color, and temperature values
regions = []
color_and_temp_values = []

# Iterate through color and temperature ranges
for i, (lower, upper, temp_range) in enumerate(color_and_temp_ranges):
    # Threshold the image based on color range
    lower_np = np.array(lower)
    upper_np = np.array(upper)
    mask_np = np.all(np.logical_and(lower_np <= hsv, hsv <= upper_np), axis=-1)

    # Find contours in the masked image using skimage.measure
    contours = measure.find_contours(mask_np, 0.5)

    # Draw contours on the original image using Pillow
    draw = ImageDraw.Draw(image)
    for contour in contours:
        draw.line(tuple(map(tuple, contour[:, ::-1])), fill=(0, 255, 0), width=2)

    # Calculate total area for the current color range using Pillow
    total_area = sum(len(contour) for contour in contours)

    # Add region, color, and temperature values to lists
    regions.append({
        'contours': contours,
        'color_range': f'Color {i + 1}',
        'temp_range': temp_range
    })

    color_and_temp_values.append({
        'region': i + 1,
        'color_range': f'Color {i + 1}',
        'temp_range': temp_range,
        'total_area': total_area
    })

# Display the image with contours using Matplotlib
plt.imshow(image)
plt.title('Image with Contours')
plt.show()

# Plot color range and temperature vs. area heatmap
color_and_temp_ranges_labels = [f'Color {i + 1}\n{temp_range[0]} to {temp_range[1]} °C' for i, (_, _, temp_range) in enumerate(color_and_temp_ranges)]
areas = [color_and_temp_info['total_area'] for color_and_temp_info in color_and_temp_values]

plt.bar(color_and_temp_ranges_labels, areas, color=['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gray'])
plt.xlabel('Color Range and Temperature')
plt.ylabel('Area')
plt.title('Color Range and Temperature vs. Area Heatmap')
plt.show()
