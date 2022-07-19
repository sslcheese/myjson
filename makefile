lcov:
	coverage run .\test_json.py
	coverage html -d coverage_result


test:
	pytest -vs   --cov=../myjson/ --cov-report=html   --html=htmlcov/report.html  test_json.py


clean:
	rm  *.yml

