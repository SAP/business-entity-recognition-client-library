from functools import partial


# health
MONITORING_HEALTH_CHECK_ENDPOINT = 'health'


# datasets
DATASETS_ENDPOINT = 'datasets'                                                              # post and get
DATASET_BY_ID_ENDPOINT = partial('datasets/{dataset_id}'.format)                                  # get and delete


# documents
DATASET_DOCUMENTS_ENDPOINT = partial('datasets/{dataset_id}/documents'.format)              # post and get
DATASET_DOCUMENT_BY_ID_ENDPOINT = partial('datasets/{dataset_id}/documents/{document_id}'.format)  # get and delete


# trainings
TRAINING_JOBS_ENDPOINT = 'training/jobs'                                                    # post
TRAINING_JOB_BY_ID_ENDPOINT = partial('training/jobs/{job_id}'.format)                             # get and delete


# models
MODELS_ENDPOINT = 'models'                                                                  # get
MODEL_BY_NAME_ENDPOINT = partial('models/{model_name}/versions'.format)                     # get
MODEL_BY_VERSION_ENDPOINT = partial('models/{model_name}/versions/{model_version}'.format)       # get and delete


# deployments
DEPLOYMENTS_ENDPOINT = 'deployments'                                                        # post and get
DEPLOYMENT_BY_ID_ENDPOINT = partial('deployments/{deployment_id}'.format)                          # get and delete


# inference
INFERENCE_JOBS_ENDPOINT = 'inference/jobs'                                                           # post
INFERENCE_JOB_BY_ID_ENDPOINT = partial('inference/jobs/{job_id}'.format)
BATCH_INFERENCE_JOB_BY_ID_ENDPOINT = partial('inference/jobs/{job_id}/document'.format)
# get

STATUS_SUCCEEDED = 'SUCCEEDED'
STATUS_FAILED = 'FAILED'

# API_PAGINATION_TOP_PARAM = 'top'
# API_PAGINATION_SKIP_PARAM = 'skip'
# API_PAGINATION_COUNT_PARAM = 'count'

# API_MIME_TYPE_FIELD = 'mimeType'
# API_DOCUMENT_EXTRACTED_TEXT_FIELD = 'extractedText'
# API_DOCUMENT_ID_FIELD = 'documentId'
# API_STATUS_FIELD = 'status'

# PDF_MIME_TYPE = 'pdf'

# MAX_POLLING_THREADS = 15
# MIN_POLLING_INTERVAL = 0.2
