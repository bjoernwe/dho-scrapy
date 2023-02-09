from experiments.experiment_template import experiment


def test_template_runs_without_errors():
    experiment(show_plot=False)
