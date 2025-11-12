# Makefile for F1 Thermal Control System 🚀

run:
	python main.py

gui:
	python ui/dashboard.py

test:
	pytest --cov=core tests/

coverage:
	coverage html
	start htmlcov/index.html

analyze:
	python scripts/analyze_log.py

clean:
	del /Q /F data\*.csv
	del /Q /F htmlcov\*.*
