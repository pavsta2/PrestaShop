pipeline {
    agent any
    parameters {
        choice (
            name: "BROWSER",
            choices: 'chrome\nfirefox',
            description: "Browser name for autotests"
        )
        choice (
            name: "LOG_LEVEL",
            choices: 'INFO\nDEBUG',
            description: "Set log level"
        )
        choice (
            name: "BROWSER_VER",
            choices: '128.0\n127.0',
            description: "Set browser version"
        )
        string (
            name: "XDIST",
            defaultValue: '2',
            description: "Set a number of workers"
        )
        string (
            name: "REMOTE_URL",
            defaultValue: 'http://selenoid4:4444/wd/hub',
            description: "Remote url"
        )
    }
    environment {
        // --- База данных ---
        DB_HOST = 'some-mysql'
        DB_NAME = 'prestashop'
        DB_USER = 'root'
        DB_PASS = 'admin'

        // --- PrestaShop ---
        PS_ADMIN_DIR = 'admin_$(openssl rand -hex 6)'  // будет заменён на конкретное имя
        PS_ADMIN_DIR_FIXED = 'admin_8k3j29smxqkl'      // фиксированное имя для стабильности

        // --- API ---
        PS_API_KEY = ''

        // --- Тесты и Allure ---
        TEST_IMAGE = 'presta_tests:latest'         // замените на имя вашего образа
        ALLURE_RESULTS = 'allure-results'
        ALLURE_REPORT = 'allure-report'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git branch: 'remote_start',
                    url: 'https://github.com/pavsta2/PrestaShop.git'
            }
        }
        stage('Build Test Image with Fresh Code') {
            steps {
                sh '''
                echo "Сборка образа с тестами"
                /usr/bin/docker build -t ${TEST_IMAGE} .
                '''
            }
        }

        stage('Запуск всей инфраструктуры') {
            steps {
                script {
                    echo 'Запуск docker-compose...'
                    sh 'docker compose -f ${COMPOSE_FILE} up -d'


                }
            }
        }

        stage('Настройка безопасности PrestaShop') {
            steps {
                script {
                    echo 'Удаление папки /install...'
                    sh 'docker exec -t prestashop rm -rf /var/www/html/install* || true'

                    echo 'Переименование /admin...'
                    sh """
                        if docker exec -t prestashop [ -d /var/www/html/admin ] && ! docker exec -t prestashop [ -d /var/www/html/${PS_ADMIN_DIR_FIXED} ]; then
                            docker exec -t prestashop mv /var/www/html/admin /var/www/html/${PS_ADMIN_DIR_FIXED}
                        fi
                    """
                    echo "Админка доступна по: http://localhost:8080/${PS_ADMIN_DIR_FIXED}"
                }
            }
        }

        stage('Активация Webservice и создание API-ключа (полный доступ)') {
            steps {
                script {
                    echo 'Генерация API-ключа с полными правами...'

                    // Получаем _COOKIE_KEY_
                    def cookieKey = sh(
                        script: "docker exec -t prestashop grep _COOKIE_KEY_ /var/www/html/config/settings.inc.php | cut -d '\"' -f 2",
                        returnStdout: true
                    ).trim()

                    if (!cookieKey) {
                        error '_COOKIE_KEY_ не найден'
                    }

                    // Генерируем API-ключ
                    def apiKey = sh(script: 'openssl rand -hex 16', returnStdout: true).trim()
                    env.PS_API_KEY = apiKey

                    // Хешируем ключ
                    def hashedKey = sh(
                        script: "php -r \"echo md5('${apiKey}' . '${cookieKey}');\"",
                        returnStdout: true
                    ).trim()

                    if (!hashedKey) {
                        error 'Не удалось сгенерировать хеш API-ключа'
                    }

                    echo "Открытый ключ: ${apiKey}"
                    echo "Хешированный ключ: ${hashedKey}"

                    // Получаем ID магазина (исправлено: без мусора в stderr)
                    def shopId = sqlQuery("SELECT id_shop FROM ps_shop WHERE active = 1 LIMIT 1;")
                    def shopGroupId = sqlQuery("SELECT id_shop_group FROM ps_shop WHERE id_shop = ${shopId};")

                    // Включаем Webservice
                    sqlExecute("UPDATE ps_configuration SET value = '1' WHERE name = 'PS_WEBSERVICE';")

                    // Создаём учётную запись
                    sqlExecute("""
                        INSERT INTO ps_webservice_account (key, description, active, date_add, date_upd, id_employee, id_shop_group, id_shop)
                        VALUES ('${hashedKey}', 'API-ключ: Jenkins CI', 1, NOW(), NOW(), 1, ${shopGroupId}, ${shopId});
                    """)

                    // Получаем ID нового ключа
                    def wsId = sqlQuery("SELECT id_webservice_account FROM ps_webservice_account WHERE description = 'API-ключ: Jenkins CI';")

                    if (!wsId) {
                        error 'Не удалось получить id_webservice_account после вставки'
                    }

                    // Выдаём полные права
                    def resources = sqlQuery("SELECT name FROM ps_webservice_definition;").split('\n')
                    ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].each { method ->
                        resources.each { resource ->
                            resource = resource.trim()
                            if (resource) {
                                sqlExecute("""
                                    INSERT IGNORE INTO ps_webservice_permission (resource, method, id_webservice_account)
                                    VALUES ('${resource}', '${method}', ${wsId});
                                """)
                            }
                        }
                    }

                    echo "Webservice активирован. API-ключ с полным доступом создан."
                }
            }
        }

        stage('Запуск UI-тестов через Selenoid') {
            steps {
                script {
                    echo 'Запуск тестового контейнера...'
                    sh '''
                        docker run --rm \\
                          --network selenoid4 \\
                          -e BROWSER='${params.BROWSER}' \\
                          -e BROWSER_VER='${params.BROWSER_VER}' \\
                          -e XDIST='${params.XDIST}' \\
                          -e LOG_LEVEL='${params.LOG_LEVEL}' \\
                          -e PS_API_URL=http://prestashop:80/api \\
                          -e PS_API_KEY=${PS_API_KEY} \\
                          -e REMOTE_URL='${params.REMOTE_URL}' \\
                          -v "jenkins_results:/root/Presta/${ALLURE_RESULTS}" \\
                          -v ${WORKSPACE}/${ALLURE_RESULTS}:/app/${ALLURE_RESULTS} \\
                          ${TEST_IMAGE}
                    '''
                }
            }
        }
        stage('Fetch Allure Results') {
            steps {
                sh '''
                set -e
                mkdir -p "$WORKSPACE/allure-results"
                cd "$WORKSPACE/allure-results"
                # никак не получалось смонтировать или скопировать результаты Allure в workspace (что то с правами)
                # нашел такое решение: захватить stdout и разархивировать в нужное место - сработало
                echo ==теперь копируем в workspace==
                docker run --rm -v jenkins_results:/data alpine tar -c -f - -C /data . | tar -x -f -
                chmod -R 777 .
                '''
            }
        }
        stage('Generate Allure Report') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: '${ALLURE_RESULTS}']]
                    ])
                }
            }
        }
    }
}

// === SQL-вспомогательные функции ===
def sqlQuery(query) {
    return sh(
        script: """
            docker exec -t -e MYSQL_PWD='admin' some-mysql \\
            mysql -u root -D prestashop -s -N -e "${query}"
        """,
        returnStdout: true
    ).trim()
}

def sqlExecute(query) {
    sh """
        docker exec -t -e MYSQL_PWD='admin' some-mysql \\
        mysql -u root -D prestashop -e "${query}"
    """
}