from html import entities
from volcengine_ml_platform.innerapi.tracking_client import Client, StepItem, EntityItem, Scalar
cli = Client()


def test():
    experiment = cli.create_experiment("test", description="xyz")
    trial = cli.create_trial(experiment.sid, "", description="", config={
        "abc": 123
    })
    cli.set_trial_config(trial.experiment_id, trial.sid, {
        "abc": 1,
        "loss": 0.1,
    })
    cli.set_trial_summary(trial.experiment_id, trial.sid, {
        "abc": 1,
        "loss": 0.1,
    })
    cli.create_trial_entity_items(trial.experiment_id, trial.sid, [
        StepItem(step=1, entity_items=[
                 EntityItem(type=Scalar.__TYPE__, name="loss", scalar=Scalar(value=0.1))])
    ])
