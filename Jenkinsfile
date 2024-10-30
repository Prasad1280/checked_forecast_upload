pipeline {
    agent any

    parameters {
        choice(
            name: 'Report_Category',
            choices: ['Best_Case', 'Market'],
            description: 'Enter the Forecast Level'
        )
        file(
            name: 'Input_File',
            description: 'Upload the .xlsx input file'
        )
    }

    stages {
        stage('Activate FS Environment') {
            steps {
                sh '/home/ef_user/miniconda3/bin/activate /home/ef_user/miniconda3/envs/stretto_ML'
            }
        }
        stage('Final_Forecasts_processing_and_upload') {
            steps {
                script {
                    sh "/home/ef_user/miniconda3/envs/stretto_ML/bin/python Checked_forecast_upload.py ${params.Report_Category}"
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

