pipeline {
    agent any

    parameters {
        choice(
            name: 'Report_Category',
            choices: ['Best_Case', 'Market'],
            description: 'Enter the Forecast Level'
        )
        file(name: 'INPUT_FILE', description: 'Upload your Excel/CSV file')
    }

    environment {
        // Define the conda environment path as an environment variable for easy access
        CONDA_ENV_PATH = '/home/ef_user/miniconda3/envs/stretto_ML'
        CONDA_EXEC_PATH = '/home/ef_user/miniconda3/bin'
    }

    stages {
        stage('Activate FS Environment') {
            steps {
                sh "source ${env.CONDA_EXEC_PATH}/activate ${env.CONDA_ENV_PATH}"
            }
        }

        stage('File_Preparation_for_db') {
            steps {
                script {
                    // Construct the full path to the input file
                    def inputFile = "${WORKSPACE}/${params.INPUT_FILE}"
                    echo "Input file path: ${inputFile}"

                    // Ensure the input file exists
                    sh '''
                    if [ ! -f "${inputFile}" ]; then
                        echo "Input file not found at ${inputFile}"
                        exit 1
                    fi
                    '''

                    // Run the Python script with the correct input file path
                    sh "${env.CONDA_ENV_PATH}/bin/python Checked_forecast_upload.py ${params.Report_Category} ${inputFile}"
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: "**/*.csv", onlyIfSuccessful: true
                }
                failure {
                    echo 'File preparation failed.'
                }
            }
        }

        stage('Deactivate FS Environment') {
            steps {
                sh "source ${env.CONDA_EXEC_PATH}/deactivate"
            }
        }
    }
}
