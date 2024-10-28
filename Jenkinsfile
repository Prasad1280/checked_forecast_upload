pipeline {
    agent any

    parameters {
        choice(
            name: 'Report_Category',
            choices: ['Best_Case', 'Market'],
            description: 'Select the Forecast Level'
        )
        file(name: 'INPUT_FILE', description: 'Upload your Excel/CSV file')
    }

    stages {
        stage('Process Upload') {
            steps {
                script {
                    // Get the name of the uploaded file
                    def uploadedFile = params.INPUT_FILE.split('/')[-1]
                    echo "Processing uploaded file: ${uploadedFile}"
                }
            }
        }
        
        stage('Activate FS Environment') {
            steps {
                sh '/home/ef_user/miniconda3/bin/activate /home/ef_user/miniconda3/envs/stretto_ML' 
            }
        }
        
        stage('Accuracy_Calculation') {
            steps {
                script {
                    def uploadedFile = params.INPUT_FILE.split('/')[-1]
                    sh "/home/ef_user/miniconda3/envs/stretto_ML/bin/python Checked_forecast_upload.py ${Report_Category} '${uploadedFile}'"
                }
            }
            post {
                success {
                    // archiveArtifacts artifacts: "**/*.xlsx", onlyIfSuccessful: true
                    archiveArtifacts artifacts: "**/*.csv", onlyIfSuccessful: true
                }
            }
        }
        
        stage('Deactivate FS Environment') {
            steps {
                sh '/home/ef_user/miniconda3/bin/deactivate /home/ef_user/miniconda3/envs/stretto_ML'
            }
        }
    }
}