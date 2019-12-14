from UserPreferencePredictor.Model import make_dataset
import matplotlib.pyplot as plt


if __name__ == "__main__":
    dataset_file_path = r'C:\Users\init\Documents\PythonScripts\ImageEnhancementFromUserPreference\Experiment\Questionnaire\tfrecords\test_224\katsudon\1123\1939\train.tfrecords'
    dataset = make_dataset(dataset_file_path, 1, 'test', (224, 224, 3))

    for _ in range(3):
        data = list(dataset.take(1))[0]
        image_list_pair = data[0]
        left_image_list, right_image_list = image_list_pair

        figure = plt.figure()
        ax1 = figure.add_subplot(1, 2, 1)
        ax1.imshow(left_image_list[0])
        ax1.set_axis_off()

        ax2 = figure.add_subplot(1, 2, 2)
        ax2.imshow(right_image_list[0])
        ax2.set_axis_off()

    plt.show()
