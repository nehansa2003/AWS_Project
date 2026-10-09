import joblib
from src.config import MODEL_OUTPUT_PATH

print("Model path:", MODEL_OUTPUT_PATH)
model = joblib.load(MODEL_OUTPUT_PATH)

print("Model type:", type(model).__name__)
print("Model module:", type(model).__module__)
print("Has predict:", hasattr(model, "predict"))
print("Has predict_proba:", hasattr(model, "predict_proba"))
print("Classes:", getattr(model, "classes_", "Not exposed"))

if hasattr(model, "feature_names_in_"):
    print("Feature names:", list(model.feature_names_in_))

if hasattr(model, "named_steps"):
    print("Pipeline steps:")
    for name, step in model.named_steps.items():
        print(" ", name, "->", type(step).__name__)
