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
    
    stages {
        stage('Activate FS Environment') {
            steps {
                sh '/home/ef_user/miniconda3/bin/activate /home/ef_user/miniconda3/envs/stretto_ML'
            }
        }
        
        stage('File_Preparation_for_db') {
            steps {
                script {
                    // Copy uploaded file to workspace with expected name
                    // sh 'cp "${INPUT_FILE}" input_file.xlsx'
                    // Run Python script with proper parameter handling
                    sh "/home/ef_user/miniconda3/envs/stretto_ML/bin/python Checked_forecast_upload.py ${params.Report_Category}"
                }
            }
            post {
                success {
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