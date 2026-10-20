from .fit import main as _fit
from .predict import main as _predict


def fit() -> None:
    _fit()


def predict() -> None:
    _predict()
