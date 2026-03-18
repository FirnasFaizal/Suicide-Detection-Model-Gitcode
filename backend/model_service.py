from __future__ import annotations

import importlib
import logging
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _ensure_keras_engine_compat() -> None:
    try:
        importlib.import_module("keras.engine")
    except ModuleNotFoundError:
        engine_package = types.ModuleType("keras.engine")
        engine_package.__path__ = []  # type: ignore[attr-defined]

        engine_modules = [
            "data_adapter",
            "keras_tensor",
            "training",
            "base_layer",
            "input_spec",
        ]

        for module_name in engine_modules:
            tf_module = importlib.import_module(f"tensorflow.python.keras.engine.{module_name}")
            sys.modules[f"keras.engine.{module_name}"] = tf_module
            setattr(engine_package, module_name, tf_module)

        sys.modules["keras.engine"] = engine_package

    try:
        importlib.import_module("keras.saving.legacy")
    except ModuleNotFoundError:
        saving_package = types.ModuleType("keras.saving")
        saving_package.__path__ = []  # type: ignore[attr-defined]
        legacy_package = types.ModuleType("keras.saving.legacy")
        legacy_package.__path__ = []  # type: ignore[attr-defined]

        saving_modules = ["hdf5_format", "save", "saving_utils", "model_config"]
        for module_name in saving_modules:
            tf_module = importlib.import_module(f"tensorflow.python.keras.saving.{module_name}")
            sys.modules[f"keras.saving.legacy.{module_name}"] = tf_module
            setattr(legacy_package, module_name, tf_module)

        sys.modules["keras.saving"] = saving_package
        sys.modules["keras.saving.legacy"] = legacy_package
        setattr(saving_package, "legacy", legacy_package)


_ensure_keras_engine_compat()

try:
    from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
except ImportError:  # pragma: no cover - depends on local environment
    AutoTokenizer = None
    TFAutoModelForSequenceClassification = None

try:
    import tensorflow as tf
except ImportError:  # pragma: no cover - depends on local environment
    tf = None


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DetectionResult:
    label: str
    confidence: float
    risk_level: str
    summary: str
    recommended_action: str


class ModelService:
    def __init__(self, model_dir: Path):
        self.model_dir = model_dir
        self.model_pipeline: Any | None = None
        self.tokenizer: Any | None = None
        self.model: Any | None = None
        self.model_available = False
        self.status_message = "Model has not been initialized yet."

    def load(self) -> None:
        weights_path = self.model_dir / "tf_model.h5"
        config_path = self.model_dir / "config.json"

        if not self.model_dir.exists():
            self.status_message = f"Model directory not found at {self.model_dir}."
            logger.warning(self.status_message)
            return

        if not config_path.exists() or not weights_path.exists():
            self.status_message = (
                "Model files are incomplete. Ensure the full Git LFS model assets are present in the model directory."
            )
            logger.warning(self.status_message)
            return

        if weights_path.stat().st_size < 1024:
            self.status_message = (
                "Model weights appear to be a Git LFS pointer. Run `git lfs pull` to download the real classifier."
            )
            logger.warning(self.status_message)
            return

        try:
            logger.info("Loading pretrained suicide-risk classifier from %s", self.model_dir)
            self.tokenizer, self.model = self._build_pipeline()
            self.model_available = True
            self.status_message = "Pretrained classifier loaded successfully."
            logger.info(self.status_message)
        except Exception as exc:  # pragma: no cover - exercised in runtime
            self.model_pipeline = None
            self.tokenizer = None
            self.model = None
            self.model_available = False
            self.status_message = f"Classifier unavailable: {exc}"
            logger.exception("Failed to load pretrained classifier")

    def _build_pipeline(self):
        if AutoTokenizer is None or TFAutoModelForSequenceClassification is None or tf is None:
            raise RuntimeError(
                "TensorFlow-compatible Transformers classes are unavailable in this environment. "
                "Install the backend requirements with a TensorFlow-supported Transformers release."
            )

        tokenizer = AutoTokenizer.from_pretrained(str(self.model_dir))
        model = TFAutoModelForSequenceClassification.from_pretrained(str(self.model_dir), from_pt=False)
        return tokenizer, model

    def analyze(self, text: str) -> DetectionResult:
        if not self.model_available or self.tokenizer is None or self.model is None or tf is None:
            raise RuntimeError("Pretrained classifier is unavailable.")

        encoded = self.tokenizer(text, truncation=True, max_length=512, return_tensors="tf")
        outputs = self.model(encoded)
        probabilities = tf.nn.softmax(outputs.logits, axis=-1).numpy()[0]
        label_index = int(probabilities.argmax())

        if getattr(self.model.config, "id2label", None):
            raw_label = str(self.model.config.id2label.get(label_index, "non-suicide")).strip().lower()
        else:
            raw_label = "suicide" if label_index == 1 else "non-suicide"

        label = "suicide" if raw_label == "suicide" else "non-suicide"
        confidence = float(probabilities[label_index])

        if label == "suicide":
            return DetectionResult(
                label=label,
                confidence=confidence,
                risk_level="high",
                summary="The pretrained classifier detected language that may indicate elevated suicide risk in this message.",
                recommended_action="Encourage immediate human support and show crisis resources without delay.",
            )

        return DetectionResult(
            label=label,
            confidence=confidence,
            risk_level="lower",
            summary="The pretrained classifier did not detect high-risk suicide language in this message.",
            recommended_action="Continue with supportive, non-diagnostic conversation and encourage professional support when helpful.",
        )
