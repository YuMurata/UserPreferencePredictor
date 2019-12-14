from UserPreferencePredictor.Model import RankNet
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    image_shape = 224, 224, 3
    model = RankNet(image_shape)
    # model.load(r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\summary\test\katsudon\1122\1813')
    model.trainable_model.load_weights(r'C:\Users\init\Downloads\weights.10-0.36-0.75.h5')

    image = Image.open(
        r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\image\katsudon\2\2.png').convert('RGB')
    cam = model.grad_cam.get_cam(np.array(image), 'block5_conv3')

    fig, ax = plt.subplots()
    ax.imshow(cam)
    ax.set_axis_off()
    plt.show()
