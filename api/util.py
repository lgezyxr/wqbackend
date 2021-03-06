import ownphotos.settings
import os.path
import logging
import logging.handlers
import os

import numpy as np
import requests
import spacy
from scipy.spatial import distance

nlp = spacy.load('en_core_web_sm')

logger = logging.getLogger('ownphotos')
fomatter = logging.Formatter(
    '%(asctime)s : %(filename)s : %(funcName)s : %(lineno)s : %(levelname)s : %(message)s')
fileMaxByte = 256 * 1024 * 200  # 100MB
fileHandler = logging.handlers.RotatingFileHandler(
    os.path.join(ownphotos.settings.LOGS_ROOT,'ownphotos.log'),
    maxBytes=fileMaxByte, backupCount=10)
fileHandler.setFormatter(fomatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)



def convert_to_degrees(values):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(values[0].num) / float(values[0].den)
    m = float(values[1].num) / float(values[1].den)
    s = float(values[2].num) / float(values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

weekdays = {1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}



def compute_bic(kmeans,X):
    """
    Computes the BIC metric for a given clusters

    Parameters:
    -----------------------------------------
    kmeans:  List of clustering object from scikit learn

    X     :  multidimension np array of data points

    Returns:
    -----------------------------------------
    BIC value
    """
    # assign centers and labels
    centers = [kmeans.cluster_centers_]
    labels  = kmeans.labels_
    #number of clusters
    m = kmeans.n_clusters
    # size of the clusters
    n = np.bincount(labels)
    #size of data set
    N, d = X.shape

    #compute variance for all clusters beforehand
    cl_var = (1.0 / (N - m) / d) * sum([sum(distance.cdist(X[np.where(labels == i)], [centers[0][i]], 
             'euclidean')**2) for i in range(m)])

    const_term = 0.5 * m * np.log(N) * (d+1)

    BIC = np.sum([n[i] * np.log(n[i]) -
        n[i] * np.log(N) -
        ((n[i] * d) / 2) * np.log(2*np.pi*cl_var) -
        ((n[i] - 1) * d/ 2) for i in range(m)]) - const_term

    return(BIC)

def mapbox_reverse_geocode(lat,lon):
    mapbox_api_key = "pk.eyJ1IjoibGdlenl4ciIsImEiOiJja2p1OGt4dXAwbmo1MnpvOG5kZWZ4OXhvIn0.pkULFA2Fm8vguK7YRR3Gmw"
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%f,%f.json?access_token=%s"%(lon,lat,mapbox_api_key)
    resp = requests.get(url)
    if resp.status_code == 200:
        resp_json = resp.json()
        search_terms = []

        if 'features' in resp_json.keys():
            for feature in resp_json['features']:
                search_terms.append(feature['text'])

        resp_json['search_text'] = ' '.join(search_terms)
        logger.info('mapbox returned status 200.')
        return resp_json
    else:
        # logger.info('mapbox returned non 200 response.')
        logger.warning('mapbox returned status {} response.'.format(resp.status_code))
        return {}

def get_prediction_from_api(image_path):
    api_url = "http://35.222.127.213:8003/webAPI"
    with open(image_path, "rb") as a_file:
        file_dict = {"images" : a_file}
        logger.info('read image, sending to prediction api')
        response = requests.post(api_url, files = file_dict)
        return response.json()
    return {"error": True}
    
