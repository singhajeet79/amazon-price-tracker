pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('github-token')
        SCANNER_HOME = tool 'sonar-scanner'
        ///placeholder for artifactory
    }

    stages {
        stage('Clean workspace') {
            steps {
                deleteDir()
            }
        }
    
        stage('Checkout') {
            steps {
                git url: 'https://github.com/singhajeet79/amazon-price-tracker.git', branch: 'main'
            }
        }
        stage('Run Pylint') {
            steps {
                script {
                    try {
                        sh 'pylint **/*.py'
                    } catch (Exception e) {
                        echo 'Linting failed'
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
        stage('Run MyPy') {
            steps {
                script {
                    try {
                        sh 'mypy *.py'
                    } catch (Exception e) {
                        echo 'Type checking failed'
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
        stage('Trigger GitHub Actions Workflow') {
            steps {
                script {
                    def response = sh(script: """
                        curl -X POST \
                        -H "Authorization: token ${env.GITHUB_TOKEN}" \
                        -H "Accept: application/vnd.github.v3+json" \
                        https://api.github.com/repos/singhajeet79/amazon-price-tracker/actions/workflows/pre-commit.yml/dispatches \
                        -d '{\"ref\":\"main\"}'
                    """, returnStdout: true).trim()
                    echo "Response from GitHub: ${response}"
                }
            }
        }
        /*stage('Run Bandit Security Scan') {
            steps {
                script {
                    try {
                        sh 'bandit -r .'
                  } catch (Exception e) {
                    echo 'Security scan failed'
                    currentBuild.result = 'FAILURE'
                    throw e
                  }
                }
            }
        }*/
        stage('Approval') {
            steps {
                script {
                    // Prompt for approval from Development Lead
                    input message: 'Pipeline execution requires approval. Please review and approve.', submitter: 'Development Lead'
                }
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                withSonarQubeEnv("sonar") {
                    sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=amazonPriceTracker -Dsonar.projectKey=amazonPriceTracker"
                }
            }
        }
        stage("Quality Gate") {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
                }
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage("TRIVY FS SCAN") {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker'){   
                       sh "docker build -t price-tracker-app ."
                       sh "docker tag price-tracker-app ajeetsingh77/price-tracker-app:latest "
                       sh "docker push ajeetsingh77/price-tracker-app:latest"
                    }    
                }
            }
        }
        stage("TRIVY"){
            steps{
                sh "trivy image ajeetsingh77/price-tracker-app:latest > trivyimage.txt" 
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    docker.image('price-tracker-app').inside {
                        sh 'python3 -m unittest discover -s tests -p "*_test.py"'
                    }
                }
            }
        }
        
    }
}
