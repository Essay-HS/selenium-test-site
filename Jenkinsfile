pipeline {
    agent any

    stages {
        stage('Prepare Python') {
            steps {
                sh '''
                    python3.12 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Start Flask') {
            environment {
                DB_PASSWORD = credentials('selenium-db-password')
                DB_USER = 'root'
                DB_HOST = '127.0.0.1'
                DB_PORT = '3306'
            }

            steps {
                sh '''
                    .venv/bin/python app.py > flask.log 2>&1 &
                    echo $! > flask.pid

                    for i in 1 2 3 4 5 6
                    do
                        if curl --fail --silent http://127.0.0.1:5000 > /dev/null
                        then
                            echo "Flask is ready"
                            exit 0
                        fi

                        echo "Waiting for Flask..."
                        sleep 5
                    done

                    echo "Flask did not start"
                    cat flask.log
                    exit 1
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p test-results

                    HEADLESS=true .venv/bin/python -m pytest -v \
                        --junitxml=test-results/results.xml
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results/results.xml',
                  allowEmptyResults: true

            script {
                try {
                    def reportFile = 'test-results/results.xml'

                    if (fileExists(reportFile)) {
                        def results = readFile(reportFile)

                        def tests =
                            (results =~ /tests="(\d+)"/)[0][1].toInteger()

                        def failures =
                            (results =~ /failures="(\d+)"/)[0][1].toInteger()

                        def errors =
                            (results =~ /errors="(\d+)"/)[0][1].toInteger()

                        def skipped =
                            (results =~ /skipped="(\d+)"/)[0][1].toInteger()

                        env.PASSED_TESTS =
                            (tests - failures - errors - skipped).toString()

                        env.FAILED_TESTS =
                            (failures + errors).toString()
                    } else {
                        env.PASSED_TESTS = '0'
                        env.FAILED_TESTS = '0'
                    }

                    env.BRANCH_NAME = 'main'

                    env.GIT_COMMIT = sh(
                        script: 'git rev-parse HEAD 2>/dev/null || echo unknown',
                        returnStdout: true
                    ).trim()

                    def jenkinsStatus =
                        currentBuild.currentResult ?: 'SUCCESS'

                    env.RELEASEGUARD_STATUS =
                        jenkinsStatus == 'FAILURE'
                            ? 'FAILED'
                            : jenkinsStatus

                    try {
                        withCredentials([
                            string(
                                credentialsId: 'releaseguard-api-token',
                                variable: 'BUILD_API_TOKEN'
                            )
                        ]) {
                            sh '''
                                export RELEASEGUARD_URL=http://127.0.0.1:5001

                                /Users/ac/Projects/releaseguard/.venv/bin/python \
                                    /Users/ac/Projects/releaseguard/scripts/record_build.py \
                                    "$RELEASEGUARD_STATUS"
                            '''
                        }
                    } catch (Exception error) {
                        echo 'WARNING: ReleaseGuard reporting failed.'
                        echo 'The original Jenkins build result will be preserved.'
                        echo "Reporting error: ${error.getMessage()}"
                    }
                    if (
                        env.RELEASEGUARD_STATUS in [
                            'FAILED',
                            'UNSTABLE',
                            'ABORTED'
                        ]
                    ) {
                        try {
                            withCredentials([
                                string(
                                    credentialsId: 'twilio-live-account-sid',
                                    variable: 'TWILIO_ACCOUNT_SID'
                                ),
                                string(
                                    credentialsId: 'twilio-live-auth-token',
                                    variable: 'TWILIO_AUTH_TOKEN'
                                ),
                                string(
                                    credentialsId: 'TWILIO_PHONE_NUMBER',
                                    variable: 'TWILIO_PHONE_NUMBER'
                                ),
                                string(
                                    credentialsId: 'ALERT_PHONE_NUMBER',
                                    variable: 'ALERT_PHONE_NUMBER'
                                )
                            ]) {
                                sh '''
                                    /Users/ac/Projects/releaseguard/.venv/bin/python \
                                        /Users/ac/Projects/releaseguard/scripts/send_twilio_alert.py \
                                        "$RELEASEGUARD_STATUS"
                                '''
                            }
                        } catch (Exception error) {
                            echo 'WARNING: Twilio alert failed.'
                            echo 'The Jenkins build result will be preserved.'
                            echo "Twilio error: ${error.getMessage()}"
                        }
                    } else {
                        echo 'Build succeeded. No Twilio alert is required.'
                    }

                } finally {
                    sh '''
                        if [ -f flask.pid ]; then
                            kill $(cat flask.pid) 2>/dev/null || true
                            rm -f flask.pid
                        fi
                    '''
                }
            }
        }
    }
}
