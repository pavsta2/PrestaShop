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
                    sh 'docker compose -f up -d'

                    // Ждём, пока PrestaShop станет доступен
                    waitUntil {
                        script {
                            try {
                                def code = sh(
                                    script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 || echo '000'",
                                    returnStdout: true
                                ).trim()
                                return code == '200'
                            } catch (e) { return false }
                        }
                    }
                    echo 'PrestaShop доступен.'

                    // Ждём, пока установка завершится (файл settings.inc.php появится)
                    echo 'Ожидание завершения установки PrestaShop...'
                    def installed = false
                    for (int i = 0; i < 30; i++) {
                        def exists = sh(
                            script: "docker exec -t prestashop [ -f /var/www/html/config/settings.inc.php ] && echo 'yes' || echo 'no'",
                            returnStdout: true
                        ).trim()
                        if (exists == 'yes') {
                            installed = true
                            break
                        }
                        sleep(5)
                    }
                    if (!installed) {
                        error 'Установка PrestaShop не завершилась за 150 секунд.'
                    }
                    echo 'Установка завершена.'
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
                        error 'Не удалось получить _COOKIE_KEY_ из settings.inc.php'
                    }

                    // Генерируем API-ключ
                    def apiKey = sh(script: 'openssl rand -hex 16', returnStdout: true).trim()
                    env.PS_API_KEY = apiKey

                    // Получаем ID магазина
                    def shopId = sqlQuery("SELECT id_shop FROM ps_shop WHERE active = 1 LIMIT 1;")
                    def shopGroupId = sqlQuery("SELECT id_shop_group FROM ps_shop WHERE id_shop = ${shopId};")

                    // Включаем Webservice
                    sqlExecute("UPDATE ps_configuration SET value = '1' WHERE name = 'PS_WEBSERVICE';")

                    // Создаём аккаунт
                    sqlExecute("""
                        INSERT INTO ps_webservice_account (user, key_val, description, active, date_add, date_upd, id_employee, id_shop_group, id_shop)
                        VALUES ('jenkins-full', '', 'Full API access (CI)', 1, NOW(), NOW(), 1, ${shopGroupId}, ${shopId});
                    """)

                    // Получаем ID нового ключа
                    def wsId = sqlQuery("SELECT id_webservice_account FROM ps_webservice_account WHERE user = 'jenkins-full';")

                    // Хешируем: md5(apiKey + cookie_key)
                    def hashedKey = sh(
                        script: "php -r \"echo md5('${apiKey}' . '${cookieKey}');\"",
                        returnStdout: true
                    ).trim()

                    // Сохраняем хеш
                    sqlExecute("UPDATE ps_webservice_account SET key_val = '${hashedKey}' WHERE id_webservice_account = ${wsId};")

                    // Получаем все ресурсы из ps_webservice_definition
                    def resources = sqlQuery("SELECT name FROM ps_webservice_definition;").split('\n')
                    def methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

                    // Даём полные права на все ресурсы
                    resources.each { res ->
                        res = res.trim()
                        if (res) {
                            methods.each { method ->
                                sqlExecute("""
                                    INSERT IGNORE INTO ps_webservice_permission (resource, method, id_webservice_account)
                                    VALUES ('${res}', '${method}', ${wsId});
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
def sqlExecute(query) {
    sh """
        docker exec -t some-mysql mysql -u${DB_USER} -p${DB_PASS} -D${DB_NAME} -e "${query.replace('\n', ' ')}"
    """
}

def sqlQuery(query) {
    return sh(
        script: "docker exec -t some-mysql mysql -u${DB_USER} -p${DB_PASS} -D${DB_NAME} -s -N -e \"${query}\"",
        returnStdout: true
    ).trim()
}