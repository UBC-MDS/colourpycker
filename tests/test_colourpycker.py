import numpy as np
import pandas as pd
import altair as alt
import pandas as pd
from colourpycker.colourpycker import donut, get_color_palette, scatterplot, negative
import matplotlib.text as text
import pytest


def test_get_color_palette_valid_input():
    """Test for get_color_palette when input parameters are valid"""
    img_url = "https://i.imgur.com/s9egWBB.jpg"
    tolerance = 20
    limit = 5
    result = get_color_palette(img_url, tolerance, limit)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (5, 3)


def test_get_color_palette_not_a_url():
    """Test for get_color_palette when URL is a random string"""
    try:
        img_url = "soijfoidjfosdijfoisdj"
        tolerance = 20
        limit = 5
        result = get_color_palette(img_url, tolerance, limit)
        assert False
    except:
        # Make sure no exception is raised and the function handles it
        assert True


def test_get_color_palette_url_but_not_image():
    """Test for get_color_palette when URL is valid but it is not pointing to an image"""
    try:
        img_url = "https://soijfoidjfosdijfoisdj.url"
        tolerance = 20
        limit = 5
        result = get_color_palette(img_url, tolerance, limit)
        assert False
    except:
        # Make sure no exception is raised and the function handles it
        assert True


def test_get_color_palette_invalid_tolerance():
    """Test for get_color_palette when tolerance is invalid"""
    try:
        img_url = "https://i.imgur.com/s9egWBB.jpg"
        tolerance = -20000
        limit = 5
        result = get_color_palette(img_url, tolerance, limit)
    except:
        # Make sure no exception is raised and the function handles it
        assert True


def test_donut():
    """Testing that donut() generates the correct output"""
    actual = str(donut("https://i.imgur.com/s9egWBB.jpg", 5, 30, 200, plot_show=False).findobj(text.Text)[0:5]).count("#")
    expect = 5

    assert actual == expect, "the function is not plotting the correct amount of colors"

    actual = str(
        type(
            donut(
                "https://i.imgur.com/s9egWBB.jpg",
                5,
                30,
                200,
                plot_show=False,
            )
        )
    )
    expect = "<class 'matplotlib.figure.Figure'>"
    assert actual == expect, "The function is not outputting a matplotlib figure"

        
    actual = str(donut("https://i.imgur.com/s9egWBB.jpg", 5, 30, 200, plot_show=False).findobj(text.Text)[0]).split("#")[1].split(":")[0]
    expect = get_color_palette("https://i.imgur.com/s9egWBB.jpg", 30, 5).iloc[0,0].replace("#","")
    assert actual == expect, "the function is not returning the correct colors"


def test_scatterplot():
    """Testing that the function scatterplot() generates the correct output and expects the right inputs."""
    # Creating a test dataframe
    test_df = pd.DataFrame(
        {
            "x": np.array([1.1, 1.3, 2.4, 1.5, 1.9, 2.1, 2.1, 0.9, 3.1]),
            "y": np.array([6.8, 7.2, 9.4, 8.3, 5.4, 9.6, 2.9, 6.6, 4.3]),
            "fill": np.array(["A", "B", "C", "A", "B", "C", "A", "B", "C"]),
        }
    )

    # Creating a test plot
    test_scatter = scatterplot(
        "https://i.imgur.com/s9egWBB.jpg",
        test_df,
        "x",
        "y",
        "fill",
        50,
    )

    # Tests
    assert test_scatter.mark == "point", "The mark should be a point"

    assert (
        type(test_scatter) == alt.vegalite.v4.api.Chart
    ), "The return should be an altair Chart"

    assert (
        test_scatter.encoding.fill.scale.range
        == get_color_palette(
            r"https://i.imgur.com/s9egWBB.jpg",
            50,
            3,
        )["HEX"].to_list()
    ), "The fill of the points should be the colours from the image"

    assert (
        test_scatter.encoding.x.field == "x"
    ), "The x-axis of the points should be mapped to the x axis of the Chart"

    assert (
        test_scatter.encoding.y.field == "y"
    ), "The y-axis of the points should be mapped to the y axis of the Chart"

    with pytest.raises(TypeError):
        # x cannot be numeric
        scatterplot(
            "https://i.imgur.com/s9egWBB.jpg",
            test_df,
            50,
            "y",
            "fill",
            50,
        )
        # y cannot be numeric
        scatterplot(
            "https://i.imgur.com/s9egWBB.jpg",
            test_df,
            "x",
            50,
            "fill",
            50,
        )
        # fill cannot be numeric
        scatterplot(
            "https://i.imgur.com/s9egWBB.jpg",
            test_df,
            "x",
            "y",
            "50",
            50,
        )
        # tolerance cannot be cannot a float
        scatterplot(
            "https://i.imgur.com/s9egWBB.jpg",
            test_df,
            "x",
            "y",
            "50",
            50.75,
        )

def test_negative():
    """Test that negative() generates the correct output and expects the right inputs."""
    expected = pd.DataFrame(
        {
            "HEX": ["#94604a", "#f6edf2", "#244176", "#c999d8", "#3eaadc"],
            "RGB": [
                (148, 96, 74),
                (246, 237, 242),
                (36, 65, 118),
                (201, 153, 216),
                (62, 170, 220),
            ],
        }
    )

    actual = negative(
        "https://i.imgur.com/s9egWBB.jpg",
        5,
        50,
    )

    assert isinstance(actual, pd.DataFrame), "Output is not a data frame."
    assert (
        actual.columns[0] == expected.columns[0]
    ), "Output data frame does not contain the column for HEX codes."
    assert (
        len(actual.index) == 5
    ), "Output data frame does not contain the correct number of rows."
    assert (
        expected["HEX"].iloc[0] == actual["HEX"].iloc[0]
    ), "HEX code of the most common negative colour is not correct."
    assert (
        expected["RGB"].iloc[0] == actual["RGB"].iloc[0]
    ), "RGB code of the most common negative colour is not correct."

    # check inversion
    test_rgb = expected["RGB"].iloc[2]
    normal_rgb = (
        255 - int(test_rgb[0]),
        255 - int(test_rgb[1]),
        255 - int(test_rgb[2]),
    )

    actual_rgb = actual["RGB"].iloc[2]
    actual_normal = (
        255 - int(actual_rgb[0]),
        255 - int(actual_rgb[1]),
        255 - int(actual_rgb[2]),
    )

    assert actual_normal == normal_rgb, "RGB code did not invert correctly."

    # maximum tolerance
    high_tol = negative(
        "https://i.imgur.com/s9egWBB.jpg",
        10,
        100,
    )
    # tolerance was set to a high value relative to the number of colours extracted
    moderate_tol = negative(
        "https://i.imgur.com/s9egWBB.jpg",
        20,
        88,
    )

    assert (
        len(high_tol.index) == 1
    ), "Setting tolerance to 100 should result in a maximum of 1 colour extracted."
    assert (
        len(moderate_tol.index) <= 20
    ), "Output data frame should have less than the specified number of colours."

    # partially transparent image
    partial = negative("https://i.stack.imgur.com/G4NCG.png", 20, 5)

    assert (
        len(partial.index) == 1
    ), "Output data frame should contain one colour; partially transparent images should ignore transparent pixels."

    with pytest.raises(ValueError):
        # trying to read a path instead of a URL
        negative("path/to/img.png", 4, 10)
        # trying to extract colours from a transparent image
        negative(
            "https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png",
            5,
            100,
        )

    with pytest.raises(TypeError):
        # tolerance cannot be a float
        negative(
            "https://i.imgur.com/s9egWBB.jpg",
            4,
            25.5,
        )
        # number of colours cannot be a float
        negative(
            "https://i.imgur.com/s9egWBB.jpg",
            4.8,
            25,
        )
        # tolerance must be less than 100
        negative(
            "https://i.imgur.com/s9egWBB.jpg",
            5,
            101,
        )
        # tolerance cannot be 0
        negative(
            "https://i.imgur.com/s9egWBB.jpg",
            5,
            0,
        )
        # tolerance cannot be a negative integer
        negative(
            "https://i.imgur.com/s9egWBB.jpg",
            5,
            -10,
        )