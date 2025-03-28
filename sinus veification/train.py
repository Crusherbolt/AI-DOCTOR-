# train.py

import os
import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ---------------------------
# 1. Configuration
# ---------------------------
TRAIN_DIR = "data/train"
VAL_DIR   = "data/val"
BATCH_SIZE = 16
IMG_SIZE   = (224, 224)
LEARNING_RATE = 1e-4
EPOCHS = 30
MODEL_SAVE_PATH = "saved_model/sinus_model.h5"

# ---------------------------
# 2. Load Datasets
# ---------------------------
train_dataset = image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="categorical",  # for multi-class; "binary" if only 2 classes
    class_names=["healthy", "unhealthy"],  # ensure correct order
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=True
)

val_dataset = image_dataset_from_directory(
    VAL_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=["healthy", "unhealthy"],
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=False
)

# Optional: Prefetch for performance
train_dataset = train_dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
val_dataset   = val_dataset.prefetch(buffer_size=tf.data.AUTOTUNE)

# ---------------------------
# 3. Build Model (Fine-Tune)
# ---------------------------
# Load a pretrained ResNet50 (minus its top layers)
base_model = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
)

# Freeze most of the layers for transfer learning
for layer in base_model.layers[:-10]:
    layer.trainable = False

# Build the classification head
x = layers.Flatten()(base_model.output)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.3)(x)
output_layer = layers.Dense(2, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output_layer)

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ---------------------------
# 4. Training Callbacks
# ---------------------------
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)
checkpoint = ModelCheckpoint(
    MODEL_SAVE_PATH,
    monitor='val_loss',
    save_best_only=True,
    mode='min'
)

# ---------------------------
# 5. Train the Model
# ---------------------------
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS,
    callbacks=[early_stop, checkpoint]
)

# The best model is automatically saved to MODEL_SAVE_PATH
print(f"Model saved to {MODEL_SAVE_PATH}")
