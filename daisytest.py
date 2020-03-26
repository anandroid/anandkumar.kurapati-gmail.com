from skimage.feature import daisy

import skimage.data
import skimage.color
import skimage as sk
import matplotlib.pyplot as plt

img_astronaut       = sk.color.rgb2gray(sk.data.astronaut())
img_photographer    = sk.data.camera()

parameters = [
        {
            'img'           : img_photographer,
            'step'          : 50,
            'radius'        : 10,
            'rings'         : 1,
            'histograms'    : 6,
            'orientations'  : 8,
        },
        {
            'img'           : img_photographer,
            'step'          : 250,
            'radius'        : 100,
            'rings'         : 3,
            'histograms'    : 6,
            'orientations'  : 8,
        },
        {
            'img'           : img_photographer,
            'step'          : 180,
            'radius'        : 58,
            'rings'         : 2,
            'histograms'    : 6,
            'orientations'  : 8,
        },
        {
            'img'           : img_astronaut,
            'step'          : 200,
            'radius'        : 75,
            'rings'         : 1,
            'histograms'    : 3,
            'orientations'  : 4,
        },
        {
            'img'           : img_astronaut,
            'step'          : 180,
            'radius'        : 58,
            'rings'         : 2,
            'histograms'    : 6,
            'orientations'  : 8,
        },
        {
            'img'           : img_astronaut,
            'step'          : 100,
            'radius'        : 50,
            'rings'         : 1,
            'histograms'    : 5,
            'orientations'  : 8,
        }
]


n_parameters = len(parameters)

for i, p in enumerate(parameters):
    descs, descs_img = daisy(visualize=True, **p)

    plt.subplot(2, n_parameters/2, i+1)
    plt.axis('off')
    plt.imshow(descs_img)
    descs_num = descs.shape[0] * descs.shape[1]
    plt.title('%i DAISY descriptors extracted:' % descs_num)

plt.show()