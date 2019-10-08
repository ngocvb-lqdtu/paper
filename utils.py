import numpy as np
def load_data(dataset, standardize=True):
    """

    :param dataset:
    :param standardize:
    :return:
    """
    features = dataset['features']
    features = np.array([feature for feature in features])
    labels = dataset['labels']
    labels = np.array([label for label in labels])
    bool_maps = dataset['bool_maps']
    bool_maps = np.array([bool_map for bool_map in bool_maps])
    percentage_resources = dataset['percentage_resources']
    percentage_resources = np.array([percentage_resource for percentage_resource in percentage_resources])
    if standardize:
        features = features/255.0

    return features, labels, bool_maps, percentage_resources
