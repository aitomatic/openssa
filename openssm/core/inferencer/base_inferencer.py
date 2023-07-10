from .abstract_inferencer import AbstractInferencer


class BaseInferencer(AbstractInferencer):
    def predict(self, input: dict) -> dict:
        """
        The BaseInferencer always returns a prediction of True.
        """
        return {"prediction": True}

    def load(self, path: str):
        """
        The BaseInferencer does not need to load anything.
        """
        pass
