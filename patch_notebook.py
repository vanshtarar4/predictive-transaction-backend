import json
import os
import numpy as np # Needed for type checking if used in eval, but here we are just writing strings.

nb_path = 'notebooks/train_model.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The code to inject
new_code = [
    "# Prepare data for SHAP\n",
    "# We need to transform X using the preprocessor part of the pipeline\n",
    "preprocessor = model.named_steps['preprocessor']\n",
    "classifier = model.named_steps['classifier']\n",
    "\n",
    "X_transformed = preprocessor.transform(X)\n",
    "\n",
    "# Get feature names from preprocessor\n",
    "feature_names = []\n",
    "if hasattr(preprocessor, 'get_feature_names_out'):\n",
    "    feature_names = preprocessor.get_feature_names_out()\n",
    "else:\n",
    "    # Fallback if get_feature_names_out is not available or complex\n",
    "    feature_names = [f'feature_{i}' for i in range(X_transformed.shape[1])]\n",
    "\n",
    "# Create SHAP explainer\n",
    "# Using a sample for speed if dataset is large\n",
    "X_sample = X_transformed[:100] if X_transformed.shape[0] > 100 else X_transformed\n",
    "\n",
    "# 1. Use TreeExplainer\n",
    "explainer = shap.TreeExplainer(classifier)\n",
    "shap_values = explainer.shap_values(X_sample)\n",
    "\n",
    "# 2. Check the type to be safe (Optional debugging print)\n",
    "print(f\"Type of shap_values: {type(shap_values)}\")\n",
    "if isinstance(shap_values, list):\n",
    "    print(f\"List length: {len(shap_values)}\")\n",
    "else:\n",
    "    print(f\"Array shape: {shap_values.shape}\")\n",
    "\n",
    "# 3. PLOT - CORRECTED\n",
    "# If shap_values is an array (most likely), pass it directly\n",
    "if not isinstance(shap_values, list):\n",
    "    shap.summary_plot(shap_values, X_sample, feature_names=feature_names)\n",
    "# If it IS a list (Multiclass or older sklearn), keep your original logic\n",
    "else:\n",
    "    shap.summary_plot(shap_values[1], X_sample, feature_names=feature_names)\n"
]

# Find the cell to replace (the last code cell)
found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "shap.summary_plot" in source or "shap.TreeExplainer" in source:
            cell['source'] = new_code
            found = True
            break

if found:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Notebook patched successfully.")
else:
    print("Could not find the target cell to patch.")
