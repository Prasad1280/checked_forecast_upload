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
        stage('Copy Input File') {
            steps {
                script {
                    // Copy uploaded file to workspace
                    sh "cp ${params.INPUT_FILE} ${WORKSPACE}/"
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
                    sh "/home/ef_user/miniconda3/envs/stretto_ML/bin/python Checked_forecast_upload.py ${Report_Category} ${params.INPUT_FILE}"
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