# ===== Base variables =====
PROJECT_NAME = shortener_users
DC = docker-compose

DC_FILE = docker-compose.yaml
ENV_FILE = env/.env


# ===== Docker automation =====
up:
	@echo "Run the bli db Docker container ..."
	${DC} --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${DC_FILE} up -d --build
	@echo "Success up!"

down:
	@echo "Stop the bli db Docker container ..."
	${DC} --env-file ${ENV_FILE} -p ${PROJECT_NAME} -f ${DC_FILE} down
	@echo "Success down!"



# ===== Linters & Formatter automation =====
lint:
	echo "Start linters ..."
	- ruff check --fix --silent .
	- ruff format --silent .
	echo "Linters done!"
