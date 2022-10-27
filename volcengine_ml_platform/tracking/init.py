import namesgenerator
from typing import Dict
from volcengine_ml_platform import tracking as tk
from volcengine_ml_platform.tracking import tk_cli
from volcengine_ml_platform.tracking.common.logger import logger
from volcengine_ml_platform.tracking.experiment import Experiment
from volcengine_ml_platform.tracking.trial import Trial, Config, Summary


def init(
    experiment_name: str,
    experiment_description: str = "",
    trial_name: str = "",
    trial_description: str = "",
    config: Dict = {},
):
    '''Init tracking process to track ML INFO
    '''
    # TODO(kishao): regex check
    # create or get experiment
    global tk
    _experiment = tk_cli.create_experiment(
        name=experiment_name, description=experiment_description)
    tk.experiment = Experiment(
        sid=_experiment['ExperimentId'],
        name=_experiment['Name'],
    )
    # create trial
    trial_name = trial_name or namesgenerator.get_random_name()  # default name
    _trial = tk_cli.create_trial(
        experiment_id=tk.experiment.sid,
        name=trial_name,
        description=trial_description,
        config=config,
    )
    tk.trial = Trial(
        sid=_trial['TrialId'],
    )
    # init config and summary
    tk.config = Config(params=config)
    tk.summary = Summary()
    logger.info("tracking trial %s initialized...", tk.trial.sid)
    return tk.trial
