import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import matplotlib.pyplot as plt

data_dir = "downloads"
BATCH_SIZE = 4
IMG_SIZE = (160, 160)


def prepare_dataset():
    global train_dataset
    global class_names

    train_dataset = image_dataset_from_directory(
        data_dir, shuffle=True, batch_size=BATCH_SIZE, image_size=IMG_SIZE
    )
    class_names = train_dataset.class_names

    train_batches = tf.data.experimental.cardinality(train_dataset)
    test_dataset = train_dataset.take(train_batches // 5)
    train_dataset = train_dataset.skip(train_batches // 5)

    print(
        "Number of train batches: %d" % tf.data.experimental.cardinality(train_dataset)
    )
    print("Number of test batches: %d" % tf.data.experimental.cardinality(test_dataset))

    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    return train_dataset, test_dataset


def build_model():
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
            tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
        ]
    )
    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    IMG_SHAPE = IMG_SIZE + (3,)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SHAPE, include_top=False, weights="imagenet"
    )
    image_batch, label_batch = next(iter(train_dataset))
    feature_batch = base_model(image_batch)

    base_model.trainable = False

    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    feature_batch_average = global_average_layer(feature_batch)

    prediction_layer = tf.keras.layers.Dense(1)
    prediction_batch = prediction_layer(feature_batch_average)

    inputs = tf.keras.Input(shape=(160, 160, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = global_average_layer(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = prediction_layer(x)
    model = tf.keras.Model(inputs, outputs)

    base_learning_rate = 0.0001
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(lr=base_learning_rate),
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model


def visualization(
    model,
    test_dataset,
):
    # Retrieve a batch of images from the test set
    image_batch, label_batch = test_dataset.as_numpy_iterator().next()
    predictions = model.predict_on_batch(image_batch).flatten()

    # Apply a sigmoid since our model returns logits
    predictions = tf.nn.sigmoid(predictions)
    predictions = tf.where(predictions < 0.5, 0, 1)

    print("Predictions:\n", predictions.numpy())
    print("Labels:\n", label_batch)

    plt.figure(figsize=(10, 10))
    for i in range(4):
        ax = plt.subplot(2, 2, i + 1)
        plt.imshow(image_batch[i].astype("uint8"))
        plt.title(class_names[predictions[i]])
        plt.axis("off")
    plt.savefig("result/result.png")


def train(epochs):
    # Prepare Dataset
    train_dataset, test_dataset = prepare_dataset()

    # Build Model
    model = build_model()

    # Train
    history = model.fit(train_dataset, epochs=epochs)

    # Evaluate
    loss, accuracy = model.evaluate(test_dataset)
    print("Test accuracy :", accuracy)

    # Visualization
    visualization(model, test_dataset)

    # Save model to example classifier
    model.save("./example_classifier/saved_model")

    # Save labels to exmaple classifier
    