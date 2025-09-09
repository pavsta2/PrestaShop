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
                    echo "Админка доступна по: http://localhost:8082/${PS_ADMIN_DIR_FIXED}"
                }
            }
        }

        stage('Запуск и ожидание установки PrestaShop') {
            steps {
                script {
                    echo 'Делаем запрос к PrestaShop для запуска установки...'

                    // Ждём доступности
                    waitUntil {
                        try {
                            def code = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://prestashop:80 || echo '000'",
                                returnStdout: true
                            ).trim()
                            return ['200', '301', '302'].contains(code)
                        } catch (e) {
                            return false
                        }
                    }

                    echo 'PrestaShop доступен. Установка начата...'


                }
            }
        }

        stage('Активация Webservice и создание API-ключа (полный доступ)') {
            steps {
                script {
                    echo 'Активация Webservice и создание API-ключа через PHP...'

                    // Генерируем ключ (32 символа)
                    def apiKey = sh(script: 'openssl rand -hex 16', returnStdout: true).trim() // 32 hex = 16 байт
                    env.PS_API_KEY = apiKey

                    // PHP-скрипт для выполнения в контейнере PrestaShop
                    def phpScript = """
                    <?php
                    require_once '/var/www/html/conpipeline {
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
                    echo "Админка доступна по: http://localhost:8082/${PS_ADMIN_DIR_FIXED}"
                }
            }
        }

        stage('Запуск и ожидание установки PrestaShop') {
            steps {
                script {
                    echo 'Делаем запрос к PrestaShop для запуска установки...'

                    // Ждём доступности
                    waitUntil {
                        try {
                            def code = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://prestashop:80 || echo '000'",
                                returnStdout: true
                            ).trim()
                            return ['200', '301', '302'].contains(code)
                        } catch (e) {
                            return false
                        }
                    }

                    echo 'PrestaShop доступен. Установка начата...'


                }
            }
        }

        stage('Активация Webservice и создание API-ключа (полный доступ)') {
            steps {
                script {
                    echo 'Активация Webservice и создание API-ключа через PHP...'

                    // Генерируем ключ (32 символа)
                    def apiKey = sh(script: 'openssl rand -hex 16', returnStdout: true).trim() // 32 hex = 16 байт
                    env.PS_API_KEY = apiKey

                    // PHP-скрипт для выполнения в контейнере PrestaShop
                    def phpScript = """
                    <?php
                    require_once '/var/www/html/config/config.inc.php';

                    // 1. Включаем Webservice
                    Configuration::updateValue('PS_WEBSERVICE', 1);
                    echo "Webservice включён\\n";

                    // 2. Создаём новый ключ
                    \$apiAccess = new WebserviceKey();
                    \$apiAccess->key = '${apiKey}';
                    if (!\$apiAccess->save()) {
                        echo "Ошибка при сохранении API-ключа\\n";
                        exit(1);
                    }
                    echo "API-ключ создан: ${apiKey}\\n";

                    // 3. Назначаем полные права на все ресурсы
                    \$resources = WebserviceRequest::getResources();
                    \$permissions = [];
                    foreach (\$resources as \$resourceName => \$resource) {
                        \$permissions[\$resourceName] = [
                            'GET' => 1,
                            'POST' => 1,
                            'PUT' => 1,
                            'PATCH' => 1,
                            'DELETE' => 1,
                            'HEAD' => 1
                        ];
                    }

                    WebserviceKey::setPermissionForAccount(\$apiAccess->id, \$permissions);
                    echo "Полные права выданы для ключа ID: {\$apiAccess->id}\\n";

                    echo "SUCCESS";
                    """

                    // Сохраняем скрипт во временный файл и выполняем
                    writeFile file: 'enable_webservice.php', text: phpScript

                    // Копируем в контейнер и выполняем
                    sh '''
                        docker cp enable_webservice.php prestashop:/tmp/enable_webservice.php
                        docker exec -t prestashop php /tmp/enable_webservice.php
                        RESULT=$(docker exec -t prestashop grep "SUCCESS" /tmp/enable_webservice.php.log 2>/dev/null || echo "")
                        docker exec -t prestashop rm -f /tmp/enable_webservice.php
                        if [ -z "$RESULT" ]; then
                            echo "Выполнение PHP-скрипта не завершилось успешно"
                            exit 1
                        fi
                    '''

                    echo "Webservice активирован, API-ключ с полными правами создан."
                    echo "Открытый ключ: ${apiKey}"
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
}fig/config.inc.php';

                    // 1. Включаем Webservice
                    Configuration::updateValue('PS_WEBSERVICE', 1);
                    echo "Webservice включён\\n";

                    // 2. Создаём новый ключ
                    \$apiAccess = new WebserviceKey();
                    \$apiAccess->key = '${apiKey}';
                    if (!\$apiAccess->save()) {
                        echo "Ошибка при сохранении API-ключа\\n";
                        exit(1);
                    }
                    echo "API-ключ создан: \${apiKey}\\n";

                    // 3. Назначаем полные права на все ресурсы
                    \$resources = WebserviceRequest::getResources();
                    \$permissions = [];
                    foreach (\$resources as \$resourceName => \$resource) {
                        \$permissions[\$resourceName] = [
                            'GET' => 1,
                            'POST' => 1,
                            'PUT' => 1,
                            'PATCH' => 1,
                            'DELETE' => 1,
                            'HEAD' => 1
                        ];
                    }

                    WebserviceKey::setPermissionForAccount(\$apiAccess->id, \$permissions);
                    echo "Полные права выданы для ключа ID: \${apiAccess->id}\\n";

                    echo "SUCCESS";
                    """

                    // Сохраняем скрипт во временный файл и выполняем
                    writeFile file: 'enable_webservice.php', text: phpScript

                    // Копируем в контейнер и выполняем
                    sh '''
                        docker cp enable_webservice.php prestashop:/tmp/enable_webservice.php
                        docker exec -t prestashop php /tmp/enable_webservice.php
                        RESULT=\$(docker exec -t prestashop grep "SUCCESS" /tmp/enable_webservice.php.log 2>/dev/null || echo "")
                        docker exec -t prestashop rm -f /tmp/enable_webservice.php
                        if [ -z "\$RESULT" ]; then
                            echo "Выполнение PHP-скрипта не завершилось успешно"
                            exit 1
                        fi
                    '''

                    echo "Webservice активирован, API-ключ с полными правами создан."
                    echo "Открытый ключ: ${apiKey}"
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