import matplotlib
import pytest

matplotlib.use("Agg")  # no display needed for testing
from datetime import date

from matplotlib.figure import Figure

from analytics.visualization import plot_equity_curve, plot_slippage_histogram


def test_plot_equity_curve_empty():
    # Should return a Figure even if no data
    fig = plot_equity_curve([], title="Empty Curve")
    assert isinstance(fig, Figure)
    ax = fig.axes[0]
    # No lines should be plotted for empty input
    assert len(ax.get_lines()) == 0


def test_plot_equity_curve_plots_values_and_labels():
    # Given a simple curve, ensure y-data and labels match
    curve = [
        (date(2025, 1, 1), 5.0),
        (date(2025, 1, 2), 7.5),
        (date(2025, 1, 3), 10.0),
    ]
    title = "Test Curve"
    fig = plot_equity_curve(curve, title=title)
    assert isinstance(fig, Figure)
    ax = fig.axes[0]

    lines = ax.get_lines()
    assert len(lines) == 1
    ydata = lines[0].get_ydata().tolist()
    # Y-values should match the provided cumulative P&L
    assert ydata == [5.0, 7.5, 10.0]

    # Axis labels and title
    assert ax.get_title() == title
    assert ax.get_xlabel() == "Date"
    assert ax.get_ylabel() == "Cumulative P&L"


def test_plot_slippage_histogram_empty():
    fig = plot_slippage_histogram([], bins=10, title="Empty Slip")
    ax = fig.axes[0]
    # No bars means no patches
    assert len(ax.patches) == 0


def test_plot_slippage_histogram_values():
    slips = [0.5, 1.0, 1.5, 2.0, 2.0]
    fig = plot_slippage_histogram(slips, bins=4, title="Slip Test")
    ax = fig.axes[0]
    # There should be as many patches as bins (even empty ones)
    assert len(ax.patches) == 4
    # The sum of heights equals the number of slippages
    heights = [p.get_height() for p in ax.patches]
    assert sum(heights) == len(slips)
    assert ax.get_title() == "Slip Test"
