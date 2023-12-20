import numpy as np
import skimage.io as io
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops, regionprops_table
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd


'''def create_individual_label_figure(label_img, regions):

    desired_label = int(input("Enter the label number (1 to 80): "))
    found_region = next((region for region in regions if region.label == desired_label), None)
    
    if found_region:
        single_label_binary_img = np.zeros_like(label_img, dtype=np.uint8)
        np.putmask(single_label_binary_img, label_img == found_region.label, found_region.label)  

        fig, ax = plt.subplots()
        ax.imshow(single_label_binary_img, cmap='nipy_spectral', interpolation='nearest')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        rect = patches.Rectangle(
            (found_region.bbox[1], found_region.bbox[0]),
            found_region.bbox[3] - found_region.bbox[1],
            found_region.bbox[2] - found_region.bbox[0],
            linewidth=1,
            edgecolor='r',
            facecolor='none'
        )
        ax.add_patch(rect)
        
        

        plt.savefig(f'C:/Users/theocf/Documents/Theo-Tarefas/Classifier/label_{desired_label}.png', dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

        plt.show()
'''        



def create_individual_label_figure(label_img, regions, save_path='C:/Users/theocf/Documents/Theo-Tarefas/Classifier/'):
    for desired_label in range(1, 81):
        found_region = next((region for region in regions if region.label == desired_label), None)

        if found_region:
            single_label_binary_img = np.zeros_like(label_img, dtype=np.uint8)
            np.putmask(single_label_binary_img, label_img == found_region.label, found_region.label)

            fig, ax = plt.subplots()
            ax.imshow(single_label_binary_img, cmap='nipy_spectral', interpolation='nearest')

            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            rect = patches.Rectangle(
                (found_region.bbox[1], found_region.bbox[0]),
                found_region.bbox[3] - found_region.bbox[1],
                found_region.bbox[2] - found_region.bbox[0],
                linewidth=1,
                edgecolor='r',
                facecolor='none'
            )
            ax.add_patch(rect)

            plt.savefig(f'{save_path}label_{desired_label}.png', dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)
            plt.close()  

        else:
            print(f"Label {desired_label} not found in the specified regions.")





    else:
        print("Invalid label number. Please enter a label within the specified regions.")
        

def create_labels_with_number(inverted_binary_img, label_img, regions):
    top_100_binary_img = np.zeros_like(inverted_binary_img, dtype=np.uint8)

    for region in regions:
        np.putmask(top_100_binary_img, label_img == region.label, region.label)

    fig, ax = plt.subplots()
    ax.imshow(top_100_binary_img, cmap='nipy_spectral', interpolation='nearest')

    for region in regions:
        y, x = region.centroid

        ax.text(x + 10, y, str(region.label), color='white', ha='left', va='center', fontsize=6)


    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])



    plt.savefig('C:/Users/theocf/Documents/Theo-Tarefas/Classifier/top_100_binary_img_with_numbers.png', dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

    plt.show()

def create_labels_without_number(inverted_binary_img, label_img, regions):
    top_100_binary_img = np.zeros_like(inverted_binary_img, dtype=np.uint8)

    for region in regions:
        np.putmask(top_100_binary_img, label_img == region.label, region.label)

    fig, ax = plt.subplots()
    ax.imshow(top_100_binary_img, cmap='nipy_spectral', interpolation='nearest')

    ax.set_axis_off()  

    plt.savefig('C:/Users/theocf/Documents/Theo-Tarefas/Classifier/top_100_binary_img_without_numbers.png', dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)

    plt.show()

img_path = "C:/Users/theocf/Documents/Theo-Tarefas/DeePore/Resultados_Sapinhoa/Imagens_binarizadas/9-BRSA-928-SPS_5157.65_x10_PP_BINARIZED.png"
img = io.imread(img_path)

thresh = 254

binary_img = img > thresh
binary_img = binary_img.astype(np.uint8)

inverted_binary_img = 1 - binary_img

label_img = label(inverted_binary_img, connectivity=2)  

regions = regionprops(label_img)
regions = sorted(regions, key=lambda x: x.area, reverse=True)

regions1 = regions[:40]
regions2 = regions[int(len(regions)/2):int((len(regions)/2)+40)]
regions = regions1 + regions2


i = 1
for region in regions:
    label_img[label_img == region.label] = i
    region.label = i
    i += 1
    

plt.imshow(binary_img, cmap='gray')
plt.show()


data = []

for region in regions:
    major_length = region.major_axis_length
    minor_length = region.minor_axis_length
    area = region.area
    bounding_box = region.bbox
    eccentricity = region.eccentricity
    roundness = ((region.perimeter)**2) * ((region.area) * 4)
    equivalent_diameter = np.sqrt(4 * region.area / np.pi)
    rectangularity = region.area / region.bbox_area
    solidity = region.area / region.convex_area

    if major_length == 0:
        equivalent_ratio = 0
    else:
        equivalent_ratio = equivalent_diameter / major_length

    if minor_length == 0:
        elongation = 0
    else:
        elongation = major_length / minor_length

  
    data.append({
        'Area': area,
        'Eccentricity': eccentricity,
        'Elongation': elongation,
        'Roundness': roundness,
        'Equivalent Ratio': equivalent_ratio,
        'Rectangularity': rectangularity,
        'Solidity': solidity
    })


df = pd.DataFrame(data)


df['Class'] = '.'

df.loc[df.index == 0, 'Class'] = 'vugular'


# Display the DataFrame
print(df)
df.to_csv('output.csv', index=False)

    
#create_individual_label_figure(label_img, regions)
create_labels_with_number(inverted_binary_img, label_img, regions)
create_labels_without_number(inverted_binary_img, label_img, regions)
