from src.data import DataInjection
from src.features import featurebuilding



data_injection = DataInjection()
fe=featurebuilding()
data = data_injection.load_data(data_injection.datainjectionconfig.data_path)
train_data, test_data = data_injection.split_data(data, data_injection.datainjectionconfig.params['test_split'], data_injection.datainjectionconfig.params['seed'])
type_change=fe.datatype_change(df=train_data)
feature_build=fe.binning(df=type_change)