pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Essay-HS/selenium-test-site.git'
            }
        }

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

            post {
    always {
        script {
            def reportFile = 'test-results/results.xml'

            if (fileExists(reportFile)) {
                def results = readFile(reportFile)

                def tests = (results =~ /tests="(\d+)"/)[0][1].toInteger()
                def failures = (results =~ /failures="(\d+)"/)[0][1].toInteger()
                def errors = (results =~ /errors="(\d+)"/)[0][1].toInteger()
                def skipped = (results =~ /skipped="(\d+)"/)[0][1].toInteger()

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
                script: 'git rev-parse HEAD',
                returnStdout: true
            ).trim()

            def jenkinsStatus = currentBuild.currentResult ?: 'SUCCESS'

            env.RELEASEGUARD_STATUS =
                jenkinsStatus == 'FAILURE' ? 'FAILED' : jenkinsStatus
        }

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

    post {
        always {
            sh '''
                if [ -f flask.pid ]; then
                    kill $(cat flask.pid) 2>/dev/null || true
                    rm -f flask.pid
                fi
            '''
        }
    }
}
