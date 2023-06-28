import logging

from .constants import DATASETS_ENDPOINT, DATASET_BY_ID_ENDPOINT, \
    DATASET_DOCUMENTS_ENDPOINT, DATASET_DOCUMENT_BY_ID_ENDPOINT, TRAINING_JOBS_ENDPOINT, TRAINING_JOB_BY_ID_ENDPOINT, \
    MODELS_ENDPOINT, MODEL_BY_NAME_ENDPOINT, MODEL_BY_VERSION_ENDPOINT, \
    DEPLOYMENTS_ENDPOINT, DEPLOYMENT_BY_ID_ENDPOINT, INFERENCE_JOBS_ENDPOINT, INFERENCE_JOB_BY_ID_ENDPOINT, \
    BATCH_INFERENCE_JOB_BY_ID_ENDPOINT
from .http_client_base import CommonClient


class BER_API_Client(CommonClient):
    """
    This class provides an interface to access SAP Business Entity Recognition REST API from a Python application.
    Structure of values returned by all the methods is documented in Swagger. See Swagger UI by adding:
    /api/v1 to your Business Entity Recognition service key URL value (from outside the uaa section).

    :param base_url: The service URL taken from the service key (key 'url' in service key JSON)
    :param client_id: The client ID taken from the service key (key 'uaa.clientid' in service key JSON)
    :param client_secret: The client secret taken from the service key (key 'uaa.clientsecret' in service key JSON)
    :param uaa_url: The XSUAA URL taken from the service key (key 'uaa.url' in service key JSON)
    produce any logs
    """

    def __init__(self,
                 base_url,
                 client_id,
                 client_secret,
                 uaa_url,
                 logging_level=logging.WARNING):

        logger = logging.getLogger('BERApiClient')
        logger.setLevel(logging_level)
        CommonClient.__init__(self,
                              base_url=base_url,
                              client_id=client_id,
                              client_secret=client_secret,
                              uaa_url=uaa_url,
                              url_path_prefix='api/v1/',
                              logging_level=logging_level)
        self.logger = logger

    # Datasets
    def get_datasets(self):
        """
        Gets summary information about the existing datasets
        :return: Object containing an array of datasets
        """
        self.logger.debug('Getting information about datasets')
        response = self.session.get(self.path_to_url(DATASETS_ENDPOINT))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the datasets')
        return response

    # Dataset
    def create_dataset(self, dataset_type="training"):
        """
        Creates an empty dataset
        :return: Object containing the dataset id
        """
        self.logger.debug('Creating a new dataset')
        response = self.session.post(self.path_to_url(DATASETS_ENDPOINT),
                                     json={"datasetType": dataset_type})
        response.raise_for_status()
        self.logger.info('Successfully created a new dataset')
        return response

    def get_dataset(self, dataset_id):
        """
        Gets statistical information about a dataset with a given ID
        :param dataset_id: The ID of the dataset
        :return: Summary information about the dataset that includes the number of documents in different processing
        stages
        """
        self.logger.debug('Getting information about the dataset {}'.format(dataset_id))
        response = self.session.get(self.path_to_url(DATASET_BY_ID_ENDPOINT(dataset_id=dataset_id)))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the dataset {}'.format(dataset_id))
        return response

    def delete_dataset(self, dataset_id):
        """
        Deletes a dataset with a given ID
        :param dataset_id: The ID of the dataset to delete
        :return: Object containing the ID of the deleted dataset and the number of documents deleted
        """
        self.logger.debug('Deleting the dataset {}'.format(dataset_id))
        response = self.session.delete(self.path_to_url(DATASET_BY_ID_ENDPOINT(dataset_id=dataset_id)))
        response.raise_for_status()
        self.logger.info('Successfully deleted the dataset {}'.format(dataset_id))
        return response

    # Documents
    def get_dataset_documents(self, dataset_id):
        """
        Gets the information about all the documents in a specific dataset
        :param dataset_id: The ID of an existing dataset
        :return: Object that contains array of the documents
        """
        self.logger.debug('Getting information about the documents in the dataset {}'.format(dataset_id))
        response = self.session.get(self.path_to_url(DATASET_DOCUMENTS_ENDPOINT(dataset_id=dataset_id)))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the documents in the dataset {}'.format(dataset_id))
        return response

    # Document
    def upload_document_to_dataset(self, dataset_id, document_path):
        """
        Uploads a single document and its ground truth to a specific dataset
        :param dataset_id: The ID of the dataset
        :param document_path: The path to the document
        :return: Object containing information about the uploaded document
        """

        self.logger.debug('Uploading the document {} to the dataset {}'.format(
            document_path, dataset_id))
        document_name = document_path.split("/")[-1]
        response = self.session.post(self.path_to_url(DATASET_DOCUMENTS_ENDPOINT(dataset_id=dataset_id)),
                                     files={'document': (document_name, open(document_path, 'rb'), "application/json")})
        response.raise_for_status()
        self.logger.debug('Successfully uploaded the document {} to the dataset {}, waiting for '
                          'the document processing'.format(document_path, dataset_id))
        return response

    def get_dataset_document(self, dataset_id, document_id):
        """
        Gets the information about all the documents in a specific dataset
        :param dataset_id: The ID of an existing dataset
        :param document_id: The reference ID of the document
        :return: Object that contains array of the documents
        """
        self.logger.debug('Getting information about the document {} in the dataset {}'.format(document_id, dataset_id))
        response = self.session.get(self.path_to_url(DATASET_DOCUMENT_BY_ID_ENDPOINT(dataset_id=dataset_id,
                                                                                     document_id=document_id)))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the document {} in the dataset {}'.format(document_id,
                                                                                                           dataset_id))
        return response

    def delete_dataset_document(self, dataset_id, document_id):
        """
        Deletes a training document from a dataset
        :param dataset_id: The ID of the dataset where the document is located
        :param document_id: The reference ID of the document
        :return: response
        """
        self.logger.debug('Deleting the document {} from the dataset {}'.format(document_id, dataset_id))
        response = self.session.delete(
            self.path_to_url(DATASET_DOCUMENT_BY_ID_ENDPOINT(dataset_id=dataset_id, document_id=document_id)))
        response.raise_for_status()
        self.logger.info('Successfully deleted the document {} from the dataset {}'.format(document_id, dataset_id))
        return response

    # Training
    def train_model(self, model_name, dataset_id):
        """
        Trigger the process to train a new model for BER, based on the documents in the
        specific dataset and wait until this process is finished. The process may take significant time to complete
        depending on the size of the dataset.
        :param model_name: The name of the new model to train
        :param dataset_id: The name of existing dataset containing enough documents for training
        :return: Object containing success or error message
        """
        self.logger.debug('Triggering training of the model {} from the dataset {}'.format(model_name, dataset_id))
        response = self.session.post(self.path_to_url(TRAINING_JOBS_ENDPOINT),
                                     json={"datasetId": dataset_id,
                                           "modelName": model_name})
        response.raise_for_status()
        self.logger.info('Triggered training of the model {} from the dataset {}, waiting for the training to complete'
                         .format(model_name, dataset_id))
        return response

    def get_training_status(self, job_id):
        """
        Get status detail of an ongoing training
        :param job_id: The job id of training job
        :return: Object containing the status detail the training
        """
        self.logger.debug('getting training of job {}'.format(job_id))
        response = self.session.get(self.path_to_url(TRAINING_JOB_BY_ID_ENDPOINT(job_id=job_id)))
        response.raise_for_status()
        return response

    def delete_ongoing_training(self, job_id):
        """
        Deletes an ongoing training
        :param job_id: The job id of training job
        :return: Object containing the success or error message
        """
        self.logger.debug('getting training of job {}'.format(job_id))
        response = self.session.delete(self.path_to_url(TRAINING_JOB_BY_ID_ENDPOINT(job_id=job_id)))
        response.raise_for_status()
        return response

    def get_recently_submitted_training_jobs_list(self):
        """
        Fetches the list of recently submitted training jobs (~12 Hour interval)
        :return: Object containing the list of training jobs
        """
        self.logger.debug('getting list of recently submitted training jobs')
        response = self.session.get(self.path_to_url(TRAINING_JOBS_ENDPOINT))
        response.raise_for_status()
        return response

    # Models
    def get_trained_models(self):
        """
        Gets information about all trained models
        :return: Object containing the array of all trained models, each model information contains training status and
        training accuracy data
        """
        self.logger.debug('Getting information about all trained models')
        response = self.session.get(self.path_to_url(MODELS_ENDPOINT))
        response.raise_for_status()
        self.logger.info('Successfully got information about all trained models')
        return response

    # Model Versions
    def get_trained_model_versions(self, model_name):
        """
        Gets information about a specific trained model
        :param model_name: The name of the model
        :return: Object containing all versions of the model with the training status and training accuracy data
        """
        self.logger.debug('Getting information about the model {}'.format(model_name))
        response = self.session.get(self.path_to_url(MODEL_BY_NAME_ENDPOINT(model_name=model_name)))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the model {}'.format(
            model_name))
        return response

    # Model Version
    def get_trained_model_version(self, model_name, model_version):
        """
        Gets information about a specific trained model
        :param model_name: The name of the model
        :param model_version: The version of the model
        :return: Object containing the training status and training accuracy data
        """
        self.logger.debug('Getting information about the model {} with version {}'.format(model_name, model_version))
        response = self.session.get(self.path_to_url(MODEL_BY_VERSION_ENDPOINT(model_name=model_name,
                                                                               model_version=model_version)))
        response.raise_for_status()
        self.logger.info('Successfully got the information about the model {} with version {}'.format(model_name,
                                                                                                      model_version))
        return response

    def delete_trained_model_version(self, model_name, model_version):
        """
        Deletes an existing trained model
        :param model_name: Name of the existing model to delete
        :param model_version: Version of the existing model to delete
        :return: Object containing the message of success or error
        """
        self.logger.debug('Triggering deletion of the model {} with version {}'.format(model_name, model_version))
        response = self.session.delete(
            self.path_to_url(MODEL_BY_VERSION_ENDPOINT(model_name=model_name, model_version=model_version)))
        response.raise_for_status()
        self.logger.info('Successfully deleted the model {} with version {}'.format(model_name, model_version))
        return response

    # Deployment
    def deploy_model(self, model_name, model_version):
        """
        Deploys a trained model to be available for inference
        :param model_name: The name of the trained model
        :param model_version: The version of the trained model
        :return: Object containing information about the deployed model serving
        """
        self.logger.debug('Triggering the deployment of the model {} with version {}'.format(model_name, model_version))
        response = self.session.post(self.path_to_url(DEPLOYMENTS_ENDPOINT), json={
                                                                                    "modelName": model_name,
                                                                                    "modelVersion": model_version
                                                                                    })
        response.raise_for_status()
        self.logger.info('Successfully triggered the deployment of the model {} with version {}, waiting for '
                         'the deployment completion'.format(model_name, model_version))
        return response

    def get_deployed_model(self, deployment_id):
        """
        Gets information about a specific deployed model.
        :param deployment_id: ID of the deployed model
        :return: Object containing the information about the deployed model serving
        """

        # todo: code can be changed to fetch the version directly

        self.logger.debug('Getting the deployment of the deployment id {}'.format(
            deployment_id))

        response = self.session.get(self.path_to_url(DEPLOYMENT_BY_ID_ENDPOINT(deployment_id=deployment_id)))

        self.logger.info('Successfully got information about the deployment of the deployment id {}'.format(
            deployment_id))

        return response

    def undeploy_model(self, deployment_id):
        """
        Removes a deployment of the specific model.
        :param deployment_id: ID of the deployed model
        :return: response with details of undeployed model
        """

        self.logger.debug(
            'Triggering the removal of the model deployment with ID {}'.format(deployment_id))
        response = self.session.delete(self.path_to_url(DEPLOYMENT_BY_ID_ENDPOINT(deployment_id=deployment_id)))
        # response.raise_for_status()
        self.logger.info('Successfully triggered the removal of the model deployment with ID {}, waiting for '
                         'the deployment completion'.format(deployment_id))

        return response

    def get_deployments(self):
        """
        See information about all deployed models.
        :return: Object containing information about the deployed models
        """
        self.logger.debug('Triggering the get deployments')
        response = self.session.get(self.path_to_url(DEPLOYMENTS_ENDPOINT))
        response.raise_for_status()
        self.logger.info('Successfully received the deployment details')
        return response

    # Inference
    def post_inference_job(self, text, model_name, model_version):
        """
        Triggers inference job
        :param text: The name of the new model to train
        :param model_name: The name of existing model
        :param model_version: The version of existing model
        :return: Object containing the job details
        """
        self.logger.debug('Submitting inference job')
        response = self.session.post(self.path_to_url(INFERENCE_JOBS_ENDPOINT),
                                     json={"text": text,
                                           "modelName": model_name,
                                           "modelVersion": model_version})
        response.raise_for_status()
        self.logger.info('Submitted inference job successfully')
        return response

    def get_inference_job(self, job_id):
        """
        Gets information about inference job
        :param job_id: Inference Job ID
        :return: Object containing the predicted result
        """
        self.logger.debug('Getting inference job information')
        response = self.session.get(self.path_to_url(INFERENCE_JOB_BY_ID_ENDPOINT(job_id=job_id)))
        response.raise_for_status()
        self.logger.info('Received inference job details successfully')
        return response

    def post_batch_inference_job(self, dataset_id, model_name, model_version):
        """
        Triggers batch inference job
        :param dataset_id: Id of the inference dataset
        :param model_name: The name of existing model
        :param model_version: The version of existing model
        :return:
        """
        self.logger.debug('Submitting batch inference job')
        response = self.session.post(self.path_to_url(INFERENCE_JOBS_ENDPOINT),
                                     json={"datasetId": dataset_id,
                                           "modelName": model_name,
                                           "modelVersion": model_version})
        response.raise_for_status()
        self.logger.info('Submitted batch inference job successfully')
        return response

    def get_batch_inference_job_result(self, job_id):
        """
        Gets results of batch inference job
        :param job_id: Inference Job ID
        :return: Object containing the predicted result
        """
        self.logger.debug('Getting inference job information')
        response = self.session.get(self.path_to_url(BATCH_INFERENCE_JOB_BY_ID_ENDPOINT(job_id=job_id)))
        response.raise_for_status()
        self.logger.info('Received batch inference job details successfully')
        return response
