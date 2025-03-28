from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import uvicorn
from io import BytesIO
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your model
MODEL_PATH = "saved_model/sinus_model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    CLASS_NAMES = ["healthy", "unhealthy"]
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

@app.post("/predict")  # Changed from /api/predict to match your frontend
async def predict(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}, content-type: {file.content_type}")
        
        # Read image contents
        contents = await file.read()
        
        # Open and convert image
        image = Image.open(BytesIO(contents))
        
        # Convert to RGB (this handles both RGBA and grayscale images)
        image = image.convert('RGB')
        
        # Log image details
        logger.info(f"Image mode: {image.mode}, size: {image.size}")
        
        # Preprocess the image
        img = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Verify shape before prediction
        logger.info(f"Input array shape: {img_array.shape}")
        
        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        predicted_label = CLASS_NAMES[predicted_class_index]
        
        logger.info(f"Prediction made: {predicted_label} with confidence {confidence}")

        return {
            "status": "success",
            "predicted_label": predicted_label,
            "confidence": confidence,
            "message": "Image processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Failed to process image: {str(e)}",
                "error_type": type(e).__name__
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)