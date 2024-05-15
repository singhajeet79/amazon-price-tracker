pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('github-token')
    }
    stages {
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
        stage('Run Bandit Security Scan') {
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
        }
    }
}

