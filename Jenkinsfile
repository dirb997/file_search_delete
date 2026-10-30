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
                // Bump the version 
                sh '''
                    python3 -c'
                    with open("VERSION", "r") as f:
                        version = f.read().strip()
                    parts = list(map(int, version.split(".")))
                    parts[2] += 1  # Increment the patch version
                    new_version = ".".join(map(str, parts))
                    with open("VERSION", "w") as f:
                        f.write(new_version)
                    print(f"Version bumped to {new_version}")
                '''
            }

        }

        stage('Push Changes and tag to GitHub') {
            steps {
                // Push the changes back to GitHub
                sh '''
                    NEW_VERSION=$(cat VERSION)

                    REPO_URL=$(git config --get remote.origin.url | sed -e "s/^https:\\/\\//https:\\/\\/$(echo $GITHUB_CREDENTIALS_USR):$(echo $GITHUB_CREDENTIALS_PSW)@/")

                    git add VERSION
                    git commit -m "Bump version to $NEW_VERSION"
                    git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
                    git push ${REPO_URL} HEAD:main --tags
                '''
            }
        }
    }
}
