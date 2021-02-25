import pytest

from random import choice, randint


@pytest.fixture(scope="session", name="load_data")
def load_data():
    """Load Pycaret Airline dataset."""
    from pycaret.datasets import get_data

    airline_data = get_data("airline")

    airline_data.index = airline_data.index.astype("datetime64[ns]")

    return airline_data


parametrize_list = [
    (randint(2, 5), randint(5, 10), "expandingwindow"),
    (randint(2, 5), randint(5, 10), "slidingwindow"),
    (randint(2, 5), randint(5, 10), "timeseries"),
]


@pytest.mark.parametrize("fold, fh, fold_strategy", parametrize_list)
def test_setup_initialization(fold, fh, fold_strategy, load_data):

    from pycaret.time_series import setup
    from sktime.forecasting.model_selection._split import (
        ExpandingWindowSplitter,
        SlidingWindowSplitter,
    )
    from sklearn.model_selection import TimeSeriesSplit

    exp_name = setup(
        data=load_data,
        fold=fold,
        fh=fh,
        fold_strategy=fold_strategy,
    )

    if fold_strategy == "expandingwindow":
        assert isinstance(exp_name.fold_generator, ExpandingWindowSplitter)
    elif fold_strategy == "slidingwindow":
        assert isinstance(exp_name.fold_generator, SlidingWindowSplitter)
    elif fold_strategy == "timeseries":
        assert isinstance(exp_name.fold_generator, TimeSeriesSplit)


setup_raises_list = [
    (randint(50, 100), randint(10, 20), "expandingwindow"),
    (randint(50, 100), randint(10, 20), "slidingwindow"),
]


@pytest.mark.parametrize("fold, fh, fold_strategy", setup_raises_list)
def test_setup_raises(fold, fh, fold_strategy, load_data):

    from pycaret.time_series import setup

    with pytest.raises(ValueError) as errmsg:
        exp_name = setup(
            data=load_data,
            fold=fold,
            fh=fh,
            fold_strategy=fold_strategy,
        )

    exceptionmsg = errmsg.value.args[0]

    assert exceptionmsg == "Not Enough Data Points, set a lower number of folds or fh"