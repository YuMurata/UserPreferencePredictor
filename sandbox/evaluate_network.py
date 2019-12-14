from UserPreferencePredictor.Model.evaluate_network import build_evaluate_network


if __name__ == "__main__":
    input_shape = (32, 32, 3)
    net = build_evaluate_network(input_shape, use_vgg16=False)

    net.summary()
