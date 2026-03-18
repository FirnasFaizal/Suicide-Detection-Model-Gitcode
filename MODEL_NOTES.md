# Model Documentation

## Model Architecture
- **Base Model**: DistilBERT (`distilbert-base-uncased`)
- **Type**: Pre-trained transformer for sequence classification
- **Framework**: TensorFlow/Keras + HuggingFace Transformers
- **Parameters**: 66,955,010 trainable parameters

## Model Files
The model is saved in the `model/` directory with the following files:
- `tf_model.h5` - TensorFlow/Keras model weights
- `config.json` - Model configuration
- `tokenizer.json` - Tokenizer configuration
- `tokenizer_config.json` - Additional tokenizer settings
- `vocab.txt` - Vocabulary file
- `special_tokens_map.json` - Special tokens mapping

## Input Format
- **Type**: Raw text string
- **Max Length**: 512 tokens (with truncation)
- **Preprocessing**: Automatic tokenization via DistilBERT tokenizer

## Output Format
The model outputs a classification with:
- **Labels**: 
  - `"suicide"` - Text indicates suicidal thoughts
  - `"non-suicide"` - Text does not indicate suicidal thoughts
- **Confidence Score**: Probability score (0.0 - 1.0)

## Loading the Model
```python
from transformers import pipeline

# Load the trained model pipeline
trained_pipeline = pipeline('text-classification', model='./model', tokenizer='./model', framework='tf')

# Make prediction
result = trained_pipeline("Sample text here", truncation=True, max_length=512)
# Returns: [{'label': 'suicide' or 'non-suicide', 'score': 0.0-1.0}]
```

## Dependencies
Key Python packages required:
- `transformers` - HuggingFace transformers library
- `tensorflow==2.15.1` - Deep learning framework
- `keras<3` - required for compatibility with the exported TensorFlow model
- `torch` - May be needed for some transformers functionality

## Model Performance
- **Accuracy**: 90.94%
- **Precision**: 86.75%
- **Recall**: 96.93%
- **F1 Score**: 91.56%

## Notes
- The model has higher false positive rate (classifying non-suicidal text as suicidal)
- This is intentional for safety - better to err on the side of caution
- Model was trained on 232k balanced examples from Suicide and Depression Detection dataset
- In the current product, this pretrained model remains the only authority for automated risk classification
