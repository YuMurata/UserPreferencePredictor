from setuptools import setup

setup(
    name='UserPreferencePredictor',
    version="0.0.1",
    description="ユーザーの好みを推測",
    author='yu murata',
    keywords='farewell',
    install_requires=["tensorflow", 'numpy',
                      'pillow', 'opencv-python', 'deap'],
    packages=['UserPreferencePredictor',
              'UserPreferencePredictor.config',
              'UserPreferencePredictor.Model',
              'UserPreferencePredictor.PreferenceOptimizer',
              'UserPreferencePredictor.TrainDataMaker',
              'UserPreferencePredictor.TrainDataMaker.DataWriter',
              ],
)
