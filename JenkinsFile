pipeline {
    agent any

    environment {
        POSTGRES_DB = 'test_db_ci'
        TEST_IMAGE = "fastapi-test:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                cleanWs()
                git branch: 'master', url: 'https://github.com/DrinkingWater64/FastApiCleanArcTemplate'
            }
        }

        stage('Build Test Image') {
            steps {
                script {
                    echo '--- Building Image with Dev Dependencies ---'
                    sh "podman build --target testing -t ${TEST_IMAGE} ."
                }
            }
        }

        stage('Run Tests with Fresh DB') {
            steps {
                script {
                    def netName = "jenkins-net-${BUILD_NUMBER}"

                    try {
                        echo '--- Setting up Ephemeral Network & DB ---'

                        sh "podman network create ${netName}"

                        sh """
                            podman run -d \
                                --name db-${BUILD_NUMBER} \
                                --network ${netName} \
                                --network-alias db \
                                -e POSTGRES_USER=${POSTGRES_USER} \
                                -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                                -e POSTGRES_DB=${POSTGRES_DB} \
                                docker.io/library/postgres:15-alpine
                        """

                        sh "sleep 5"

                        echo '--- Running Pytest ---'

                        sh """
                            podman run --rm \
                                --network ${netName} \
                                -e DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}" \
                                ${TEST_IMAGE} \
                                uv run pytest tests
                        """

                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        throw e
                    } finally {
                        echo '--- Teardown: Dropping DB & Network ---'
                        sh "podman stop db-${BUILD_NUMBER} || true"
                        sh "podman rm db-${BUILD_NUMBER} || true"
                        sh "podman network rm ${netName} || true"
                        sh "podman rmi ${TEST_IMAGE} || true"
                    }
                }
            }
        }
    }
}
