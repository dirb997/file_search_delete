pipeline {
    agent any

    environment {
        // We'll define environment variables here
        GITHUB_CREDENTIALS = credentials('github-pat-creds')
        
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from GitHub
                checkout scm
            }
        }

        stage('Configure Git') {
            steps {
                // Configure Git with the provided credentials
                sh '''
                    git config --global user.name "Jenkins CI"
                    git config --global user.email "jenkins@buildserver.com"
                '''
            }
        }

        stage('Bump Version and Build') {
            steps {
                // Bump the version in package.json
                sh '''
                    npm version patch -m "Bump version to %s [ci skip]"
                '''
            }
            post {
                success {
                    echo 'Version bumped successfully.'
                }
            }
        }

        stage('Push Changes and tag to GitHub') {
            steps {
                // Push the changes back to GitHub
                sh '''
                    # Extract the repository URL from the remote
                    REPO_URL=$(git config --get remote.origin.url) | sed -e "s#https://#https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@#"
                    git push ${REPO_URL} HEAD:${BRANCH_NAME} --tags
                '''
            }

            post {
                success {
                    echo 'Changes pushed and tagged successfully.'
                }
            }
        }
    }
}
